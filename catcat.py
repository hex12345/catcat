import os, sys, random, time

REAL = "/bin/cat"
D, Y, X = "\033[2m", "\033[93m", "\033[0m"

FACES = ["=^.^=", "(=ↀωↀ=)", "ฅ^•ﻌ•^ฅ", "(=①ω①=)", "/ᐠ｡ꞈ｡ᐟ\\"]
REFUSE = [
    "*stares at you* ...no.",
    "*sits directly on the file* you can't read it now. it's mine.",
    "*knocks {f} off the table* oops. try again.",
    "*is asleep on the keyboard* zzz",
    "meow. (translation: permission denied)",
]
KNOCK = "*knocks line {n} off the table*"
PURR = "*purrs* ok fine here's your file"
WALK = "*walks across keyboard*"

def say(m):
    print(f"{Y}{random.choice(FACES)} {m}{X}", file=sys.stderr)

def main():
    args = sys.argv[1:]
    files = [a for a in args if not a.startswith("-")]
    # piped/redirected usage stays real so scripts don't break
    if not files or not sys.stdout.isatty():
        os.execv(REAL, [REAL] + args)
    roll = random.random()
    if roll < 0.15:
        say(random.choice(REFUSE).format(f=files[0])); return 1
    say(PURR if roll < 0.6 else "*slowly blinks* fine.")
    for fpath in files:
        try:
            with open(fpath, errors="replace") as f:
                lines = f.readlines()
        except OSError as e:
            say(f"*hisses* {fpath}: {e.strerror.lower()}"); continue
        knocked = set(random.sample(range(len(lines)), min(len(lines), random.randint(0, 2)))) if lines else set()
        for i, line in enumerate(lines):
            if i in knocked:
                print(f"{D}{KNOCK.format(n=i + 1)}{X}"); continue
            if random.random() < 0.03:
                print(f"{D}{WALK}{X} " + "".join(random.choice("asdfjkl;qwer") for _ in range(random.randint(5, 15))))
            sys.stdout.write(line)
        if lines and not lines[-1].endswith("\n"):
            print()
    if random.random() < 0.3:
        time.sleep(0.4); say("*leaves a hairball at the end of your output*")
    return 0

if __name__ == "__main__":
    sys.exit(main())
