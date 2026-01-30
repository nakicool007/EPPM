EPPM Automation - README

Contents:
- RES25_Generation.ipynb
- PPM Pro Project Attachment Extraction.py
- readme.txt (this file)

------------------------------------------------------------

RES25_Generation.ipynb

Purpose:
Prepares and computes RES25 resource totals and costs by merging new, previous, and archived
resource spreadsheets, mapping anonymized IDs, computing categories, zeroing future weeks
according to rules, and recalculating totals and costs.

Required input files (place next to the notebook):
- RES25_new.xlsx (sheet: Main)
- Previous.xlsx (sheet: Main)
- ETO_Archived_Resource_List.xlsx
- ETO_Resource_Portfolio.xlsx

Prerequisites:
- Python 3.8+ recommended
- Jupyter Notebook or JupyterLab
- Python packages: pandas, openpyxl

How to run:
1) Open RES25_Generation.ipynb in Jupyter and run cells top-to-bottom.
2) Ensure the input Excel files above are in the same folder (or update paths in the notebook).

Notes:
- The notebook expects columns like ResourceName, WorkdayID, AnonymizedName, RealName,
  TS Status, Effort Type, and week columns prefixed with FY.
- Update current_week_col (example: FY2026_WK12) and date-based rules as needed.

------------------------------------------------------------

PPM Pro Project Attachment Extraction.py

Purpose:
Logs into PPM Pro (Clarizen), queries all projects, downloads project attachments, zips them,
and emails the archive. This is a template that requires tenant-specific query and download
endpoints to be confirmed.

Prerequisites:
- Python 3.8+ recommended
- Python package: requests
- Network access to your PPM Pro (Clarizen) REST API endpoint

Configuration (environment variables):
- PPM_USER / PPM_PASS: PPM Pro credentials
- SMTP_HOST / SMTP_PORT / SMTP_USER / SMTP_PASS: SMTP settings
- MAIL_FROM: sender email address
- MAIL_TO: recipient email(s), comma-separated

Key TODOs to finalize for your tenant:
- Update the project query in iter_projects if your API requires different fields or syntax.
- Replace the document query in iter_project_documents with the correct attachment lookup.
- Confirm the correct download endpoint and payload in download_document_bytes.

How to run:
1) Set the environment variables listed above.
2) Run the script:
   python "PPM Pro Project Attachment Extraction.py"

Notes:
- The script uses the Clarizen REST v2 login flow (getServerDefinition -> login).
- Large attachment sets may exceed typical email size limits; consider splitting or using
  a file share if needed.

------------------------------------------------------------

readme.txt

Purpose:
Describes the contents of this folder and how to run the included automation artifacts.

