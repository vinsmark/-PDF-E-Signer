# Local PDF E-Signer for Streamlit

## What it does

1. Select a PDF.
2. Select one or more e-signature images.
3. Select the PDF page.
4. Drag the selected signature to the desired location.
5. Optionally resize it using the blue handle.
6. Click **Apply & Prepare PDF**.
7. Download the signed PDF.

## Storage behavior

This project does **not** use:
- a database
- SQLite
- a cloud storage bucket
- permanent server-side file saving

The uploaded PDF/signature and generated PDF are kept in Streamlit/Python memory for the active session.

Important: if deployed on Streamlit Cloud or another hosted Streamlit server, the PDF still travels to that server for PyMuPDF processing. It is not persistent storage, but it is not strictly browser-only processing.

## Run locally

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt

streamlit run app.py
```

Then open the local URL shown by Streamlit, normally:
`http://localhost:8501`

## Deploy to Streamlit Community Cloud

Push these files to GitHub:

```text
pdf-esigner/
├── app.py
├── requirements.txt
└── frontend/
    └── index.html
```

In Streamlit Community Cloud, select the repository and set the main file to:

```text
app.py
```

No secrets are required.

## Notes

Use a transparent PNG for the signature when possible. JPG signatures normally have a white background.

For very large PDFs, the page preview is rendered in memory, so memory usage can increase during editing.
