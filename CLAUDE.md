# Cross-Feeder Biofilm Simulation

## Quick Reference

**Project**: Agent-based simulation of cross-feeding bacteria with EPS
**Tech**: NUFEB/LAMMPS, C++, Python (SALib, BoTorch, Ray)
**Author**: 邱弈瑞 (Chiu, Yi-Jui)、蔡秀吉 (Hsiu-Chi Tsai)

---

## Project Overview

**Goal**: Explore how EPS production and spatial structure affect the survival time of
cross-feeding communities in the presence of metabolite cheaters, using NUFEB + LAMMPS
as the simulator and Python for large-scale parameter sweeps, sensitivity analysis,
and surrogate modelling.

**Core Idea**: Treat each NUFEB run as an expensive black-box function `f(theta)` that
outputs metrics such as consortium collapse time, biomass trajectories, and spatial
structure indicators.

---

## Directory Structure

```
.
├── CLAUDE.md              # 本檔案 - 專案指引
├── README.md              # 快速開始指南
├── requirements.txt       # Python 依賴
├── Snakefile              # Snakemake 工作流
├── .gitignore             # Git 排除規則
│
├── src/                   # 原始碼
│   ├── cpp/
│   │   └── growth_models/ # C++ NUFEB 自訂生長模型
│   │       ├── fix_growth_cross1.cpp/.h
│   │       ├── fix_growth_cross2.cpp/.h
│   │       ├── fix_growth_cheater.cpp/.h
│   │       ├── fix_growth_eps.cpp/.h
│   │       └── fix_eps_secretion.cpp/.h
│   └── python/
│       ├── eps_biofilm/   # 主要分析套件
│       │   ├── parameter_space.py  # 參數定義與取樣
│       │   ├── io_nufeb.py         # NUFEB 輸出解析
│       │   ├── metrics.py          # 計算崩潰時間等指標
│       │   ├── salib_sensitivity.py # 全域敏感度分析
│       │   ├── botorch_surrogate.py # GP 代理模型
│       │   └── plots.py            # 繪圖工具
│       ├── analysis/
│       │   ├── theory_models/      # 理論模型視覺化
│       │   │   ├── cheater.py      # 含 cheater 的動態
│       │   │   ├── no_cheater.py   # 無 cheater 的動態
│       │   │   └── LSA1.py         # 線性穩定性分析
│       │   ├── collect_lifetime.py # 存活時間分析
│       │   └── growth_curve.py     # 生長曲線繪製
│       └── input_generation/       # 輸入檔生成器
│
├── scripts/               # 執行腳本
│   ├── run_single_sim.py  # 單次模擬
│   ├── run_sweep.py       # 參數掃描
│   ├── aggregate_results.py
│   └── parse_outputs.py
│
├── configs/               # 參數配置 (YAML)
│   └── params_example.yaml
│
├── config/                # NUFEB 輸入腳本
│   ├── inputscript_EPS.nufeb
│   └── inputscript_NEPS_ch.nufeb
│
├── templates/             # NUFEB 輸入模板
│   └── base_nufeb_input.in
│
├── docs/                  # 文件
│   ├── poster.md          # 海報內容
│   ├── context.md         # 口頭報告稿
│   ├── Install_NUFEB.md   # NUFEB 安裝指南
│   ├── TOOLS.md           # 工具清單
│   ├── images/            # 海報圖片
│   └── references/        # PDF 文獻 (~28 篇)
│
├── notebooks/             # Jupyter 筆記本
│   ├── 00_exploration.ipynb
│   └── 10_paper_figures.ipynb
│
├── data/                  # 資料
│   ├── raw/               # 原始 NUFEB 輸出
│   └── processed/         # 處理後的指標
│
├── biofilm/               # NUFEB 工作區 (大部分在 .gitignore)
│
├── archive/               # 舊版歸檔
│   └── data_and_code/
│
└── .github/workflows/     # CI 配置
    └── ci.yml
```

---

## Key Files

### C++ Growth Models
- `fix_growth_cross1.cpp` - Cross-feeder 1 生長 (Monod + 代謝物交換)
- `fix_growth_cross2.cpp` - Cross-feeder 2 生長
- `fix_growth_cheater.cpp` - Cheater 生長 (只消耗不分泌)
- `fix_eps_secretion.cpp` - EPS 粒子分泌機制

### Python Analysis
- `src/python/eps_biofilm/metrics.py` - 計算崩潰時間
- `src/python/eps_biofilm/salib_sensitivity.py` - Sobol 敏感度分析
- `src/python/eps_biofilm/botorch_surrogate.py` - 貝葉斯優化

---

## Commands

```bash
# 建立環境
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 執行單次模擬
cd biofilm/crossfeeding
mpirun -np 4 lmp_mpi -in inputscript_EPS.nufeb

# 執行參數掃描
python scripts/run_sweep.py --config configs/params_example.yaml --n-samples 32

# 生成初始原子配置
python src/python/input_generation/atom_generate.py

# 分析存活時間
python src/python/analysis/collect_lifetime.py
```

---

## Development Guidelines

**CRITICAL**: Follow these rules when editing code:

- TDD: Write tests first, implement all planned tasks
- Boy Scout Rule: Leave code cleaner than found
- Small CLs: Keep changes focused and minimal
- **NEVER**: Over-generate, premature abstraction
- **NEVER**: Use flashy syntax unnecessarily
- Comments: 繁體中文, shorter than code itself
- Bug fixes: Analyze logs step-by-step, don't guess

開發計畫務必整合 "TDD Rule" 和 "Boy Scout Rule" 或是 "Small CLs"。
程式碼要像人類撰寫，保持自然，遵循 Code Readability。

---

## Excluded from Git

- `biofilm/` simulation outputs (VTK, HDF5, ~26GB)
- `ParaView-*/` (external software, 3.4GB)
- `*.vtu`, `*.vti`, `*.h5`, `*.zip`, `*.mp4`

---

## Tech Stack

### Simulation
- NUFEB / LAMMPS (C++, MPI)
- Custom growth fixes

### Orchestration & Analysis (Python 3.10+)
- **Snakemake / Ray** - 參數掃描調度
- **SALib** - 全域敏感度分析
- **BoTorch / GPyTorch** - GP 代理模型
- **NumPy / pandas / xarray** - 資料處理
- **matplotlib / seaborn** - 視覺化

---

## Restructuring Log (2025-12-02)

### 檔案移動記錄

| 原位置 | 新位置 | 說明 |
|--------|--------|------|
| `/*.pdf` (8 files) | `docs/references/` | 根目錄 PDF 文獻 |
| `ref/*.pdf` (20 files) | `docs/references/` | ref 目錄 PDF 文獻 |
| `image*.png`, `l_square.jpg` | `docs/images/` | 海報圖片 |
| `cheater.py`, `no_cheater.py`, `LSA1.py` | `src/python/analysis/theory_models/` | 理論模型腳本 |
| `poster.md`, `context.md`, `Install NUFEB.md` | `docs/` | 文件檔案 |
| `data_and_code/`, `data_and_code.zip` | `archive/` | 舊版歸檔 |
| `goal/src/eps_biofilm/*` | `src/python/eps_biofilm/` | 整合新分析套件 |
| `goal/scripts/*` | `scripts/` | 執行腳本 |
| `goal/configs/*` | `configs/` | 參數配置 |
| `goal/templates/*` | `templates/` | NUFEB 模板 |
| `goal/notebooks/*` | `notebooks/` | Jupyter 筆記本 |
| `goal/.github/*` | `.github/` | CI 配置 |
| `goal/TOOLS.md` | `docs/TOOLS.md` | 工具文件 |

### 刪除的檔案
- `data_generate.py`, `data_preview.py` (根目錄重複)
- `ref/` 空目錄
- `goal/` 目錄 (已整合)

---

## Future Research Directions

### 文獻調研摘要 (2025-12-02)

#### 核心文獻
| 主題 | 關鍵發現 | 來源 |
|------|----------|------|
| EPS 作為公共財 | EPS 保護群落免受壓力，但可被 cheater 利用 | Dragoš et al. 2018, ISME J |
| 空間結構雙面性 | 空間隔離可保護合作者，但也可能讓 cheater 建立據點 | Nadell et al. 2016, Nat Rev Microbiol |
| 代謝交叉餵養 | 45-65% 的腸道菌種依賴交叉餵養 | Zelezniak et al. 2015, PNAS |
| 公共財困境 | Siderophore 分泌實驗證實頻率依賴選擇 | Griffin et al. 2004, Nature |

#### 理論框架
- **Public Goods Game**: 將 EPS 和代謝物視為可被剝削的公共財
- **Spatial Evolutionary Game Theory**: 空間結構下的演化穩定策略
- **Inclusive Fitness / Kin Selection**: 親緣關係如何影響合作演化

---

### 潛在學術貢獻方向

#### 方向 1：EPS 產量的演化穩定策略 (ESS)
**問題**: 什麼樣的 EPS 分泌策略能在 cheater 存在下演化穩定？
**方法**:
- NUFEB 模擬不同 EPS 產率的競爭
- 建立適應度函數 fitness = f(EPS_rate, local_density, cheater_freq)
- 使用 evolutionary invasion analysis 判斷 ESS
**創新點**: 結合 individual-based model 與演化博弈論

#### 方向 2：空間異質性對合作的非線性效應
**問題**: EPS 產生的空間異質性如何影響 cross-feeder 與 cheater 的共存？
**方法**:
- 追蹤空間指標：pair correlation function, local density variance
- 相變分析：識別合作崩潰的臨界點
- SALib Sobol 分析各參數對空間結構的貢獻
**創新點**: 首次在 IbM 框架下系統量化 EPS-空間-合作 的三角關係

#### 方向 3：GP 代理模型加速參數探索
**問題**: 如何高效探索高維參數空間？
**方法**:
- BoTorch 建立 GP 代理模型
- Expected Improvement (EI) 或 UCB 策略
- 主動學習選擇下一批模擬點
**創新點**: 將機器學習代理模型應用於 biofilm 模擬，減少計算成本

#### 方向 4：多尺度分析
**問題**: 細胞層級的隨機性如何影響群落層級的穩定性？
**方法**:
- 微觀：單細胞生長隨機性、分裂方向
- 介觀：colony 形態、代謝物梯度
- 巨觀：群落崩潰時間分布
**創新點**: 連結微觀機制與巨觀湧現現象

---

### 已確認實作項目

1. **Sobol 敏感度分析** (優先級：高)
   - 參數：EPS 產率、生長速率、代謝物擴散係數、初始 cheater 比例
   - 輸出：崩潰時間的一階/總階 Sobol 指數
   - 工具：`src/python/eps_biofilm/salib_sensitivity.py`

2. **GP 代理模型** (優先級：高)
   - 輸入：參數向量 θ
   - 輸出：預測崩潰時間 + 不確定性
   - 工具：`src/python/eps_biofilm/botorch_surrogate.py`

3. **空間統計指標** (優先級：中)
   - Pair correlation function g(r)
   - Local clustering coefficient
   - Voronoi tessellation 分析

4. **視覺化 Dashboard** (優先級：低)
   - 整合所有指標的互動式介面
   - 可能使用 Panel 或 Streamlit

---

### 待驗證假說

1. **H1**: EPS 產生的空間隔離增加 cross-feeder 之間的代謝物濃度，提升合作效益
2. **H2**: 存在最佳 EPS 產率，過高會消耗過多資源，過低無法有效隔離 cheater
3. **H3**: 初始空間配置對最終存活時間有顯著影響（path dependence）
4. **H4**: 崩潰時間分布呈現非高斯特徵，反映底層的臨界動力學

---

### 實驗驗證可能性

若模擬結果顯著，可考慮以下實驗系統驗證：
- **E. coli 互補營養缺陷型** (auxotrophs)：經典 cross-feeding 系統
- **Pseudomonas aeruginosa biofilm**：天然 EPS 產生者
- **合成生物學線路**：可調控 EPS 產量的工程菌株
- **微流控晶片**：控制空間結構和代謝物梯度
