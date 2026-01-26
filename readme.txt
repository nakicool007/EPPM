RES25_Generation - README

Purpose:
This notebook (`RES25_Generation.ipynb`) prepares and computes RES25 resource totals and costs
by merging new, previous, and archived resource spreadsheets, mapping anonymized IDs,
computing categories, zeroing future weeks according to rules, and recalculating totals/costs.

Required input files (place next to the notebook):
- RES25_new.xlsx (sheet: Main)
- Previous.xlsx (sheet: Main)
- ETO_Archived_Resource_List.xlsx
- ETO_Resource_Portfolio.xlsx

Prerequisites:
- Python 3.8+ recommended
- Jupyter Notebook or JupyterLab
- Required Python packages: `pandas`, `openpyxl` (for Excel IO)

Quick setup (example):
1) Create a virtual environment (optional):
   python -m venv .venv
   .\.venv\Scripts\activate
2) Install packages:
   pip install pandas openpyxl

How to run:
- Open `RES25_Generation.ipynb` in Jupyter and run cells top-to-bottom.
- Ensure the input Excel files named above are available in the same folder (or update paths in the notebook).

Notes & assumptions:
- The notebook uses `pandas.read_excel` and expects columns such as `ResourceName`, `WorkdayID`,
  `AnonymizedName`, `RealName`, `TS Status`, `Effort Type`, week columns prefixed like `FY...`.
- Adjust `current_week_col` (e.g., `FY2026_WK12`) and date-based rules in the notebook as required.

If you want a reproducible install list, create a `requirements.txt` with:
   pandas
   openpyxl

Contact:
For questions or changes, update the notebook or contact the project owner.
