"""Finish the rented box's library work as one queue (2026-10-15); replaces the tail of `box_run.sh finish`.

The late location chains are the slow part: a 2016-2026 location snapshot takes about 25 CPU-minutes, not
the 4 measured on early seasons. With six blocks per chain the box would sit half idle for its last hours,
and the extensions would wait behind them. This queue:

1. retires the running location blocks 3-6 of 6, each right after it finishes a snapshot, and runs their
   dates as season blocks (library_blocks.py --block k/18, k = 7..17, one block per season). The cuts of the
   6-block split are cuts of the 18-block split, which is checked at start, and a cold start equals the
   sequential chain;
2. runs every chain's season-2027 penalty choice at once (library_extend.py --tune), then each chain's 2027q1
   extension as soon as its 2026-03-02 snapshot exists;
3. runs the era extension in finer segments (library_extend.py --era --segment k/n);
4. verifies each chain once no block of it is running, as box_run.sh does, and logs ALL DONE (or STOPPED) to
   logs/finish.log, which scripts/box_return.sh watches.

At most SLOTS library processes run at once, counting the blocks already running. A job that fails is run once
more (finished snapshots are skipped everywhere, so a rerun only redoes the unfinished one). Progress goes to
logs/schedule.log.

    /home/ubuntu/venv/bin/python -u scripts/box_schedule.py --dry     # print the plan; touch nothing
    SLOTS=22 nohup /home/ubuntu/venv/bin/python -u scripts/box_schedule.py > logs/schedule.out 2>&1 &
"""
import json
import os
import signal
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
PY = os.environ.get("PY", "/home/ubuntu/venv/bin/python")
SLOTS = int(os.environ.get("SLOTS", os.cpu_count()))
LIB = Path("experiments/cache/joint_capability_2026_09_18_v16_library_full1")
ERA = Path("experiments/cache/capability_library_era_extension")
EXT = Path("experiments/cache/capability_library_2027q1_extension")
BANKS, FAMILIES = ("offense", "defense"), ("location", "counts", "conversion", "recovery")
OLD, NEW = 6, 18                                     # location blocks: the running split and the season split
ERA_SEGMENTS = dict(location=4, counts=3, conversion=3, recovery=2)
ERA_COUNT, EXT_COUNT = 87, 8                         # era snapshots 2001-12..2009-02; 2026-04..2026-10 + 10-20
ENV = dict(os.environ, PYTHONPATH=f"{ROOT}:{ROOT}/scripts", PYTHONHASHSEED="160918",
           **{k: "1" for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
                               "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS")})
CHAIN = ("from experiments.joint_capability_repro import no_database\n"
         "from experiments.joint_capability_v16_library import chain\n"
         "with no_database(): chain('{lib}', '{bank}', '{family}')")


def stamp(message, *logs):
    line = f"{datetime.now():%F %T} {message}\n"
    for log in ("logs/schedule.log", *logs):
        with open(log, "a") as f:
            f.write(line)


def alive(pid):
    try:
        return Path(f"/proc/{pid}/stat").read_text().split(") ")[1][0] != "Z"
    except (OSError, IndexError):
        return False


def library_processes():
    """The library_blocks.py processes already running, by pid: their command lines."""
    found = {}
    for d in Path("/proc").iterdir():
        if d.name.isdigit() and int(d.name) != os.getpid():
            try:
                args = [a.decode() for a in (d / "cmdline").read_bytes().split(b"\0") if a]
            except OSError:
                continue
            if any(a.endswith("library_blocks.py") for a in args):
                found[int(d.name)] = args
    return found


def option(args, name):
    return args[args.index(name) + 1]


def done(directory, n=None):
    """Finished snapshots under a chain directory (or whether all n are)."""
    k = len(list(Path(directory, "snapshots").glob("*/complete.json")))
    return k if n is None else k >= n


def memory_available_gb():
    for line in Path("/proc/meminfo").read_text().splitlines():
        if line.startswith("MemAvailable:"):
            return int(line.split()[1]) / 2**20
    return 0.0


def season_split():
    """New block k (of NEW) for each old location block K (of OLD) from 3 on; checks the cuts line up."""
    from experiments.joint_capability_v16_library import schedule_frame
    from library_blocks import blocks
    dates = json.loads((LIB / "manifest.json").read_text())["dates"]
    schedule = schedule_frame()
    old, new = blocks(dates, schedule, OLD), blocks(dates, schedule, NEW)
    owner = {}
    for k, part in enumerate(new, 1):
        if part[0] >= old[2][0]:
            K = next(K for K, o in enumerate(old, 1) if part[0] in o)
            if not set(part) <= set(old[K - 1]):
                raise SystemExit(f"season block {k} crosses old block {K}")
            owner.setdefault(K, []).append(k)
    covered = sorted(d for K in owner for k in owner[K] for d in new[k - 1])
    if covered != sorted(d for o in old[2:] for d in o):
        raise SystemExit("season blocks do not cover old blocks 3..6 exactly")
    return owner, new


class Job:
    def __init__(self, name, args, log, ready=lambda: True, priority=0):
        self.name, self.args, self.log, self.ready, self.priority = name, args, log, ready, priority
        self.proc, self.tries, self.finished, self.failed = None, 0, False, False

    def start(self):
        self.tries += 1
        stamp(f"start {self.name} (try {self.tries})")
        with open(self.log, "a") as out:
            self.proc = subprocess.Popen(self.args, stdout=out, stderr=subprocess.STDOUT, env=ENV, cwd=ROOT)

    def poll(self):
        if self.proc is None or self.proc.poll() is None:
            return
        code, self.proc = self.proc.returncode, None
        if code == 0:
            self.finished = True
            stamp(f"done {self.name}")
        elif self.tries < 2:
            stamp(f"FAILED {self.name} (exit {code}, see {self.log}); retrying")
        else:
            self.failed = True
            stamp(f"STOPPED: {self.name} failed twice (exit {code}, see {self.log}); the rest of the queue goes on",
                  "logs/finish.log")


def main():
    finish = "logs/finish.log"
    owner, new = season_split()
    if "--dry" not in sys.argv:
        stamp(f"queue on {SLOTS} slots; season blocks {owner}", finish)
    dry = "--dry" in sys.argv
    old = library_processes()
    retire, keep = {}, {}
    for pid, args in old.items():
        bank, family, block = option(args, "--bank"), option(args, "--family"), option(args, "--block")
        log = os.readlink(f"/proc/{pid}/fd/1")          # the block's own log
        if family == "location" and block.split("/")[1] == str(OLD) and int(block.split("/")[0]) in owner:
            marks = sum(line.startswith("BLOCK ") for line in open(log))
            retire[pid] = dict(bank=bank, K=int(block.split("/")[0]), log=log, marks=marks, sent=False)
        else:
            keep[pid] = dict(bank=bank, family=family, args=args, log=log)
    if not dry:
        stamp(f"running blocks: {len(retire)} to retire at their next snapshot, {len(keep)} kept")
    retired = set()

    jobs = []
    lib = lambda b, f: LIB / "chains" / b / f
    for bank in BANKS:
        for K, ks in owner.items():
            for k in ks:
                jobs.append(Job(f"location {bank} {k}/{NEW}",
                                [PY, "-u", "scripts/library_blocks.py", "--out", str(LIB), "--bank", bank,
                                 "--family", "location", "--block", f"{k}/{NEW}"],
                                f"logs/block_{bank}_location_{k}of{NEW}.log",
                                ready=lambda b=bank, K=K: (b, K) in retired,
                                priority=0 if k == max(owner[max(owner)]) else 2))
        for family in FAMILIES:
            tuned = Job(f"tune2027 {bank} {family}",
                        [PY, "-u", "scripts/library_extend.py", "--tune", "--bank", bank, "--family", family],
                        f"logs/tune2027_{bank}_{family}.log", priority=1)
            jobs.append(tuned)
            jobs.append(Job(f"ext2027 {bank} {family}",
                            [PY, "-u", "scripts/library_extend.py", "--bank", bank, "--family", family],
                            f"logs/ext2027_{bank}_{family}.log",
                            ready=lambda b=bank, f=family, t=tuned: t.finished and
                            (lib(b, f) / "snapshots" / "2026-03-02" / "complete.json").exists(), priority=1))
            n = ERA_SEGMENTS[family]
            for k in range(1, n + 1):
                jobs.append(Job(f"era {bank} {family} {k}/{n}",
                                [PY, "-u", "scripts/library_extend.py", "--era", "--bank", bank, "--family", family,
                                 "--segment", f"{k}/{n}"],
                                f"logs/era_{bank}_{family}_{k}of{n}.log", priority=3 if family == "location" else 4))
    blocks_of = lambda b, f: [j for j in jobs if j.name.startswith(f"{f} {b} ")]
    for bank in BANKS:
        for family in FAMILIES:
            def chain_ready(b=bank, f=family):
                quiet = not any(p in keep and keep[p]["bank"] == b and keep[p]["family"] == f and alive(p) for p in keep)
                quiet &= not any(r["bank"] == b and alive(p) for p, r in retire.items()) or f != "location"
                return quiet and all(j.finished for j in blocks_of(b, f)) and done(lib(b, f), 254)
            jobs.append(Job(f"chain {bank} {family}",
                            [PY, "-u", "-c", CHAIN.format(lib=LIB, bank=bank, family=family)],
                            f"logs/chain_{bank}_{family}.log", ready=chain_ready, priority=5))
    jobs.sort(key=lambda j: j.priority)
    if dry:
        print(f"season blocks per old block: {owner}")
        for pid, r in retire.items():
            print(f"retire {pid} location {r['bank']} {r['K']}/{OLD} {r['log']} ({r['marks']} snapshots logged)")
        for pid, k in keep.items():
            print(f"keep {pid} {k['family']} {k['bank']} {option(k['args'], '--block')} {k['log']}")
        for j in jobs:
            print(f"job p{j.priority} {j.name} ready={j.ready()} -> {j.log}\n    {' '.join(j.args)[:150]}")
        return

    last_report = 0
    while True:
        for pid, r in retire.items():
            key = (r["bank"], r["K"])
            if key in retired:
                continue
            if not alive(pid):
                retired.add(key)
                stamp(f"retired location {r['bank']} {r['K']}/{OLD}")
            elif not r["sent"] and sum(line.startswith("BLOCK ") for line in open(r["log"])) > r["marks"]:
                os.kill(pid, signal.SIGTERM)
                r["sent"] = True
        for pid, k in list(keep.items()):
            if not alive(pid):
                tail = open(k["log"]).read()[-2000:]
                if "BLOCK_DONE" not in tail:      # died without finishing: run its command again as a job
                    stamp(f"FAILED kept block {k['family']} {k['bank']} {option(k['args'], '--block')}; rerunning")
                    jobs.insert(0, Job(f"{k['family']} {k['bank']} {option(k['args'], '--block')} (rerun)",
                                       [PY, "-u", *k["args"][k["args"].index("scripts/library_blocks.py"):]],
                                       k["log"], priority=0))
                    jobs[0].tries = 1
                del keep[pid]
        for j in jobs:
            j.poll()
        running = sum(alive(p) for p in keep) + sum(alive(p) for p in retire) + \
            sum(j.proc is not None for j in jobs)
        launched = 0
        for j in jobs:
            if running >= SLOTS or launched >= 2 or memory_available_gb() < 8:
                break
            if j.proc is None and not j.finished and not j.failed and j.ready():
                j.start()
                running += 1
                launched += 1
        if time.time() - last_report > 900:
            last_report = time.time()
            counts = " ".join(f"{b[:3]}/{f[:3]} {done(lib(b, f))}+{done(ERA / 'chains' / b / f)}"
                              f"+{done(EXT / 'chains' / b / f)}" for b in BANKS for f in FAMILIES)
            stamp(f"running {running}; snapshots library+era+2027q1: {counts}; "
                  f"memory free {memory_available_gb():.0f} GB")
        startable = [j for j in jobs if j.proc is not None or (not j.finished and not j.failed and j.ready())]
        if not startable and not keep and all(not alive(p) for p in retire):
            break                                  # nothing running and nothing left that can start
        time.sleep(20)

    failed = [j.name for j in jobs if not j.finished]
    receipts = all((lib(b, f) / "complete.json").exists() for b in BANKS for f in FAMILIES)
    era = all(done(ERA / "chains" / b / f, ERA_COUNT) for b in BANKS for f in FAMILIES)
    ext = all(done(EXT / "chains" / b / f, EXT_COUNT) for b in BANKS for f in FAMILIES)
    if failed or not (receipts and era and ext):
        stamp(f"STOPPED: unfinished {failed}; chain receipts {receipts}, era {era}, 2027q1 {ext}", finish)
        sys.exit(1)
    stamp("ALL DONE", finish)


if __name__ == "__main__":
    main()
