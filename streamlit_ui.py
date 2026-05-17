import streamlit as st
from pathlib import Path
import os
import shutil

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

.folder-contents-card {
    background: #141414;
    border: 1px solid #2a2a2a;
    border-left: 3px solid #a78bfa;
    border-radius: 8px;
    padding: 0.6rem 1rem;
    margin: 0.2rem 0 0.2rem 1.5rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.80rem;
    color: #c8c8d8;
}

.folder-stats {
    background: #1a1a2e;
    border: 1px solid #2a2a4e;
    border-radius: 8px;
    padding: 1rem 1.5rem;
    margin-bottom: 1rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    color: #a0a0b0;
}
.folder-stats span { color: #a78bfa; font-weight: 700; }

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

def get_folder_size(folder: Path) -> int:
    """Return total size in bytes of all files inside a folder."""
    return sum(f.stat().st_size for f in folder.rglob('*') if f.is_file())

def format_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 ** 2:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 ** 2):.2f} MB"


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
        "👁️‍🗨️ Read Folder",
        "📝 Update Folder",
        "🔤 Rename Folder",
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

    # ── 7. Read Folder ──────────────────────────────────────────────────────────
    elif operation == "👁️‍🗨️ Read Folder":
        st.subheader("Read a Folder")
        folders = [str(i) for i in get_all_items() if Path(i).is_dir()]
        if not folders:
            msg("No folders available.", "warn")
        else:
            folder_name = st.selectbox("Select folder to inspect", folders)
            if st.button("Read Folder"):
                try:
                    folder_path = Path(folder_name)
                    all_contents = list(folder_path.rglob('*'))
                    direct_contents = list(folder_path.iterdir())
                    sub_dirs  = [x for x in direct_contents if x.is_dir()]
                    files     = [x for x in direct_contents if x.is_file()]
                    total_size = get_folder_size(folder_path)

                    # Stats panel
                    st.markdown(
                        f'<div class="folder-stats">'
                        f'📁 <span>{folder_name}</span> &nbsp;|&nbsp; '
                        f'Direct items: <span>{len(direct_contents)}</span> &nbsp;|&nbsp; '
                        f'Sub-folders: <span>{len(sub_dirs)}</span> &nbsp;|&nbsp; '
                        f'Files: <span>{len(files)}</span> &nbsp;|&nbsp; '
                        f'Total size: <span>{format_size(total_size)}</span>'
                        f'</div>',
                        unsafe_allow_html=True
                    )

                    st.markdown('<div class="section-label">Direct Contents</div>', unsafe_allow_html=True)

                    if not direct_contents:
                        st.markdown('<div class="file-card">📭 Folder is empty</div>', unsafe_allow_html=True)
                    else:
                        for item in sorted(direct_contents):
                            if item.is_dir():
                                # Show sub-folder and its children
                                sub_items = list(item.iterdir())
                                label = f"📁 {item.name}/ &nbsp; <span style='color:#666;font-size:0.75rem'>({len(sub_items)} item{'s' if len(sub_items)!=1 else ''})</span>"
                                st.markdown(f'<div class="file-card folder">{label}</div>', unsafe_allow_html=True)
                                for sub in sorted(sub_items)[:10]:
                                    icon = "📁" if sub.is_dir() else "📄"
                                    size_str = format_size(sub.stat().st_size) if sub.is_file() else ""
                                    st.markdown(
                                        f'<div class="folder-contents-card">{icon} {sub.name}'
                                        f'{"&nbsp;<span style=\'color:#666\'>(" + size_str + ")</span>" if size_str else ""}'
                                        f'</div>',
                                        unsafe_allow_html=True
                                    )
                                if len(sub_items) > 10:
                                    st.markdown(
                                        f'<div class="folder-contents-card" style="color:#666;">… and {len(sub_items)-10} more</div>',
                                        unsafe_allow_html=True
                                    )
                            else:
                                size_str = format_size(item.stat().st_size)
                                st.markdown(
                                    f'<div class="file-card file">📄 {item.name} &nbsp; '
                                    f'<span style="color:#666;font-size:0.75rem">({size_str})</span></div>',
                                    unsafe_allow_html=True
                                )

                    # Recursive summary
                    if all_contents:
                        all_files = [x for x in all_contents if x.is_file()]
                        if all_files:
                            st.markdown('<div class="section-label" style="margin-top:1.2rem;">All Files (Recursive)</div>', unsafe_allow_html=True)
                            for f in sorted(all_files):
                                rel = f.relative_to(folder_path)
                                size_str = format_size(f.stat().st_size)
                                st.markdown(
                                    f'<div class="file-card file">📄 {rel} &nbsp;'
                                    f'<span style="color:#666;font-size:0.75rem">({size_str})</span></div>',
                                    unsafe_allow_html=True
                                )

                except Exception as e:
                    msg(f"❌ Error: {e}", "error")

    # ── 8. Update Folder ────────────────────────────────────────────────────────
    elif operation == "📝 Update Folder":
        st.subheader("Update a Folder")
        st.caption("Move files into or out of a folder, or add a new sub-folder inside it.")

        folders = [str(i) for i in get_all_items() if Path(i).is_dir()]
        if not folders:
            msg("No folders available.", "warn")
        else:
            folder_name = st.selectbox("Select target folder", folders)
            tab1, tab2, tab3 = st.tabs(["➕ Add Sub-folder", "📥 Move File Into Folder", "📤 Move File Out of Folder"])

            # Tab 1 — Add sub-folder
            with tab1:
                sub_name = st.text_input("Sub-folder name", key="sub_name")
                if st.button("Create Sub-folder", key="create_sub"):
                    if not sub_name:
                        msg("⚠️ Enter a sub-folder name.", "warn")
                    else:
                        p = Path(folder_name) / sub_name
                        if p.exists():
                            msg("⚠️ Sub-folder already exists!", "warn")
                        else:
                            try:
                                p.mkdir(parents=True)
                                msg(f"✅ Sub-folder '{p}' created!")
                                st.rerun()
                            except Exception as e:
                                msg(f"❌ Error: {e}", "error")

            # Tab 2 — Move a file INTO the folder
            with tab2:
                all_files = [str(i) for i in get_all_items() if Path(i).is_file() and Path(i).parent != Path(folder_name)]
                if not all_files:
                    msg("No files outside this folder to move in.", "warn")
                else:
                    file_to_move = st.selectbox("Select file to move in", all_files, key="move_in_file")
                    if st.button("Move File In", key="move_in_btn"):
                        try:
                            src = Path(file_to_move)
                            dst = Path(folder_name) / src.name
                            if dst.exists():
                                msg(f"⚠️ '{dst}' already exists in the folder!", "warn")
                            else:
                                shutil.move(str(src), str(dst))
                                msg(f"✅ '{src.name}' moved into '{folder_name}'!")
                                st.rerun()
                        except Exception as e:
                            msg(f"❌ Error: {e}", "error")

            # Tab 3 — Move a file OUT of the folder
            with tab3:
                inside_files = [str(i) for i in get_all_items()
                                if Path(i).is_file() and str(Path(i)).startswith(folder_name + os.sep)]
                if not inside_files:
                    msg("No files inside this folder to move out.", "warn")
                else:
                    file_to_move = st.selectbox("Select file to move out", inside_files, key="move_out_file")
                    dest_dir = st.text_input("Destination path (leave blank for current directory)", key="move_out_dest")
                    if st.button("Move File Out", key="move_out_btn"):
                        try:
                            src = Path(file_to_move)
                            dst_folder = Path(dest_dir) if dest_dir.strip() else Path('')
                            dst = dst_folder / src.name
                            if dst.exists():
                                msg(f"⚠️ '{dst}' already exists at destination!", "warn")
                            else:
                                shutil.move(str(src), str(dst))
                                msg(f"✅ '{src.name}' moved to '{dst_folder or '.'}'!")
                                st.rerun()
                        except Exception as e:
                            msg(f"❌ Error: {e}", "error")

    # ── 9. Rename Folder ────────────────────────────────────────────────────────
    elif operation == "🔤 Rename Folder":
        st.subheader("Rename a Folder")
        folders = [str(i) for i in get_all_items() if Path(i).is_dir()]
        if not folders:
            msg("No folders available.", "warn")
        else:
            folder_name = st.selectbox("Select folder to rename", folders)
            new_name    = st.text_input("New folder name")
            st.info("ℹ️ The folder will be renamed in place. All contents are preserved.")
            if st.button("Rename Folder"):
                if not new_name:
                    msg("⚠️ Enter a new name.", "warn")
                elif new_name == folder_name:
                    msg("⚠️ New name is the same as the current name.", "warn")
                else:
                    src = Path(folder_name)
                    # Rename within the same parent directory
                    dst = src.parent / new_name
                    if dst.exists():
                        msg(f"⚠️ A folder named '{new_name}' already exists!", "warn")
                    else:
                        try:
                            src.rename(dst)
                            msg(f"✅ Folder renamed from '{folder_name}' to '{new_name}'!")
                            st.rerun()
                        except Exception as e:
                            msg(f"❌ Error: {e}", "error")

    # ── 10. Delete Folder ────────────────────────────────────────────────────────
    elif operation == "❌ Delete Folder":
        st.subheader("Delete a Folder")
        items = [str(i) for i in get_all_items() if Path(i).is_dir()]
        if not items:
            msg("No folders available.", "warn")
        else:
            folder_name  = st.selectbox("Select folder to delete", items)
            delete_mode  = st.radio(
                "Delete mode",
                ["Empty folders only", "Force delete (including all contents)"],
                horizontal=True
            )
            if delete_mode == "Empty folders only":
                st.warning(f"⚠️ Folder must be **empty** to delete. This will permanently remove **{folder_name}**.")
            else:
                st.error(f"🚨 This will permanently delete **{folder_name}** and ALL its contents!")

            if st.button("Delete Folder", type="primary"):
                try:
                    if delete_mode == "Empty folders only":
                        Path(folder_name).rmdir()
                    else:
                        shutil.rmtree(folder_name)
                    msg(f"🗑️ Folder '{folder_name}' deleted.")
                    st.rerun()
                except Exception as e:
                    msg(f"❌ Error: {e}", "error")

    # ── 11. Create File in Folder ────────────────────────────────────────────────
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