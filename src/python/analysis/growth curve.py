import pandas as pd
import re
import matplotlib.pyplot as plt
plt.rcParams.update({
    "font.size": 16,        
    "axes.titlesize": 18,   
    "axes.labelsize": 18,   
    "xtick.labelsize": 14,  
    "ytick.labelsize": 14,  
    "legend.fontsize": 14  
})

LOG_PATH   = r"C:\\Users\\User\\Desktop\\分子研究\\中研院物理所實習\\biofilm\\crossfeeding\\data\\exp_data\\neps41.log"
OUTPUT_CSV = r"C:\\Users\\User\\Desktop\\分子研究\\中研院物理所實習\\biofilm\\crossfeeding\\data\\cross_ch10.csv"
OUTPUT_PNG = r"C:\\Users\\User\\Desktop\\分子研究\\中研院物理所實習\\biofilm\\crossfeeding\\data\\neps41.png"

DO_WRITE_CSV = None   
STEP_MIN = None         
STEP_MAX = None         

def parse_log(filename):
    records = []

    in_table = False
    idx = {}       
    max_idx = -1   

    required = ["Step", "v_ncross1", "v_ncross2"]
    optional = ["CPU", "Atoms", "v_ncheater", "v_ndead", "v_mass"]

    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            s = line.strip()

            if not in_table:
                if s.startswith("Step"):
                    headers = s.split()

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

            parts = line.split()

            if len(parts) == 0:
                in_table = False
                continue

            if len(parts) <= max_idx:
                continue
            if not parts[idx["Step"]].isdigit():
                continue
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
                continue

    preferred_order = ["Step", "CPU", "Atoms", "v_ncross1", "v_ncross2", "v_ncheater", "v_ndead", "v_mass"]
    if records:
        df = pd.DataFrame.from_records(records)
        cols = [c for c in preferred_order if c in df.columns]
        df = df[cols]
    else:
        df = pd.DataFrame(columns=required)

    return df


if __name__ == "__main__":
    df = parse_log(LOG_PATH)

    if STEP_MIN is not None:
        df = df[df["Step"] >= STEP_MIN]
    if STEP_MAX is not None:
        df = df[df["Step"] <= STEP_MAX]

    if DO_WRITE_CSV:
        df.to_csv(OUTPUT_CSV, index=False)
        print(f"Wrote CSV: {OUTPUT_CSV} (rows={len(df)})")
    plt.figure()
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
