import streamlit as st
from pathlib import Path
import os

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="File Manager",
    page_icon="🗂️",
    layout="wide",
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Syne:wght@400;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: #0e0e0e;
    color: #f0f0f0;
}

.stApp { background-color: #0e0e0e; }

h1, h2, h3 { font-family: 'Syne', sans-serif; font-weight: 800; }

.title-block {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border: 1px solid #e94560;
    border-radius: 12px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
}
.title-block h1 { color: #e94560; font-size: 2.5rem; margin: 0; letter-spacing: -1px; }
.title-block p  { color: #a0a0b0; margin: 0.4rem 0 0; font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; }

.file-card {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 8px;
    padding: 0.6rem 1rem;
    margin: 0.25rem 0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    color: #c8c8d8;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.file-card.folder { border-left: 3px solid #f5a623; color: #f5a623; }
.file-card.file   { border-left: 3px solid #4ecdc4; }

.section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 2px;
    color: #e94560;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

.success-msg { color: #4ecdc4; font-weight: 700; }
.error-msg   { color: #e94560; font-weight: 700; }
.warn-msg    { color: #f5a623; font-weight: 700; }

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #111111 !important;
    border-right: 1px solid #2a2a2a;
}
[data-testid="stSidebar"] .stRadio label { font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; }

/* Inputs */
input, textarea {
    background-color: #1a1a1a !important;
    color: #f0f0f0 !important;
    border: 1px solid #333 !important;
    font-family: 'JetBrains Mono', monospace !important;
    border-radius: 6px !important;
}

/* Buttons */
.stButton > button {
    background: #e94560;
    color: #fff;
    border: none;
    border-radius: 6px;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    padding: 0.5rem 1.5rem;
    transition: background 0.2s;
}
.stButton > button:hover { background: #c73652; }

/* Divider */
hr { border-color: #2a2a2a; }

/* Radio buttons */
div[data-testid="stRadio"] > label { color: #a0a0b0; }
</style>
""", unsafe_allow_html=True)


# ─── Helpers ───────────────────────────────────────────────────────────────────
def get_all_items():
    p = Path('')
    return sorted(p.rglob('*'))

def render_file_tree():
    items = get_all_items()
    if not items:
        st.markdown('<div class="file-card">📭 No files or folders found</div>', unsafe_allow_html=True)
        return
    for item in items:
        if item.is_dir():
            st.markdown(f'<div class="file-card folder">📁 {item}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="file-card file">📄 {item}</div>', unsafe_allow_html=True)

def msg(text, kind="success"):
    css = {"success": "success-msg", "error": "error-msg", "warn": "warn-msg"}
    st.markdown(f'<p class="{css.get(kind, "success-msg")}">{text}</p>', unsafe_allow_html=True)


# ─── Title ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="title-block">
  <h1>🗂️ File Manager</h1>
  <p>CRUD operations · files & folders · powered by pathlib</p>
</div>
""", unsafe_allow_html=True)

col_sidebar, col_main = st.columns([1, 3])

# ─── Sidebar / Operation Selector ──────────────────────────────────────────────
with col_sidebar:
    st.markdown('<div class="section-label">Operations</div>', unsafe_allow_html=True)
    operation = st.radio("", [
        "📄 Create File",
        "👁️ Read File",
        "✏️ Update File",
        "🗑️ Delete File",
        "🔤 Rename File",
        "📁 Create Folder",
        "❌ Delete Folder",
        "📁➕ Create File in Folder",
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown('<div class="section-label">Explorer</div>', unsafe_allow_html=True)
    render_file_tree()


# ─── Main Panel ────────────────────────────────────────────────────────────────
with col_main:

    # ── 1. Create File ──────────────────────────────────────────────────────────
    if operation == "📄 Create File":
        st.subheader("Create a New File")
        file_name = st.text_input("File name (e.g. notes.txt)")
        content   = st.text_area("File content", height=150)
        if st.button("Create File"):
            if not file_name:
                msg("⚠️ Please enter a file name.", "warn")
            else:
                p = Path(file_name)
                if p.exists():
                    msg("⚠️ File already exists!", "warn")
                else:
                    try:
                        p.parent.mkdir(parents=True, exist_ok=True)
                        p.write_text(content)
                        msg(f"✅ '{file_name}' created successfully!")
                        st.rerun()
                    except Exception as e:
                        msg(f"❌ Error: {e}", "error")

    # ── 2. Read File ────────────────────────────────────────────────────────────
    elif operation == "👁️ Read File":
        st.subheader("Read a File")
        items = [str(i) for i in get_all_items() if Path(i).is_file()]
        if not items:
            msg("No files available.", "warn")
        else:
            file_name = st.selectbox("Select file to read", items)
            if st.button("Read File"):
                try:
                    content = Path(file_name).read_text()
                    st.markdown('<div class="section-label">Content</div>', unsafe_allow_html=True)
                    st.code(content if content else "(empty file)", language="text")
                except Exception as e:
                    msg(f"❌ Error: {e}", "error")

    # ── 3. Update File ──────────────────────────────────────────────────────────
    elif operation == "✏️ Update File":
        st.subheader("Update a File")
        items = [str(i) for i in get_all_items() if Path(i).is_file()]
        if not items:
            msg("No files available.", "warn")
        else:
            file_name  = st.selectbox("Select file to update", items)
            update_mode = st.radio("Update mode", ["Overwrite", "Append"], horizontal=True)
            new_content = st.text_area("New content", height=150)
            if st.button("Update File"):
                try:
                    mode = 'w' if update_mode == "Overwrite" else 'a'
                    with open(file_name, mode) as f:
                        f.write(new_content)
                    msg(f"✅ '{file_name}' updated ({update_mode.lower()})!")
                    st.rerun()
                except Exception as e:
                    msg(f"❌ Error: {e}", "error")

    # ── 4. Delete File ──────────────────────────────────────────────────────────
    elif operation == "🗑️ Delete File":
        st.subheader("Delete a File")
        items = [str(i) for i in get_all_items() if Path(i).is_file()]
        if not items:
            msg("No files available.", "warn")
        else:
            file_name = st.selectbox("Select file to delete", items)
            st.warning(f"⚠️ This will permanently delete **{file_name}**.")
            if st.button("Delete File", type="primary"):
                try:
                    os.remove(file_name)
                    msg(f"🗑️ '{file_name}' deleted.")
                    st.rerun()
                except Exception as e:
                    msg(f"❌ Error: {e}", "error")

    # ── 5. Rename File ──────────────────────────────────────────────────────────
    elif operation == "🔤 Rename File":
        st.subheader("Rename a File")
        items = [str(i) for i in get_all_items() if Path(i).is_file()]
        if not items:
            msg("No files available.", "warn")
        else:
            file_name = st.selectbox("Select file to rename", items)
            new_name  = st.text_input("New file name")
            if st.button("Rename File"):
                if not new_name:
                    msg("⚠️ Enter a new name.", "warn")
                else:
                    try:
                        Path(file_name).rename(new_name)
                        msg(f"✅ Renamed to '{new_name}'!")
                        st.rerun()
                    except Exception as e:
                        msg(f"❌ Error: {e}", "error")

    # ── 6. Create Folder ────────────────────────────────────────────────────────
    elif operation == "📁 Create Folder":
        st.subheader("Create a New Folder")
        folder_name = st.text_input("Folder name")
        if st.button("Create Folder"):
            if not folder_name:
                msg("⚠️ Enter a folder name.", "warn")
            else:
                p = Path(folder_name)
                if p.exists():
                    msg("⚠️ Folder already exists!", "warn")
                else:
                    try:
                        p.mkdir(parents=True)
                        msg(f"✅ Folder '{folder_name}' created!")
                        st.rerun()
                    except Exception as e:
                        msg(f"❌ Error: {e}", "error")

    # ── 7. Delete Folder ────────────────────────────────────────────────────────
    elif operation == "❌ Delete Folder":
        st.subheader("Delete a Folder")
        items = [str(i) for i in get_all_items() if Path(i).is_dir()]
        if not items:
            msg("No folders available.", "warn")
        else:
            folder_name = st.selectbox("Select folder to delete", items)
            st.warning(f"⚠️ Folder must be **empty** to delete. This will permanently remove **{folder_name}**.")
            if st.button("Delete Folder", type="primary"):
                try:
                    Path(folder_name).rmdir()
                    msg(f"🗑️ Folder '{folder_name}' deleted.")
                    st.rerun()
                except Exception as e:
                    msg(f"❌ Error: {e}", "error")

    # ── 8. Create File in Folder ────────────────────────────────────────────────
    elif operation == "📁➕ Create File in Folder":
        st.subheader("Create a File inside a Folder")
        folders = [str(i) for i in get_all_items() if Path(i).is_dir()]

        tab1, tab2 = st.tabs(["Use existing folder", "Create new folder"])

        with tab1:
            if not folders:
                msg("No folders yet. Create one first or use the other tab.", "warn")
            else:
                folder_name = st.selectbox("Select folder", folders)
                file_name   = st.text_input("File name", key="exist_fn")
                content     = st.text_area("File content", height=120, key="exist_fc")
                if st.button("Create File", key="exist_btn"):
                    if not file_name:
                        msg("⚠️ Enter a file name.", "warn")
                    else:
                        p = Path(folder_name) / file_name
                        if p.exists():
                            msg("⚠️ File already exists!", "warn")
                        else:
                            try:
                                p.write_text(content)
                                msg(f"✅ '{p}' created!")
                                st.rerun()
                            except Exception as e:
                                msg(f"❌ Error: {e}", "error")

        with tab2:
            folder_name = st.text_input("New folder name", key="new_folder")
            file_name   = st.text_input("File name", key="new_fn")
            content     = st.text_area("File content", height=120, key="new_fc")
            if st.button("Create Folder + File", key="new_btn"):
                if not folder_name or not file_name:
                    msg("⚠️ Enter both folder and file names.", "warn")
                else:
                    p = Path(folder_name) / file_name
                    if p.exists():
                        msg("⚠️ File already exists!", "warn")
                    else:
                        try:
                            p.parent.mkdir(parents=True, exist_ok=True)
                            p.write_text(content)
                            msg(f"✅ '{p}' created!")
                            st.rerun()
                        except Exception as e:
                            msg(f"❌ Error: {e}", "error")