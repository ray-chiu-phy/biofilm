from pathlib import Path
import re
import sys

OUTPUT_PREFIX = "inputscript_EPS"  
N_FILES = 50                       
INDEX_START = 1                    
TEMPLATE_NAME = "inputscript_EPS.nufeb"
LABELS = {
    "div1": (1, 101),
    "div2": (2, 102),
    "div3": (3, 103),
    "eps1": (4, 104),
    "eps2": (5, 105),
}

DIV_PATTERN = re.compile(
    r'^(?P<prefix>\s*fix\s+div(?P<num>[1-3])\b[^\n]*?\bnufeb/division/coccus\b[^\n]*?\s)'
    r'(?P<seed>\d+)(?P<suffix>\s*(?:#.*)?)$',
    flags=re.MULTILINE
)

EPS_PATTERN = re.compile(
    r'^(?P<prefix>\s*fix\s+eps(?P<num>[1-2])\b[^\n]*?\bnufeb/eps_secretion\b[^\n]*?\s)'
    r'(?P<seed>\d+)(?P<suffix>\s*(?:#.*)?)$',
    flags=re.MULTILINE
)

def seed_for(label: str, i: int) -> int:
    v, offset = LABELS[label]
    return i*i*(v*v) + 2*v + offset

def make_versioned_content(text: str, idx: int) -> str:
    def repl_div(m: re.Match) -> str:
        which = m.group("num")
        label = f"div{which}"
        return f"{m.group('prefix')}{seed_for(label, idx)}{m.group('suffix')}"
    def repl_eps(m: re.Match) -> str:
        which = m.group("num")
        label = f"eps{which}"
        return f"{m.group('prefix')}{seed_for(label, idx)}{m.group('suffix')}"
    text = DIV_PATTERN.sub(repl_div, text)
    text = EPS_PATTERN.sub(repl_eps, text)
    return text

def main():
    here = Path(__file__).parent
    src = here / TEMPLATE_NAME
    if not src.exists():
        sys.exit(f"No：{src}")

    text = src.read_text(encoding="utf-8")
    outs = []
    for i in range(INDEX_START, INDEX_START + N_FILES):
        new_text = make_versioned_content(text, i)
        out = src.with_name(f"{OUTPUT_PREFIX}{i}.nufeb")
        out.write_text(new_text, encoding="utf-8")
        outs.append(out.name)

    print("generate：")
    for name in outs:
        print("  ", name)

if __name__ == "__main__":
    main()
