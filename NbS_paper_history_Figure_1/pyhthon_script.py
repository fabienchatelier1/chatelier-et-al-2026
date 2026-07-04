r"""
Title  : Merge multiple Excel exports and plot yearly publication counts
Input  : A folder containing Excel files named like "savedrecs.xls", "savedrecs (1).xls", ...; each file has a column "Publication Year"
Output : (1) A pandas DataFrame of yearly counts (Year, Count) filtered to Year >= 1990 and excluding 2026
         (2) A bar chart with an overlaid line of the same counts
Method: 1) Find all matching Excel files in the folder.
        2) Read each file into a DataFrame and concatenate them row-wise.
        3) Count publications per year from the "Publication Year" column.
        4) Filter years (>= 1990) and remove year 2026.
        5) Plot bars, then overlay a line using the same counts, and add a dotted grid.
Author : Amir Rouhani
Date   : 2025-08-05
Email  : amir.rouhani@ufz.de
"""

from pathlib import Path
import re

import pandas as pd
import matplotlib.pyplot as plt


# ----------------------------
# 1) Locate and read all files
# ----------------------------
folder = Path("./NbS_51274")

# Matches: savedrecs.xls, savedrecs (1).xls, savedrecs (2).xls, ...
pattern = re.compile(r"^savedrecs(?: \(\d+\))?\.xls$", re.IGNORECASE)

excel_files = sorted([p for p in folder.iterdir() if p.is_file() and pattern.match(p.name)])

if not excel_files:
    raise FileNotFoundError(
        f"No Excel files found in: {folder}\n"
        "Expected names like: savedrecs.xls, savedrecs (1).xls, ..."
    )

dfs = []
for f in excel_files:
    df = pd.read_excel(f)
    dfs.append(df)

NbS_all = pd.concat(dfs, ignore_index=True)


# -----------------------------------------
# 2) Count publications per year (same data)
# -----------------------------------------
year_col = "Publication Year"
if year_col not in NbS_all.columns:
    raise KeyError(
        f'Column "{year_col}" not found. Available columns include:\n{list(NbS_all.columns)}'
    )

NbS_all_date = (
    NbS_all[[year_col]]
    .dropna()
    .assign(**{year_col: pd.to_numeric(NbS_all[year_col], errors="coerce")})
    .dropna()
)

NbS_all_date = (
    NbS_all_date[year_col]
    .astype(int)
    .value_counts()
    .sort_index()
    .rename_axis("Year")
    .reset_index(name="Count")
)

NbS_all_date_above_1990 = NbS_all_date.query("Year >= 1990 and Year != 2026").copy()


# ----------------------------
# 3) Plot (bar + line overlay)
# ----------------------------
x = NbS_all_date_above_1990["Year"].astype(str).tolist()
y = NbS_all_date_above_1990["Count"].tolist()

fig, ax = plt.subplots(figsize=(12, 6))

# Bars
bar_positions = range(len(x))
ax.bar(
    bar_positions,
    y,
    edgecolor="none",
    alpha=1,
    color="#4c92c3"
)

# Overlay line (same midpoints as bars)
# ax.plot(
#     list(bar_positions),
#     y,
#     marker="o",
#     linewidth=2,
#     color="#ba171c",   # Line colour (e.g. "black", "red", "#1f77b4")
#     alpha=0.8        # Opacity: 0 = fully transparent, 1 = fully opaque
# )

ax.set_xlabel("Publication Year")
ax.set_ylabel("Numbers of publication")
ax.set_title("Numbers of publication on Nature-based solutions per year")

# Match the R-style rotated year labels
ax.set_xticks(list(bar_positions))
ax.set_xticklabels(x, rotation=90)

# Similar limits to your R code (adjust as you like)
ax.set_ylim(0, 6000)

# If you really want an x-range like xlim=c(1,45) in R, that is about visible span.
# Here we set the visible index window. Comment this out if you want all years shown.
ax.set_xlim(-0.5, 35.5)

# Dotted gridlines in black (like lty="dotted", col="black")
ax.grid(False)

plt.tight_layout()
plt.savefig('publication_per_year_bar.png', dpi = 700)
# plt.show()
