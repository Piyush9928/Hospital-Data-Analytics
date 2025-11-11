"""
Hospital Data – End-to-End Analysis Pipeline
- Reads Excel
- Cleans & normalizes columns
- DEDUPes
- Derives fields (age_band, membership_status, etc.)
- Exploratory analysis & charts (matplotlib)
- Exports cleaned file + summaries

Run: python analysis.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import os

RAW_PATH = "Hospital Data Revised.xlsx"          # <-- input file
OUT_XLSX = "hospital_cleaned.xlsx"
OUT_SUMMARY = "hospital_summary.csv"
FIG_DIR = "hospital_figs"

os.makedirs(FIG_DIR, exist_ok=True)

# ---------- Helpers ----------
def to_snake(s: str) -> str:
    s = str(s).strip()
    s = re.sub(r"[^\w\s]", "", s)
    s = re.sub(r"\s+", "_", s)
    return s.lower()

def has(df, colname): return colname in df.columns

# ---------- Load ----------
df_raw = pd.read_excel(RAW_PATH)
df = df_raw.copy()
df.columns = [to_snake(c) for c in df.columns]

# ---------- Light cleaning ----------
# Strip whitespace strings
for c in df.columns:
    if df[c].dtype == "object":
        df[c] = (
            df[c]
            .astype(str).str.strip()
            .replace({"nan": np.nan, "None": np.nan, "": np.nan})
        )

# Coerce common numerics
for c in ["age","pincode","zipcode","daywisesno","tahsilid","blockid","stateid","cityid","districtid"]:
    if has(df,c):
        df[c] = pd.to_numeric(df[c], errors="coerce")

# Parse date-like columns
for c in df.columns:
    if any(x in c for x in ["date","dob","created","updated","registration"]):
        df[c] = pd.to_datetime(df[c], errors="coerce")

# ---------- Gender normalization ----------
gender_col = None
for g in ["sex","gender"]:
    if has(df,g):
        gender_col = g; break

if gender_col:
    gmap = {"m":"M","male":"M","f":"F","female":"F","o":"O","other":"O","others":"O"}
    series = df[gender_col].astype(str).str.strip().str.lower()
    df[gender_col] = series.replace(gmap)
    df[gender_col] = df[gender_col].where(df[gender_col].isin(["M","F","O"]), "Unknown")

# ---------- Age cleanup + band ----------
if has(df,"age"):
    df["age"] = pd.to_numeric(df["age"], errors="coerce")
    df.loc[(df["age"] < 0) | (df["age"] > 120), "age"] = np.nan
    df["age_band"] = pd.cut(
        df["age"],
        bins=[0,12,18,30,45,60,75,120],
        labels=["0-12","13-18","19-30","31-45","46-60","61-75","76+"],
        right=True
    )

# ---------- Full name fallback ----------
if not has(df,"fullname") and (has(df,"firstname") or has(df,"first_name")):
    first = df["firstname"] if has(df,"firstname") else df.get("first_name")
    last = df["lastname"] if has(df,"lastname") else df.get("last_name")
    df["fullname"] = (first.fillna("") + " " + last.fillna("")).str.replace(r"\s+"," ",regex=True).str.strip()
elif has(df,"fullname"):
    df["fullname"] = df["fullname"].astype(str).str.strip()

# ---------- Membership flags ----------
for m in ["ismembershipactive","ismembershiptakendirectly"]:
    if has(df,m):
        df[m] = pd.to_numeric(df[m], errors="coerce").fillna(0).astype(int)
if has(df,"ismembershipactive"):
    df["membership_status"] = np.where(df["ismembershipactive"]==1, "Active", "Inactive")

# ---------- Deduplication ----------
key_cols = [k for k in ["patientid","patient_id","guid","patientguid"] if has(df,k)]
if key_cols:
    df = df.drop_duplicates(subset=key_cols, keep="first")
else:
    subset = [c for c in ["fullname","mobile","mobileno","phone","age","sex","gender"] if has(df,c)]
    df = df.drop_duplicates(subset=subset, keep="first") if subset else df.drop_duplicates()

# ---------- Missing handling (light touch) ----------
for c in df.columns:
    if df[c].dtype == "object" and not any(x in c for x in ["id","guid","code"]):
        df[c] = df[c].fillna("Unknown")

# ---------- Summaries ----------
missing = df.isna().sum().rename("missing_count").to_frame()
missing["missing_pct"] = (missing["missing_count"]/len(df)).round(4)

numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
desc = df[numeric_cols].describe().T if numeric_cols else pd.DataFrame()

# ---------- Visualizations (matplotlib only, no style/colors) ----------
def save_plot(fig_path):
    plt.tight_layout()
    plt.savefig(fig_path)
    plt.close()

if has(df,"age"):
    plt.figure()
    df["age"].dropna().plot(kind="hist", bins=20, title="Age Distribution")
    plt.xlabel("Age"); plt.ylabel("Count")
    save_plot(os.path.join(FIG_DIR,"age_distribution.png"))

if gender_col:
    plt.figure()
    df[gender_col].fillna("Unknown").value_counts().plot(kind="bar", title="Gender Distribution")
    plt.xlabel("Gender"); plt.ylabel("Count")
    save_plot(os.path.join(FIG_DIR,"gender_distribution.png"))

geo_label = "state" if has(df,"state") else ("state_name" if has(df,"state_name") else ("stateid" if has(df,"stateid") else None))
if geo_label:
    plt.figure()
    df[geo_label].fillna("Unknown").astype(str).value_counts().head(10).sort_values().plot(kind="barh", title="Top 10 States by Patient Count")
    plt.xlabel("Patients"); plt.ylabel("State")
    save_plot(os.path.join(FIG_DIR,"top_states.png"))

if has(df,"membership_status"):
    plt.figure()
    df["membership_status"].value_counts().plot(kind="pie", autopct="%1.1f%%", title="Membership Status", ylabel="")
    save_plot(os.path.join(FIG_DIR,"membership_status.png"))

if len(numeric_cols) >= 2:
    corr = df[numeric_cols].corr(numeric_only=True)
    plt.figure()
    plt.imshow(corr, aspect="auto")
    plt.title("Correlation Heatmap (Numeric Columns)")
    plt.colorbar()
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
    plt.yticks(range(len(corr.index)), corr.index)
    save_plot(os.path.join(FIG_DIR,"correlation_heatmap.png"))

# ---------- Export ----------
with pd.ExcelWriter(OUT_XLSX, engine="xlsxwriter") as w:
    df.to_excel(w, index=False, sheet_name="cleaned_data")
    missing.to_excel(w, sheet_name="missing_summary")
    if not desc.empty:
        desc.to_excel(w, sheet_name="numeric_summary")

missing.to_csv(OUT_SUMMARY)
print("Saved:", OUT_XLSX, OUT_SUMMARY, FIG_DIR)
