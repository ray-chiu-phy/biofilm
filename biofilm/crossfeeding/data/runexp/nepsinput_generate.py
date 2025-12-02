#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Standalone NUFEB input generator (no external args).
- 讀取同資料夾的模板檔：inputscript_NEPS_ch.nufeb
- 將三條 division fix 的最後一個整數 seed 改為：
    div1: i^2 * 1
    div2: i^2 * 2
    div3: i^2 * 3
  其中 i 為輸出檔案的索引（預設 0..9）
- 產生：inputscript_NEPS{i}.nufeb
"""

from pathlib import Path
import re
import sys

# ===== 可在這裡調整 =====
OUTPUT_PREFIX = "inputscript_NEPS"     # 輸出檔名前綴
N_FILES = 50                           # 產生檔數：索引 0..N_FILES-1
INDEX_START = 1                        # 起始索引
SEED_MULT = {"1": 1, "2": 2, "3": 3}   # div1/div2/div3 的乘數
TEMPLATE_NAME = "inputscript_NEPS.nufeb"  # 模板檔名（需與本檔同夾）
# =======================

# 模板路徑：與本腳本同資料夾
SRC = Path(__file__).with_name(TEMPLATE_NAME)

def make_versioned_content(text: str, idx: int) -> str:
    """
    將模板文字中的三條 division/coccus 指令之 seed 替換為
    i^2 * 對應乘數（div1->*1, div2->*2, div3->*3）。
    僅動到「行尾的整數種子」。
    """
    SEED_MULT   = {"1": 1, "2": 2, "3": 3}        # 乘數
    SEED_OFFSET = {"1": 101, "2": 102, "3": 103}  # 加數

    seeds = {k: (idx * idx * (v**2) + 2*v + SEED_OFFSET.get(k, 0)) for k, v in SEED_MULT.items()}


    # 範例行：
    #   fix div1 CROSS1 nufeb/division/coccus 1.36e-6 1234
    # 僅替換最後那個整數（1234）
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
        sys.exit(f"模板檔不存在：{SRC}")

    text = SRC.read_text()
    out_files = []

    for i in range(INDEX_START, INDEX_START + N_FILES):
        new_text = make_versioned_content(text, i)
        out = SRC.with_name(f"{OUTPUT_PREFIX}{i}.nufeb")
        out.write_text(new_text)
        out_files.append(out.name)

    print("已產生：")
    for name in out_files:
        print("  ", name)

if __name__ == "__main__":
    main()
