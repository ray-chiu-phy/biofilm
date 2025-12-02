from pathlib import Path
import re
import sys


OUTPUT_PREFIX = "inputscript_NEPS"    
N_FILES = 50                           
INDEX_START = 1                       
SEED_MULT = {"1": 1, "2": 2, "3": 3}  
TEMPLATE_NAME = "inputscript_NEPS.nufeb"  

SRC = Path(__file__).with_name(TEMPLATE_NAME)

def make_versioned_content(text: str, idx: int) -> str:
    SEED_MULT   = {"1": 1, "2": 2, "3": 3}        
    SEED_OFFSET = {"1": 101, "2": 102, "3": 103} 

    seeds = {k: (idx * idx * (v**2) + 2*v + SEED_OFFSET.get(k, 0)) for k, v in SEED_MULT.items()}

    pattern = re.compile(
        r'^(?P<prefix>\s*fix\s+div(?P<div>[123])\b[^\n]*?\bnufeb/division/coccus\b[^\n]*?\s)'
        r'(?P<seed>\d+)(?P<suffix>\s*(?:#.*)?)$',
        flags=re.MULTILINE
    )

    def repl(m: re.Match) -> str:
        d = m.group("div")  # "1" / "2" / "3"
        new_seed = seeds.get(d, m.group("seed"))
        return f"{m.group('prefix')}{new_seed}{m.group('suffix')}"

    new_text, _ = pattern.subn(repl, text)
    return new_text

def main() -> None:
    if not SRC.exists():
        sys.exit(f"No：{SRC}")

    text = SRC.read_text()
    out_files = []

    for i in range(INDEX_START, INDEX_START + N_FILES):
        new_text = make_versioned_content(text, i)
        out = SRC.with_name(f"{OUTPUT_PREFIX}{i}.nufeb")
        out.write_text(new_text)
        out_files.append(out.name)

    print("generate：")
    for name in out_files:
        print("  ", name)

if __name__ == "__main__":
    main()
