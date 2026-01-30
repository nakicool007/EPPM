# PPM Pro (Clarizen) attachments -> zip -> email
import os
import io
import json
import zipfile
import requests
from email.message import EmailMessage
import smtplib

PPM_USER = os.getenv("PPM_USER")
PPM_PASS = os.getenv("PPM_PASS")

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
MAIL_FROM = os.getenv("MAIL_FROM")
MAIL_TO = os.getenv("MAIL_TO")  # comma-separated

def ppm_login(user, password):
    # 1) Get server definition (data center)
    r = requests.post(
        "https://api.clarizen.com/v2.0/services/authentication/getServerDefinition",
        json={"userName": user, "password": password},
        timeout=60,
    )
    r.raise_for_status()
    server = r.json()["serverLocation"]

    # 2) Login on that server
    r = requests.post(
        f"{server}/authentication/login",
        json={"userName": user, "password": password},
        timeout=60,
    )
    r.raise_for_status()
    session_id = r.json()["sessionId"]

    headers = {"Authorization": f"Session {session_id}"}
    return server, headers

def data_query(server, headers, query, from_=0, limit=200):
    # TODO: confirm query payload format for your tenant (Clarizen REST v2)
    payload = {
        "query": query,
        "paging": {"from": from_, "limit": limit},
    }
    r = requests.post(f"{server}/data/query", json=payload, headers=headers, timeout=60)
    r.raise_for_status()
    return r.json()

def iter_projects(server, headers):
    # TODO: adjust fields and query syntax to your API guide
    # Example Clarizen query syntax is usually SQL-like:
    # "SELECT Id, Name FROM Project"
    query = "SELECT Id, Name FROM Project"
    from_ = 0
    limit = 200
    while True:
        result = data_query(server, headers, query, from_=from_, limit=limit)
        rows = result.get("entities", []) or result.get("data", [])
        if not rows:
            break
        for row in rows:
            yield row
        paging = result.get("paging") or {}
        if not paging.get("hasMore"):
            break
        from_ = paging.get("from", from_) + paging.get("limit", limit)

def iter_project_documents(server, headers, project_id):
    # TODO: replace with the correct attachment query for your tenant
    # Example idea: AttachmentLink between Project and Document.
    # You may need "AttachmentLink" or "Document" with a relation filter.
    query = f"SELECT Id, Name FROM Document WHERE Parent = '{project_id}'"
    result = data_query(server, headers, query, from_=0, limit=500)
    return result.get("entities", []) or result.get("data", [])

def download_document_bytes(server, headers, document_id):
    # TODO: confirm correct download method.
    # Clarizen REST API has a Files service (Upload/Download).
    # Some tenants use /services/files/Download with a JSON body containing documentId.
    r = requests.post(
        f"{server}/files/Download",
        json={"documentId": document_id},
        headers=headers,
        timeout=120,
        stream=True,
    )
    r.raise_for_status()
    return r.content

def build_zip(server, headers):
    zip_buf = io.BytesIO()
    with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for proj in iter_projects(server, headers):
            proj_id = proj.get("Id") or proj.get("id")
            proj_name = proj.get("Name") or proj.get("name") or proj_id
            if not proj_id:
                continue
            docs = iter_project_documents(server, headers, proj_id)
            for doc in docs:
                doc_id = doc.get("Id") or doc.get("id")
                doc_name = doc.get("Name") or doc.get("name") or doc_id
                if not doc_id:
                    continue
                content = download_document_bytes(server, headers, doc_id)
                safe_proj = "".join(c for c in proj_name if c not in r'<>:"/\\|?*')
                safe_doc = "".join(c for c in doc_name if c not in r'<>:"/\\|?*')
                zf.writestr(f"{safe_proj}/{safe_doc}", content)
    zip_buf.seek(0)
    return zip_buf

def send_email_with_zip(zip_buf, filename="ppm_pro_attachments.zip"):
    msg = EmailMessage()
    msg["From"] = MAIL_FROM
    msg["To"] = MAIL_TO
    msg["Subject"] = "PPM Pro project attachments"
    msg.set_content("Attached: all project attachments from PPM Pro.")

    msg.add_attachment(
        zip_buf.read(),
        maintype="application",
        subtype="zip",
        filename=filename,
    )

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
        s.starttls()
        s.login(SMTP_USER, SMTP_PASS)
        s.send_message(msg)

# ---- run ----
server, headers = ppm_login(PPM_USER, PPM_PASS)
zip_buf = build_zip(server, headers)
send_email_with_zip(zip_buf)
print("Done.")
