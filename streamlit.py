import streamlit as st
from pathlib import Path
import os
import shutil

st.set_page_config(
    page_title="FileOS",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:ital,wght@0,300;0,400;0,500;1,400&family=Outfit:wght@300;400;500;600;700&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"], .stApp {
    font-family: 'Outfit', sans-serif;
    background: #07080f !important;
    color: #e2e8f4;
}

/* ── Animated grid background ── */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(99,179,237,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(99,179,237,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1117 0%, #0a0e18 100%) !important;
    border-right: 1px solid rgba(99,179,237,0.12) !important;
    padding-top: 0 !important;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 0; }
[data-testid="stSidebar"] .stRadio { margin-top: 0.25rem; }
[data-testid="stSidebar"] .stRadio label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.78rem !important;
    color: #7a8ba6 !important;
    letter-spacing: 0.3px;
    padding: 0.15rem 0;
}
[data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] p { display: none; }

/* ── Main content area ── */
section[data-testid="stMain"] > div { padding: 1.5rem 2rem 2rem; position: relative; z-index: 1; }

/* ── Title / Header ── */
.os-header {
    display: flex;
    align-items: center;
    gap: 1.25rem;
    padding: 1.5rem 2rem;
    background: linear-gradient(135deg, rgba(13,20,40,0.95) 0%, rgba(10,14,30,0.95) 100%);
    border: 1px solid rgba(99,179,237,0.15);
    border-radius: 16px;
    margin-bottom: 1.75rem;
    backdrop-filter: blur(12px);
    position: relative;
    overflow: hidden;
}
.os-header::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99,179,237,0.4), rgba(167,139,250,0.4), transparent);
}
.os-logo {
    width: 48px; height: 48px;
    background: linear-gradient(135deg, #1a4a7a, #3b1d6e);
    border-radius: 12px;
    border: 1px solid rgba(99,179,237,0.3);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.4rem;
    flex-shrink: 0;
}
.os-title { flex: 1; }
.os-title h1 {
    font-family: 'Outfit', sans-serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: #e2e8f4;
    letter-spacing: -0.5px;
    line-height: 1.2;
}
.os-title p {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: #4a6080;
    margin-top: 0.2rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}
.os-badge {
    background: rgba(99,179,237,0.1);
    border: 1px solid rgba(99,179,237,0.2);
    border-radius: 8px;
    padding: 0.4rem 0.85rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    color: #63b3ed;
    letter-spacing: 1px;
}

/* ── Section labels ── */
.sec-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 2.5px;
    color: #3d5a80;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
    padding-left: 2px;
}

/* ── File tree cards ── */
.tree-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 0.45rem 0.75rem;
    border-radius: 8px;
    margin: 2px 0;
    font-family: 'DM Mono', monospace;
    font-size: 0.73rem;
    transition: background 0.15s;
    cursor: default;
    border: 1px solid transparent;
}
.tree-item:hover { background: rgba(99,179,237,0.06); border-color: rgba(99,179,237,0.1); }
.tree-item.is-folder { color: #f6ad55; }
.tree-item.is-folder .tree-dot { background: #f6ad55; }
.tree-item.is-file   { color: #76e4f7; }
.tree-item.is-file .tree-dot   { background: #76e4f7; }
.tree-dot {
    width: 5px; height: 5px;
    border-radius: 50%;
    flex-shrink: 0;
}

/* ── Sidebar ops menu label ── */
.ops-header {
    background: linear-gradient(135deg, #0d1117, #0a0e18);
    border-bottom: 1px solid rgba(99,179,237,0.1);
    padding: 1.2rem 1rem 1rem;
    margin-bottom: 0.5rem;
}
.ops-header .logo-row {
    display: flex; align-items: center; gap: 10px; margin-bottom: 0.6rem;
}
.ops-hex {
    font-size: 1.2rem;
    color: #63b3ed;
}
.ops-name {
    font-family: 'Outfit', sans-serif;
    font-weight: 700;
    font-size: 1.1rem;
    color: #e2e8f4;
    letter-spacing: -0.3px;
}
.ops-sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    color: #2d4a6a;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

/* ── Panel / Card containers ── */
.panel {
    background: rgba(13,17,28,0.85);
    border: 1px solid rgba(99,179,237,0.1);
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(8px);
    position: relative;
}
.panel::before {
    content: '';
    position: absolute;
    top: 0; left: 1.5rem;
    width: 40px; height: 1px;
    background: rgba(99,179,237,0.35);
}

/* ── Stats row ── */
.stats-row {
    display: flex;
    gap: 10px;
    margin-bottom: 1rem;
}
.stat-chip {
    flex: 1;
    background: rgba(10,14,26,0.8);
    border: 1px solid rgba(99,179,237,0.1);
    border-radius: 10px;
    padding: 0.7rem 0.9rem;
    text-align: center;
}
.stat-chip .val {
    font-family: 'DM Mono', monospace;
    font-size: 1.2rem;
    font-weight: 500;
    color: #63b3ed;
    display: block;
}
.stat-chip .key {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    color: #3d5a80;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-top: 2px;
    display: block;
}

/* ── File list items (content view) ── */
.fc-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0.55rem 0.9rem;
    border-radius: 8px;
    margin: 3px 0;
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    border: 1px solid transparent;
    transition: all 0.15s;
}
.fc-item:hover { background: rgba(99,179,237,0.05); border-color: rgba(99,179,237,0.1); }
.fc-item.fc-dir { color: #f6ad55; border-left: 2px solid rgba(246,173,85,0.3); border-radius: 0 8px 8px 0; }
.fc-item.fc-file { color: #76e4f7; border-left: 2px solid rgba(118,228,247,0.3); border-radius: 0 8px 8px 0; }
.fc-sub {
    margin-left: 2rem;
    font-size: 0.72rem;
    color: #a78bfa;
    border-left: 1px dashed rgba(167,139,250,0.25);
    padding-left: 0.7rem;
}
.fc-size { margin-left: auto; color: #2d4a6a; font-size: 0.68rem; }

/* ── Feedback messages ── */
.fb { padding: 0.65rem 1rem; border-radius: 9px; font-family: 'DM Mono', monospace; font-size: 0.78rem; margin: 0.5rem 0; }
.fb-ok   { background: rgba(72,187,120,0.08); border: 1px solid rgba(72,187,120,0.25); color: #68d391; }
.fb-err  { background: rgba(252,129,129,0.08); border: 1px solid rgba(252,129,129,0.25); color: #fc8181; }
.fb-warn { background: rgba(246,173,85,0.08);  border: 1px solid rgba(246,173,85,0.25);  color: #f6ad55; }

/* ── Inputs ── */
.stTextInput input, .stTextArea textarea, .stSelectbox select {
    background: rgba(10,14,26,0.9) !important;
    color: #c8d8f0 !important;
    border: 1px solid rgba(99,179,237,0.18) !important;
    border-radius: 9px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.83rem !important;
    transition: border-color 0.2s !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: rgba(99,179,237,0.45) !important;
    box-shadow: 0 0 0 3px rgba(99,179,237,0.08) !important;
}
.stTextInput label, .stTextArea label, .stSelectbox label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    color: #3d5a80 !important;
    letter-spacing: 0.8px !important;
    text-transform: uppercase !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #1a3a5c, #1a2a50) !important;
    color: #63b3ed !important;
    border: 1px solid rgba(99,179,237,0.3) !important;
    border-radius: 9px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    padding: 0.55rem 1.5rem !important;
    letter-spacing: 0.3px !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #1e4570, #1e3460) !important;
    border-color: rgba(99,179,237,0.5) !important;
    color: #90cdf4 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(99,179,237,0.15) !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #7b1f3a, #5c1530) !important;
    color: #fc8181 !important;
    border-color: rgba(252,129,129,0.3) !important;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #922440, #6e1a38) !important;
    border-color: rgba(252,129,129,0.5) !important;
    box-shadow: 0 4px 20px rgba(252,129,129,0.15) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(10,14,26,0.5) !important;
    border-radius: 10px !important;
    border: 1px solid rgba(99,179,237,0.1) !important;
    padding: 3px !important;
    gap: 2px !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    color: #4a6080 !important;
    border-radius: 8px !important;
    padding: 0.4rem 1rem !important;
    background: transparent !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(99,179,237,0.12) !important;
    color: #63b3ed !important;
}

/* ── Radio ── */
.stRadio [data-testid="stWidgetLabel"] { display: none !important; }

/* ── Subheader ── */
h2, h3 {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    color: #b8cce4 !important;
    letter-spacing: -0.3px !important;
    font-size: 1.1rem !important;
    margin-bottom: 0.75rem !important;
}

/* ── Select box ── */
.stSelectbox [data-baseweb="select"] > div {
    background: rgba(10,14,26,0.9) !important;
    border: 1px solid rgba(99,179,237,0.18) !important;
    border-radius: 9px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.82rem !important;
    color: #c8d8f0 !important;
}

/* ── Code blocks ── */
.stCodeBlock {
    border: 1px solid rgba(99,179,237,0.12) !important;
    border-radius: 10px !important;
    background: rgba(5,8,18,0.95) !important;
}

/* ── Warning / info boxes ── */
.stAlert {
    border-radius: 10px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.78rem !important;
}

/* ── Divider ── */
hr { border-color: rgba(99,179,237,0.08) !important; margin: 0.75rem 0 !important; }

/* ── Caption / small text ── */
.stCaption, [data-testid="stCaptionContainer"] p {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.7rem !important;
    color: #3d5a80 !important;
}

/* ── Radio options styling ── */
.stRadio [data-testid="stMarkdownContainer"] { display: none; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ─────────────────────────────────────────────────────────────────────
def get_all_items():
    return sorted(Path('').rglob('*'))

def get_folder_size(folder: Path) -> int:
    return sum(f.stat().st_size for f in folder.rglob('*') if f.is_file())

def fmt_size(n: int) -> str:
    if n < 1024: return f"{n}B"
    if n < 1024**2: return f"{n/1024:.1f}KB"
    return f"{n/1024**2:.2f}MB"

def msg(text, kind="ok"):
    css = {"ok": "fb-ok", "err": "fb-err", "warn": "fb-warn"}
    st.markdown(f'<div class="fb {css.get(kind,"fb-ok")}">{text}</div>', unsafe_allow_html=True)

def render_tree():
    items = get_all_items()
    if not items:
        st.markdown('<div class="tree-item is-file"><span class="tree-dot"></span>empty</div>', unsafe_allow_html=True)
        return
    for item in items:
        name = str(item)
        if item.is_dir():
            st.markdown(f'<div class="tree-item is-folder"><span class="tree-dot"></span>/{name}</div>', unsafe_allow_html=True)
        else:
            size = fmt_size(item.stat().st_size) if item.is_file() else ""
            st.markdown(f'<div class="tree-item is-file"><span class="tree-dot"></span>{name}<span style="margin-left:auto;color:#2d4a6a;font-size:0.62rem">{size}</span></div>', unsafe_allow_html=True)


# ── Sidebar ──────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="ops-header">
      <div class="logo-row">
        <span class="ops-hex">⬡</span>
        <span class="ops-name">FileOS</span>
      </div>
      <div class="ops-sub">v2.0 · pathlib engine</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-label" style="padding:0 0.5rem;margin-top:0.75rem">Operations</div>', unsafe_allow_html=True)

    operation = st.radio("ops", [
        "📄  Create File",
        "👁  Read File",
        "✏️  Update File",
        "🗑  Delete File",
        "🔤  Rename File",
        "───────────",
        "📁  Create Folder",
        "🔍  Read Folder",
        "📝  Update Folder",
        "🔤  Rename Folder",
        "❌  Delete Folder",
        "───────────",
        "📁+  File in Folder",
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown('<div class="sec-label" style="padding:0 0.5rem">File Tree</div>', unsafe_allow_html=True)
    render_tree()


# ── Header ───────────────────────────────────────────────────────────────────────
op_clean = operation.strip().lstrip("📄👁✏️🗑🔤📁🔍📝❌+─ ")
st.markdown(f"""
<div class="os-header">
  <div class="os-logo">⬡</div>
  <div class="os-title">
    <h1>FileOS <span style="color:#3d5a80;font-weight:300">·</span> File Manager</h1>
    <p>pathlib engine · CRUD · folders & files</p>
  </div>
  <div class="os-badge">{operation.strip()[:30]}</div>
</div>
""", unsafe_allow_html=True)


# ── Skip dividers ────────────────────────────────────────────────────────────────
if "───" in operation:
    st.markdown('<div class="panel"><p style="font-family:\'DM Mono\',monospace;font-size:0.8rem;color:#3d5a80;text-align:center">Select an operation from the sidebar</p></div>', unsafe_allow_html=True)
    st.stop()


# ── 1. Create File ───────────────────────────────────────────────────────────────
elif operation == "📄  Create File":
    st.subheader("Create New File")
    with st.container():
        file_name = st.text_input("File name", placeholder="e.g. notes.txt")
        content   = st.text_area("Content", height=140, placeholder="File contents...")
        if st.button("⬡  Create File"):
            if not file_name:
                msg("⚠ Enter a file name", "warn")
            else:
                p = Path(file_name)
                if p.exists(): msg("⚠ File already exists", "warn")
                else:
                    try:
                        p.parent.mkdir(parents=True, exist_ok=True); p.write_text(content)
                        msg(f"✓ '{file_name}' created")
                        st.rerun()
                    except Exception as e: msg(f"✗ {e}", "err")

# ── 2. Read File ─────────────────────────────────────────────────────────────────
elif operation == "👁  Read File":
    st.subheader("Read File")
    items = [str(i) for i in get_all_items() if Path(i).is_file()]
    if not items: msg("No files available", "warn")
    else:
        file_name = st.selectbox("Select file", items)
        if st.button("⬡  Read"):
            try:
                content = Path(file_name).read_text()
                size = fmt_size(Path(file_name).stat().st_size)
                st.markdown(f'<div class="stats-row"><div class="stat-chip"><span class="val">{size}</span><span class="key">size</span></div><div class="stat-chip"><span class="val">{len(content.splitlines())}</span><span class="key">lines</span></div><div class="stat-chip"><span class="val">{len(content)}</span><span class="key">chars</span></div></div>', unsafe_allow_html=True)
                st.markdown('<div class="sec-label">Content</div>', unsafe_allow_html=True)
                st.code(content if content else "(empty file)", language="text")
            except Exception as e: msg(f"✗ {e}", "err")

# ── 3. Update File ───────────────────────────────────────────────────────────────
elif operation == "✏️  Update File":
    st.subheader("Update File")
    items = [str(i) for i in get_all_items() if Path(i).is_file()]
    if not items: msg("No files available", "warn")
    else:
        file_name   = st.selectbox("Select file", items)
        update_mode = st.radio("Mode", ["Overwrite", "Append"], horizontal=True)
        new_content = st.text_area("New content", height=140)
        if st.button("⬡  Update"):
            try:
                mode = 'w' if update_mode == "Overwrite" else 'a'
                with open(file_name, mode) as f: f.write(new_content)
                msg(f"✓ '{file_name}' updated ({update_mode.lower()})"); st.rerun()
            except Exception as e: msg(f"✗ {e}", "err")

# ── 4. Delete File ───────────────────────────────────────────────────────────────
elif operation == "🗑  Delete File":
    st.subheader("Delete File")
    items = [str(i) for i in get_all_items() if Path(i).is_file()]
    if not items: msg("No files available", "warn")
    else:
        file_name = st.selectbox("Select file", items)
        st.warning(f"This will permanently delete **{file_name}**")
        if st.button("⬡  Delete File", type="primary"):
            try:
                os.remove(file_name); msg(f"✓ '{file_name}' deleted"); st.rerun()
            except Exception as e: msg(f"✗ {e}", "err")

# ── 5. Rename File ───────────────────────────────────────────────────────────────
elif operation == "🔤  Rename File":
    st.subheader("Rename File")
    items = [str(i) for i in get_all_items() if Path(i).is_file()]
    if not items: msg("No files available", "warn")
    else:
        file_name = st.selectbox("Select file", items)
        new_name  = st.text_input("New name")
        if st.button("⬡  Rename"):
            if not new_name: msg("⚠ Enter a new name", "warn")
            else:
                try:
                    Path(file_name).rename(new_name); msg(f"✓ Renamed to '{new_name}'"); st.rerun()
                except Exception as e: msg(f"✗ {e}", "err")

# ── 6. Create Folder ─────────────────────────────────────────────────────────────
elif operation == "📁  Create Folder":
    st.subheader("Create Folder")
    folder_name = st.text_input("Folder name", placeholder="e.g. projects/docs")
    if st.button("⬡  Create Folder"):
        if not folder_name: msg("⚠ Enter a folder name", "warn")
        else:
            p = Path(folder_name)
            if p.exists(): msg("⚠ Already exists", "warn")
            else:
                try:
                    p.mkdir(parents=True); msg(f"✓ '{folder_name}' created"); st.rerun()
                except Exception as e: msg(f"✗ {e}", "err")

# ── 7. Read Folder ───────────────────────────────────────────────────────────────
elif operation == "🔍  Read Folder":
    st.subheader("Inspect Folder")
    folders = [str(i) for i in get_all_items() if Path(i).is_dir()]
    if not folders: msg("No folders available", "warn")
    else:
        folder_name = st.selectbox("Select folder", folders)
        if st.button("⬡  Inspect"):
            try:
                fp = Path(folder_name)
                direct  = list(fp.iterdir())
                subdirs = [x for x in direct if x.is_dir()]
                files   = [x for x in direct if x.is_file()]
                total_sz = get_folder_size(fp)

                st.markdown(f"""
                <div class="stats-row">
                  <div class="stat-chip"><span class="val">{len(direct)}</span><span class="key">items</span></div>
                  <div class="stat-chip"><span class="val">{len(subdirs)}</span><span class="key">folders</span></div>
                  <div class="stat-chip"><span class="val">{len(files)}</span><span class="key">files</span></div>
                  <div class="stat-chip"><span class="val">{fmt_size(total_sz)}</span><span class="key">total</span></div>
                </div>""", unsafe_allow_html=True)

                st.markdown('<div class="sec-label">Direct Contents</div>', unsafe_allow_html=True)
                if not direct:
                    st.markdown('<div class="fc-item fc-file">empty folder</div>', unsafe_allow_html=True)
                else:
                    for item in sorted(direct):
                        if item.is_dir():
                            children = list(item.iterdir())
                            st.markdown(f'<div class="fc-item fc-dir">📁 {item.name}/ <span class="fc-size">{len(children)} items</span></div>', unsafe_allow_html=True)
                            for ch in sorted(children)[:8]:
                                icon = "📁" if ch.is_dir() else "📄"
                                sz   = fmt_size(ch.stat().st_size) if ch.is_file() else ""
                                st.markdown(f'<div class="fc-item fc-file fc-sub">{icon} {ch.name}<span class="fc-size">{sz}</span></div>', unsafe_allow_html=True)
                            if len(children) > 8:
                                st.markdown(f'<div class="fc-item fc-file fc-sub" style="color:#3d5a80">… {len(children)-8} more</div>', unsafe_allow_html=True)
                        else:
                            sz = fmt_size(item.stat().st_size)
                            st.markdown(f'<div class="fc-item fc-file">📄 {item.name}<span class="fc-size">{sz}</span></div>', unsafe_allow_html=True)

                all_files = [x for x in fp.rglob('*') if x.is_file()]
                if all_files:
                    st.markdown('<div class="sec-label" style="margin-top:1.2rem">All Files (recursive)</div>', unsafe_allow_html=True)
                    for f in sorted(all_files):
                        rel = f.relative_to(fp)
                        sz  = fmt_size(f.stat().st_size)
                        st.markdown(f'<div class="fc-item fc-file">📄 {rel}<span class="fc-size">{sz}</span></div>', unsafe_allow_html=True)
            except Exception as e: msg(f"✗ {e}", "err")

# ── 8. Update Folder ─────────────────────────────────────────────────────────────
elif operation == "📝  Update Folder":
    st.subheader("Update Folder")
    st.caption("Add sub-folders, move files in or out")
    folders = [str(i) for i in get_all_items() if Path(i).is_dir()]
    if not folders: msg("No folders available", "warn")
    else:
        folder_name = st.selectbox("Target folder", folders)
        tab1, tab2, tab3 = st.tabs(["➕ Add Sub-folder", "📥 Move File In", "📤 Move File Out"])

        with tab1:
            sub = st.text_input("Sub-folder name", key="sub_k")
            if st.button("⬡  Create Sub-folder", key="sub_btn"):
                if not sub: msg("⚠ Enter a name", "warn")
                else:
                    p = Path(folder_name) / sub
                    if p.exists(): msg("⚠ Already exists", "warn")
                    else:
                        try: p.mkdir(parents=True); msg(f"✓ '{p}' created"); st.rerun()
                        except Exception as e: msg(f"✗ {e}", "err")

        with tab2:
            ext = [str(i) for i in get_all_items() if Path(i).is_file() and Path(i).parent != Path(folder_name)]
            if not ext: msg("No external files to move in", "warn")
            else:
                ftm = st.selectbox("File to move in", ext, key="mi_sel")
                if st.button("⬡  Move In", key="mi_btn"):
                    try:
                        s, d = Path(ftm), Path(folder_name) / Path(ftm).name
                        if d.exists(): msg("⚠ File already exists there", "warn")
                        else: shutil.move(str(s), str(d)); msg(f"✓ '{s.name}' moved in"); st.rerun()
                    except Exception as e: msg(f"✗ {e}", "err")

        with tab3:
            inside = [str(i) for i in get_all_items() if Path(i).is_file() and str(Path(i)).startswith(folder_name + os.sep)]
            if not inside: msg("No files inside this folder", "warn")
            else:
                ftm  = st.selectbox("File to move out", inside, key="mo_sel")
                dest = st.text_input("Destination (blank = current dir)", key="mo_dest")
                if st.button("⬡  Move Out", key="mo_btn"):
                    try:
                        s  = Path(ftm)
                        df = Path(dest) if dest.strip() else Path('')
                        d  = df / s.name
                        if d.exists(): msg("⚠ Already exists at destination", "warn")
                        else: shutil.move(str(s), str(d)); msg(f"✓ '{s.name}' moved out"); st.rerun()
                    except Exception as e: msg(f"✗ {e}", "err")

# ── 9. Rename Folder ─────────────────────────────────────────────────────────────
elif operation == "🔤  Rename Folder":
    st.subheader("Rename Folder")
    folders = [str(i) for i in get_all_items() if Path(i).is_dir()]
    if not folders: msg("No folders available", "warn")
    else:
        folder_name = st.selectbox("Select folder", folders)
        new_name    = st.text_input("New name")
        st.caption("All contents will be preserved")
        if st.button("⬡  Rename Folder"):
            if not new_name: msg("⚠ Enter a new name", "warn")
            elif new_name == folder_name: msg("⚠ Same name as current", "warn")
            else:
                src = Path(folder_name); dst = src.parent / new_name
                if dst.exists(): msg(f"⚠ '{new_name}' already exists", "warn")
                else:
                    try: src.rename(dst); msg(f"✓ Renamed to '{new_name}'"); st.rerun()
                    except Exception as e: msg(f"✗ {e}", "err")

# ── 10. Delete Folder ────────────────────────────────────────────────────────────
elif operation == "❌  Delete Folder":
    st.subheader("Delete Folder")
    items = [str(i) for i in get_all_items() if Path(i).is_dir()]
    if not items: msg("No folders available", "warn")
    else:
        folder_name = st.selectbox("Select folder", items)
        mode = st.radio("Mode", ["Empty only", "Force delete all contents"], horizontal=True)
        if mode == "Empty only": st.warning(f"Folder must be empty · permanently removes **{folder_name}**")
        else: st.error(f"Deletes **{folder_name}** and ALL its contents — irreversible")
        if st.button("⬡  Delete Folder", type="primary"):
            try:
                if mode == "Empty only": Path(folder_name).rmdir()
                else: shutil.rmtree(folder_name)
                msg(f"✓ '{folder_name}' deleted"); st.rerun()
            except Exception as e: msg(f"✗ {e}", "err")

# ── 11. Create File in Folder ────────────────────────────────────────────────────
elif operation == "📁+  File in Folder":
    st.subheader("Create File in Folder")
    folders = [str(i) for i in get_all_items() if Path(i).is_dir()]
    tab1, tab2 = st.tabs(["Use Existing Folder", "Create New Folder"])

    with tab1:
        if not folders: msg("No folders yet — use the other tab", "warn")
        else:
            fn = st.selectbox("Folder", folders, key="ef_sel")
            nm = st.text_input("File name", key="ef_nm")
            ct = st.text_area("Content", height=110, key="ef_ct")
            if st.button("⬡  Create", key="ef_btn"):
                if not nm: msg("⚠ Enter a file name", "warn")
                else:
                    p = Path(fn) / nm
                    if p.exists(): msg("⚠ Already exists", "warn")
                    else:
                        try: p.write_text(ct); msg(f"✓ '{p}' created"); st.rerun()
                        except Exception as e: msg(f"✗ {e}", "err")

    with tab2:
        nf = st.text_input("New folder name", key="nf_nm")
        nm = st.text_input("File name", key="nf_fn")
        ct = st.text_area("Content", height=110, key="nf_ct")
        if st.button("⬡  Create Both", key="nf_btn"):
            if not nf or not nm: msg("⚠ Enter both names", "warn")
            else:
                p = Path(nf) / nm
                if p.exists(): msg("⚠ Already exists", "warn")
                else:
                    try: p.parent.mkdir(parents=True, exist_ok=True); p.write_text(ct); msg(f"✓ '{p}' created"); st.rerun()
                    except Exception as e: msg(f"✗ {e}", "err")