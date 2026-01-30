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

   
PPM Pro Project Attachment Extraction - README
Purpose:
This script (`PPM Pro Project Attachment Extraction.py`) logs into PPM Pro (Clarizen),
queries all projects, downloads project attachments, zips them, and emails the archive.
It is a template that requires tenant-specific query and download endpoints to be confirmed.
Prerequisites:
- Python 3.8+ recommended
- Required Python packages: `requests`
- Network access to your PPM Pro (Clarizen) REST API endpoint
Configuration (environment variables):
- PPM_USER / PPM_PASS: PPM Pro credentials
- SMTP_HOST / SMTP_PORT / SMTP_USER / SMTP_PASS: SMTP settings
- MAIL_FROM: sender email address
- MAIL_TO: recipient email(s), comma-separated
Key TODOs to finalize for your tenant:
- Update the project query in `iter_projects` if your API requires different fields or syntax.
- Replace the document query in `iter_project_documents` with the correct attachment lookup.
- Confirm the correct download endpoint and payload in `download_document_bytes`.
How to run:
1) Set the environment variables listed above.
2) Run the script:
   python "PPM Pro Project Attachment Extraction.py"
Notes & assumptions:
- The script uses the Clarizen REST v2 login flow (getServerDefinition -> login).
- Large attachment sets may exceed typical email size limits; consider splitting or using
  a file share if needed.


Contact:
For questions or changes, update the notebook or contact the project owner.
