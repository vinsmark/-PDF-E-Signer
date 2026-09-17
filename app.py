# app.py

import base64
import hashlib
import io
from pathlib import Path

import fitz
import streamlit as st
import streamlit.components.v1 as components


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="PDF E-Signer",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# MINIMALIST UI
# ============================================================

st.markdown(
    """
    <style>

    :root {
        --black: #111111;
        --text: #16181c;
        --muted: #52565c;
        --border: #d6d6d6;
        --background: #f7f7f7;
        --white: #ffffff;
        --hover: #f2f2f2;
        --accent: #2451c9;
    }

    * {
        box-sizing: border-box;
    }

    html,
    body,
    [data-testid="stAppViewContainer"] {
        background: var(--background);
    }

    body {
        color: var(--text);
    }

    /* Remove Streamlit chrome */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"],
    .stDeployButton {
        display: none !important;
    }

    /* Main container */

    .block-container {
        max-width: 1450px !important;
        padding: 36px 42px 50px !important;
    }

    /* Header */

    .app-header {
        margin-bottom: 28px;
    }

    .app-title {
        color: #111111;
        font-size: 22px;
        line-height: 1.2;
        font-weight: 700;
        letter-spacing: -0.35px;
        margin: 0;
    }

    .app-subtitle {
        color: #52565c;
        font-size: 13px;
        margin-top: 7px;
    }

    /* ------------------------------------------------------
       PREVIEW CARD (left) — real container, styled via key
    ------------------------------------------------------ */

    .st-key-preview_card {
        background: #eeeeee !important;
        border: 1px solid var(--border) !important;
        border-radius: 7px !important;
        min-height: 720px;
        overflow: hidden;
    }

    .st-key-preview_card > div {
        min-height: 720px;
    }

    .preview-empty {
        min-height: 680px;
        display: flex;
        justify-content: center;
        align-items: center;
        color: #555555;
        font-size: 14px;
        font-weight: 500;
        text-align: center;
    }

    /* ------------------------------------------------------
       CONTROL CARD (right) — real container, styled via key
    ------------------------------------------------------ */

    .st-key-control_card {
        background: var(--white) !important;
        border: 1px solid var(--border) !important;
        border-radius: 7px !important;
        padding: 24px !important;
    }

    .control-title {
        font-size: 15px;
        font-weight: 700;
        color: #111111;
        margin-bottom: 16px;
    }

    .control-label {
        font-size: 13px;
        font-weight: 600;
        color: #111111;
        margin-bottom: 8px;
    }

    .file-name {
        font-size: 13px;
        font-weight: 500;
        color: #2c2f34;
        margin-top: 8px;
        word-break: break-word;
    }

    .file-size {
        font-size: 12px;
        color: #777777;
        margin-top: 3px;
    }

    .description {
        color: #52565c;
        font-size: 12.5px;
        font-weight: 500;
        line-height: 1.55;
        margin-top: 8px;
    }

    .divider {
        width: 100%;
        height: 1px;
        background: #e0e0e0;
        margin: 22px 0;
    }

    /* File uploader */

    [data-testid="stFileUploader"] {
        margin: 0 !important;
    }

    [data-testid="stFileUploader"] > label {
        display: none !important;
    }

    [data-testid="stFileUploaderDropzone"] {
        min-height: 88px !important;
        padding: 12px !important;
        border: 1px solid #cfcfcf !important;
        border-radius: 6px !important;
        background: #fafafa !important;
    }

    [data-testid="stFileUploaderDropzone"]:hover {
        border-color: #9a9a9a !important;
        background: #f5f5f5 !important;
    }

    [data-testid="stFileUploaderDropzoneInstructions"] {
        color: #4a4a4a !important;
        font-weight: 500 !important;
    }

    [data-testid="stFileUploaderDropzoneInstructions"] > div:first-child {
        font-size: 13px !important;
    }

    [data-testid="stFileUploaderDropzone"] svg {
        width: 17px !important;
        height: 17px !important;
    }

    /* Buttons */

    .stButton > button,
    .stDownloadButton > button {
        min-height: 46px !important;
        border-radius: 6px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        letter-spacing: 0.1px;
        box-shadow: none !important;
        transition: 0.15s ease;
    }

    .stButton > button {
        background: #111111 !important;
        color: #ffffff !important;
        border: 1px solid #111111 !important;
    }

    .stButton > button:hover {
        background: #303030 !important;
        border-color: #303030 !important;
    }

    .stButton > button:disabled {
        background: #ececec !important;
        color: #a0a0a0 !important;
        border-color: #dddddd !important;
    }

    .stDownloadButton > button {
        background: #ffffff !important;
        color: #111111 !important;
        border: 1.5px solid #111111 !important;
    }

    .stDownloadButton > button:hover {
        background: #111111 !important;
        color: #ffffff !important;
    }

    /* Page selector */

    .page-control {
        margin-top: 18px;
    }

    [data-testid="stNumberInput"] input {
        border-radius: 6px !important;
        border: 1px solid #b8b8b8 !important;
        background: white !important;
        color: #111111 !important;
        font-weight: 600 !important;
    }

    /* Status */

    .success-message {
        margin-top: 12px;
        padding: 10px 12px;
        border: 1px solid #c9c9c9;
        border-radius: 6px;
        background: #f2f2f2;
        font-size: 13px;
        font-weight: 500;
        color: #111111;
    }

    /* Mobile */

    @media (max-width: 950px) {

        .block-container {
            padding: 24px 18px 35px !important;
        }

        .st-key-preview_card {
            min-height: 560px;
        }

        .preview-empty {
            min-height: 520px;
        }

        .st-key-control_card {
            margin-top: 18px;
        }
    }

    @media (max-width: 600px) {

        .block-container {
            padding: 18px 12px 25px !important;
        }

        .app-header {
            margin-bottom: 18px;
        }

        .app-title {
            font-size: 20px;
        }

        .app-subtitle {
            font-size: 12px;
        }

        .st-key-preview_card {
            min-height: 450px;
            border-radius: 6px;
        }

        .preview-empty {
            min-height: 410px;
        }

        .st-key-control_card {
            padding: 18px !important;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "pdf_bytes": None,
    "pdf_name": None,
    "pdf_hash": None,

    "signature_bytes": None,
    "signature_name": None,

    "page_index": 0,

    "signature_position": {
        "x": 0.65,
        "y": 0.78,
        "w": 0.22,
        "h": 0.10,
    },

    "signature_token": 0,

    "signed_pdf": None,
    "signed_name": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="app-header">
        <div class="app-title">PDF E-Signer</div>
        <div class="app-subtitle">
            Sign your document directly in your browser.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# TWO-COLUMN WORKSPACE
# LEFT  = PDF PREVIEW
# RIGHT = CONTROLS
# ============================================================

left_column, right_column = st.columns(
    [3.3, 1],
    gap="large",
)


# ============================================================
# LEFT: PDF PREVIEW
# ============================================================

with left_column:

    # A real container (not a manually-closed <div>) so everything
    # placed inside it is actually grouped together and styled as
    # one card, instead of leaving an empty styled box behind.
    with st.container(border=True, key="preview_card"):

        if not st.session_state.pdf_bytes:

            st.markdown(
                """
                <div class="preview-empty">
                    Select a PDF document from the panel on the right.
                </div>
                """,
                unsafe_allow_html=True,
            )

        else:

            try:

                pdf_document = fitz.open(
                    stream=st.session_state.pdf_bytes,
                    filetype="pdf",
                )

                if pdf_document.needs_pass:

                    st.error(
                        "This PDF is password protected and cannot be opened."
                    )

                else:

                    page_count = len(pdf_document)

                    if page_count > 1:

                        selected_page = st.number_input(
                            "Page",
                            min_value=1,
                            max_value=page_count,
                            value=st.session_state.page_index + 1,
                            step=1,
                            label_visibility="collapsed",
                        )

                        st.session_state.page_index = selected_page - 1

                    else:

                        st.session_state.page_index = 0

                    page_index = st.session_state.page_index

                    page = pdf_document.load_page(page_index)

                    # Render PDF page
                    pixmap = page.get_pixmap(
                        matrix=fitz.Matrix(1.5, 1.5),
                        alpha=False,
                    )

                    png_bytes = pixmap.tobytes("png")

                    pdf_image = (
                        "data:image/png;base64,"
                        + base64.b64encode(png_bytes).decode("utf-8")
                    )

                    # Signature
                    signature_image = None

                    if st.session_state.signature_bytes:

                        signature_image = (
                            "data:image/png;base64,"
                            + base64.b64encode(
                                st.session_state.signature_bytes
                            ).decode("utf-8")
                        )

                    # Custom PDF editor
                    pdf_editor = components.declare_component(
                        "pdf_esigner",
                        path=str(
                            Path(__file__).parent / "frontend"
                        ),
                    )

                    result = pdf_editor(
                        pdf=pdf_image,
                        signature=signature_image,
                        position=st.session_state.signature_position,
                        token=st.session_state.signature_token,
                        key=f"pdf_editor_page_{page_index}",
                    )

                    if isinstance(result, dict):

                        if result.get("type") == "position":

                            st.session_state.signature_position = {
                                "x": float(
                                    result.get("x", 0.65)
                                ),

                                "y": float(
                                    result.get("y", 0.78)
                                ),

                                "w": float(
                                    result.get("w", 0.22)
                                ),

                                "h": float(
                                    result.get("h", 0.10)
                                ),
                            }

                    pdf_document.close()

            except Exception as error:

                st.error(
                    f"Unable to display the PDF: {error}"
                )


# ============================================================
# RIGHT: CONTROL PANEL
# ============================================================

with right_column:

    # Same fix here: a real container groups the title, uploader,
    # description and button together as one visible white card,
    # instead of leaving a separate empty card floating above them.
    with st.container(border=True, key="control_card"):

        # --------------------------------------------------------
        # PDF
        # --------------------------------------------------------

        st.markdown(
            '<div class="control-title">Document</div>',
            unsafe_allow_html=True,
        )

        pdf_file = st.file_uploader(
            "Select PDF",
            type=["pdf"],
            accept_multiple_files=False,
            key="pdf_upload",
            label_visibility="collapsed",
        )

        if pdf_file is not None:

            uploaded_pdf = pdf_file.getvalue()

            uploaded_hash = hashlib.sha256(
                uploaded_pdf
            ).hexdigest()

            if uploaded_hash != st.session_state.pdf_hash:

                st.session_state.pdf_bytes = uploaded_pdf
                st.session_state.pdf_name = pdf_file.name
                st.session_state.pdf_hash = uploaded_hash

                # Reset everything when a new PDF is selected
                st.session_state.page_index = 0

                st.session_state.signature_bytes = None
                st.session_state.signature_name = None

                st.session_state.signature_position = {
                    "x": 0.65,
                    "y": 0.78,
                    "w": 0.22,
                    "h": 0.10,
                }

                st.session_state.signature_token += 1

                st.session_state.signed_pdf = None
                st.session_state.signed_name = None

                st.rerun()

        if st.session_state.pdf_name:

            st.markdown(
                f"""
                <div class="file-name">
                    {st.session_state.pdf_name}
                </div>
                """,
                unsafe_allow_html=True,
            )

        # --------------------------------------------------------
        # Divider
        # --------------------------------------------------------

        st.markdown(
            '<div class="divider"></div>',
            unsafe_allow_html=True,
        )

        # --------------------------------------------------------
        # SIGNATURE
        # --------------------------------------------------------

        st.markdown(
            '<div class="control-title">Electronic signature</div>',
            unsafe_allow_html=True,
        )

        signature_file = st.file_uploader(
            "Select signature",
            type=["png", "jpg", "jpeg"],
            accept_multiple_files=False,
            key="signature_upload",
            label_visibility="collapsed",
        )

        if signature_file is not None:

            uploaded_signature = signature_file.getvalue()

            if uploaded_signature != st.session_state.signature_bytes:

                st.session_state.signature_bytes = uploaded_signature
                st.session_state.signature_name = (
                    signature_file.name
                )

                st.session_state.signature_token += 1

                st.session_state.signed_pdf = None
                st.session_state.signed_name = None

                st.rerun()

        if st.session_state.signature_name:

            st.markdown(
                f"""
                <div class="file-name">
                    {st.session_state.signature_name}
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            """
            <div class="description">
                Drag the signature on the document.
                Use the corner handle to resize it.
            </div>
            """,
            unsafe_allow_html=True,
        )

        # --------------------------------------------------------
        # Divider
        # --------------------------------------------------------

        st.markdown(
            '<div class="divider"></div>',
            unsafe_allow_html=True,
        )

        # --------------------------------------------------------
        # APPLY
        # --------------------------------------------------------

        can_apply = (
            st.session_state.pdf_bytes is not None
            and st.session_state.signature_bytes is not None
        )

        if st.button(
            "Apply signature",
            use_container_width=True,
            disabled=not can_apply,
        ):

            try:

                output_document = fitz.open(
                    stream=st.session_state.pdf_bytes,
                    filetype="pdf",
                )

                page_index = max(
                    0,
                    min(
                        st.session_state.page_index,
                        len(output_document) - 1,
                    ),
                )

                output_page = output_document.load_page(
                    page_index
                )

                # Current signature position
                position = (
                    st.session_state.signature_position
                )

                x = float(position.get("x", 0.65))
                y = float(position.get("y", 0.78))
                w = float(position.get("w", 0.22))
                h = float(position.get("h", 0.10))

                # Safety limits
                w = max(0.01, min(w, 1.0))
                h = max(0.01, min(h, 1.0))

                x = max(0.0, min(x, 1.0 - w))
                y = max(0.0, min(y, 1.0 - h))

                page_width = output_page.rect.width
                page_height = output_page.rect.height

                signature_rect = fitz.Rect(
                    x * page_width,
                    y * page_height,
                    (x + w) * page_width,
                    (y + h) * page_height,
                )

                # Insert signature
                output_page.insert_image(
                    signature_rect,
                    stream=st.session_state.signature_bytes,
                    keep_proportion=True,
                )

                # Save completely in memory
                output_buffer = io.BytesIO()

                output_document.save(
                    output_buffer,
                    garbage=4,
                    deflate=True,
                )

                output_document.close()

                st.session_state.signed_pdf = (
                    output_buffer.getvalue()
                )

                st.session_state.signed_name = (
                    Path(
                        st.session_state.pdf_name
                    ).stem
                    + "_signed.pdf"
                )

                st.rerun()

            except Exception as error:

                st.error(
                    f"Unable to apply the signature: {error}"
                )

        # --------------------------------------------------------
        # DOWNLOAD
        # --------------------------------------------------------

        if st.session_state.signed_pdf:

            st.markdown(
                '<div style="height:10px;"></div>',
                unsafe_allow_html=True,
            )

            st.download_button(
                "Download signed PDF",
                data=st.session_state.signed_pdf,
                file_name=st.session_state.signed_name,
                mime="application/pdf",
                use_container_width=True,
            )

            st.markdown(
                """
                <div class="success-message">
                    Your signed PDF is ready.
                </div>
                """,
                unsafe_allow_html=True,
            )