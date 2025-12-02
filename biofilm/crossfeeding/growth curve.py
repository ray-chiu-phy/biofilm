import pandas as pd
import re
import matplotlib.pyplot as plt
# 放在 import 後面
plt.rcParams.update({
    "font.size": 16,        # 全域基準字體
    "axes.titlesize": 18,   # (若有) 圖標題
    "axes.labelsize": 18,   # x/y 軸標題
    "xtick.labelsize": 14,  # x 刻度字
    "ytick.labelsize": 14,  # y 刻度字
    "legend.fontsize": 14   # 圖例字
    # 如需顯示中文，可加： "font.sans-serif": ["Noto Sans CJK TC","Microsoft JhengHei","Arial Unicode MS"]
})


# =========================
# Config（內部參數）
# =========================
LOG_PATH   = r"C:\\Users\\User\\Desktop\\分子研究\\中研院物理所實習\\biofilm\\crossfeeding\\data\\exp_data\\neps41.log"
OUTPUT_CSV = r"C:\\Users\\User\\Desktop\\分子研究\\中研院物理所實習\\biofilm\\crossfeeding\\data\\cross_ch10.csv"
OUTPUT_PNG = r"C:\\Users\\User\\Desktop\\分子研究\\中研院物理所實習\\biofilm\\crossfeeding\\data\\neps41.png"

DO_WRITE_CSV = None     # 是否輸出 CSV
STEP_MIN = None         # 例如 100；None 代表不限制下限
STEP_MAX = None         # 例如 300；None 代表不限制上限
# =========================


def parse_log(filename):
    """
    Parse LAMMPS/NUFEB log.
    Required: Step, v_ncross1, v_ncross2
    Optional: CPU, Atoms, v_ncheater, v_ndead, v_mass
    """
    records = []

    # 狀態與欄位索引
    in_table = False
    idx = {}       # 欄名 -> split() 後的索引
    max_idx = -1   # 目前需要的最大欄位索引（用來檢查欄位是否足夠）

    required = ["Step", "v_ncross1", "v_ncross2"]
    optional = ["CPU", "Atoms", "v_ncheater", "v_ndead", "v_mass"]

    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            s = line.strip()

            # 1) 找表頭
            if not in_table:
                if s.startswith("Step"):
                    headers = s.split()

                    # 只要必備三欄都在表頭，才開始解析
                    if all(k in headers for k in required):
                        idx.clear()
                        max_idx = -1
                        for k in required + optional:
                            if k in headers:
                                idx[k] = headers.index(k)
                                if idx[k] > max_idx:
                                    max_idx = idx[k]
                        in_table = True
                continue

            # 2) 在表格中：嘗試解析資料列（最小改動版）
            parts = line.split()

            # 空行視為表格結束
            if len(parts) == 0:
                in_table = False
                continue

            # 只加兩個判斷：
            # (a) 欄位數要夠（至少到目前需要的最大索引）
            if len(parts) <= max_idx:
                continue
            # (b) Step 欄必須是純整數（避免 64.7% 等摘要行）
            if not parts[idx["Step"]].isdigit():
                continue

            # 嘗試轉型；若遇到 '64.7%' 這類格式就略過
            try:
                rec = {
                    "Step": int(parts[idx["Step"]]),
                    "v_ncross1": int(parts[idx["v_ncross1"]]),
                    "v_ncross2": int(parts[idx["v_ncross2"]]),
                }
                if "CPU" in idx:
                    rec["CPU"] = float(parts[idx["CPU"]])
                if "Atoms" in idx:
                    rec["Atoms"] = int(parts[idx["Atoms"]])
                if "v_ncheater" in idx:
                    rec["v_ncheater"] = int(parts[idx["v_ncheater"]])
                if "v_ndead" in idx:
                    rec["v_ndead"] = int(parts[idx["v_ndead"]])
                if "v_mass" in idx:
                    rec["v_mass"] = float(parts[idx["v_mass"]])

                records.append(rec)
            except ValueError:
                # 任何非數字（或非標準科學記號）導致轉型失敗就跳過
                continue

    # 按偏好順序輸出；不存在的欄位自動跳過
    preferred_order = ["Step", "CPU", "Atoms", "v_ncross1", "v_ncross2", "v_ncheater", "v_ndead", "v_mass"]
    if records:
        df = pd.DataFrame.from_records(records)
        cols = [c for c in preferred_order if c in df.columns]
        df = df[cols]
    else:
        df = pd.DataFrame(columns=required)

    return df


if __name__ == "__main__":
    # 解析
    df = parse_log(LOG_PATH)

    # 依內部參數做 Step 篩選
    if STEP_MIN is not None:
        df = df[df["Step"] >= STEP_MIN]
    if STEP_MAX is not None:
        df = df[df["Step"] <= STEP_MAX]

    # 輸出 CSV（可關閉）
    if DO_WRITE_CSV:
        df.to_csv(OUTPUT_CSV, index=False)
        print(f"Wrote CSV: {OUTPUT_CSV} (rows={len(df)})")

    # 畫圖：Step vs Cross1/Cross2/Cheater
    plt.figure()
    # 三條線：有欄位才畫
    if "v_ncross1" in df.columns:
        plt.plot(df["Step"], df["v_ncross1"], label="Cross1", color="b")
    if "v_ncross2" in df.columns:
        plt.plot(df["Step"], df["v_ncross2"], label="Cross2", color="g")
    if "v_ncheater" in df.columns:
        plt.plot(df["Step"], df["v_ncheater"], label="Cheater", color="r")

    plt.xlabel("Simulation Step")
    plt.ylabel("Number")
    plt.ylim(0, 3000)
    #plt.title("Population Counts Over Steps")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_PNG, dpi=150)
    print(f"Wrote plot: {OUTPUT_PNG}")
