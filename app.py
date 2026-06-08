import os
import re
import time
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="YT Blog AI · LangChain",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS 
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@400;500&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        background: #0a0a0f;
        color: #e8e6f0;
        font-family: 'Syne', sans-serif;
    }
    [data-testid="stAppViewContainer"]::before {
        content: '';
        position: fixed;
        inset: 0;
        background:
            radial-gradient(ellipse 80% 60% at 20% 10%, rgba(123,58,237,0.18) 0%, transparent 60%),
            radial-gradient(ellipse 60% 50% at 80% 90%, rgba(236,72,153,0.12) 0%, transparent 60%);
        pointer-events: none;
        z-index: 0;
    }

    [data-testid="stSidebar"] {
        background: rgba(14,12,26,0.95) !important;
        border-right: 1px solid rgba(123,58,237,0.3);
    }
    [data-testid="stSidebar"] * { color: #e8e6f0 !important; }

    .hero-title {
        font-family: 'DM Serif Display', serif;
        font-size: clamp(2.2rem, 5vw, 3.8rem);
        font-weight: 400;
        line-height: 1.1;
        background: linear-gradient(135deg, #a78bfa 0%, #ec4899 50%, #f59e0b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.2rem;
    }
    .hero-sub {
        font-size: 0.95rem;
        color: rgba(232,230,240,0.5);
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 2rem;
    }
    .badge {
        display: inline-block;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        padding: 0.2rem 0.65rem;
        border-radius: 999px;
        background: linear-gradient(135deg, rgba(123,58,237,0.25), rgba(236,72,153,0.2));
        border: 1px solid rgba(167,139,250,0.4);
        color: #c4b5fd;
        margin-bottom: 1.5rem;
    }

    .glass-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(123,58,237,0.25);
        border-radius: 16px;
        padding: 1.6rem 1.8rem;
        margin-bottom: 1.2rem;
        backdrop-filter: blur(10px);
    }
    .section-label {
        font-size: 0.7rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: #a78bfa;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }

    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(123,58,237,0.4) !important;
        border-radius: 10px !important;
        color: #e8e6f0 !important;
        font-family: 'Syne', sans-serif !important;
        font-size: 0.95rem !important;
        padding: 0.75rem 1rem !important;
        transition: border-color 0.2s, box-shadow 0.2s;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #a78bfa !important;
        box-shadow: 0 0 0 3px rgba(167,139,250,0.15) !important;
    }

    .stButton > button[kind="primary"],
    div[data-testid="stForm"] .stButton > button {
        background: linear-gradient(135deg, #7c3aed, #ec4899) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 10px !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.05em !important;
        padding: 0.65rem 1.8rem !important;
        cursor: pointer !important;
        transition: opacity 0.2s, transform 0.15s !important;
    }
    .stButton > button[kind="primary"]:hover {
        opacity: 0.88 !important;
        transform: translateY(-1px) !important;
    }
    .stButton > button:not([kind="primary"]) {
        background: transparent !important;
        border: 1px solid rgba(167,139,250,0.5) !important;
        color: #a78bfa !important;
        border-radius: 10px !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 600 !important;
    }

    .status-box {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        background: rgba(167,139,250,0.08);
        border: 1px solid rgba(167,139,250,0.3);
        border-radius: 10px;
        padding: 0.85rem 1.2rem;
        font-size: 0.9rem;
        margin-bottom: 0.8rem;
        transition: border-color 0.3s;
    }
    .status-box.active {
        border-color: #a78bfa;
        background: rgba(167,139,250,0.14);
    }
    .status-box.done {
        border-color: rgba(52,211,153,0.5);
        background: rgba(52,211,153,0.06);
    }
    .status-dot {
        width: 9px; height: 9px;
        border-radius: 50%;
        background: #a78bfa;
        flex-shrink: 0;
        animation: pulse 1.4s ease-in-out infinite;
    }
    .status-dot.done { background: #34d399; animation: none; }
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.4; transform: scale(0.7); }
    }

    .blog-output {
        background: rgba(255,255,255,0.035);
        border: 1px solid rgba(123,58,237,0.2);
        border-radius: 16px;
        padding: 2rem 2.2rem;
        font-family: 'DM Serif Display', serif;
        font-size: 1.05rem;
        line-height: 1.8;
        color: #e8e6f0;
        white-space: pre-wrap;
        word-break: break-word;
    }

    .metric-row { display: flex; gap: 1rem; margin-bottom: 1.2rem; flex-wrap: wrap; }
    .metric-card {
        flex: 1; min-width: 120px;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(123,58,237,0.2);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        text-align: center;
    }
    .metric-val {
        font-family: 'DM Mono', monospace;
        font-size: 1.5rem;
        font-weight: 500;
        color: #a78bfa;
    }
    .metric-lbl {
        font-size: 0.7rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: rgba(232,230,240,0.45);
        margin-top: 0.2rem;
    }

    .stTabs [data-baseweb="tab-list"] {
        background: transparent !important;
        border-bottom: 1px solid rgba(123,58,237,0.25) !important;
        gap: 0 !important;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Syne', sans-serif !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.08em !important;
        color: rgba(232,230,240,0.5) !important;
        padding: 0.6rem 1.4rem !important;
        border-bottom: 2px solid transparent !important;
    }
    .stTabs [aria-selected="true"] {
        color: #a78bfa !important;
        border-bottom-color: #a78bfa !important;
    }

    .chain-step {
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    .chain-num {
        font-family: 'DM Mono', monospace;
        font-size: 1.1rem;
        color: #a78bfa;
        flex-shrink: 0;
        margin-top: 0.05rem;
        width: 24px;
    }
    .chain-arrow {
        text-align: center;
        color: rgba(167,139,250,0.4);
        font-size: 1.3rem;
        margin: 0.2rem 0 0.2rem 0;
    }

    hr { border-color: rgba(123,58,237,0.2); }
    .stAlert { border-radius: 10px; }
    label { color: rgba(232,230,240,0.7) !important; font-size: 0.85rem !important; }
    code {
        background: rgba(167,139,250,0.12) !important;
        color: #c4b5fd !important;
        border-radius: 4px !important;
        padding: 0.1em 0.35em !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ── Session State ─────────────────────────────────────────────────────────────
for key, default in {
    "blog_result": None,
    "generation_time": None,
    "word_count": 0,
    "history": [],
    "running": False,
    "current_step": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("###  Configuration")
    st.markdown("---")

    hf_token = st.text_input(
        "HuggingFace Token",
        value=os.getenv("HF_TOKEN", ""),
        type="password",
        placeholder="hf_xxxxxxxxxxxx",
        help="Your HuggingFace API token.",
    )
    if hf_token:
        os.environ["HF_TOKEN"] = hf_token

    st.markdown("---")

    model_info = {
        "Model": "meta-llama/Meta-Llama-3-8B-Instruct",
        "Framework": "LangChain LCEL",
        "Chains": "2 (Researcher + Writer)",
        "Pattern": "Sequential pipe ( | )",
    }
    st.markdown("###  Pipeline Info")
    for k, v in model_info.items():
        st.markdown(
            f'<p style="font-size:0.8rem; color:rgba(232,230,240,0.6); margin:0.2rem 0;">'
            f'<span style="color:#a78bfa; font-weight:600;">{k}:</span> {v}</p>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("###  History")
    if st.session_state.history:
        for i, item in enumerate(reversed(st.session_state.history[-5:])):
            with st.expander(f"#{len(st.session_state.history) - i} {item['topic'][:28]}…"):
                st.caption(item["channel"])
                st.caption(item["timestamp"])
    else:
        st.caption("No generations yet.")

    st.markdown("---")
    st.markdown("### ℹ About")
    st.caption(
        "Built in **LangChain LCEL** — two chained runnables "
        
    )


# ── Main Layout ───────────────────────────────────────────────────────────────
st.markdown('<p class="hero-title">YouTube → Blog AI</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-sub">LangChain LCEL · Two-chain research & writing pipeline</p>',
    unsafe_allow_html=True,
)
st.markdown('<span class="badge">⛓ LangChain Edition</span>', unsafe_allow_html=True)

tab_generate, tab_about = st.tabs(["✦ Generate", "✦ How It Works"])


# ── Generate Tab ──────────────────────────────────────────────────────────────
with tab_generate:
    col_form, col_result = st.columns([1, 1.4], gap="large")

    with col_form:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<p class="section-label">Channel</p>', unsafe_allow_html=True)
        channel_handle = st.text_input(
            label="YouTube Channel Handle",
            placeholder="@veritasium or https://www.youtube.com/@veritasium",
            label_visibility="collapsed",
        )

        st.markdown(
            '<p class="section-label" style="margin-top:1rem;">Topic / Query</p>',
            unsafe_allow_html=True,
        )
        topic = st.text_area(
            label="Topic",
            placeholder="e.g. 'latest AI trends', 'Python tutorial for beginners'",
            height=100,
            label_visibility="collapsed",
        )

        st.markdown(
            '<p class="section-label" style="margin-top:1rem;">Output File Name</p>',
            unsafe_allow_html=True,
        )
        output_filename = st.text_input(
            label="Output file",
            value="new-blog-post.md",
            label_visibility="collapsed",
        )
        st.markdown("</div>", unsafe_allow_html=True)

        def validate() -> str | None:
            if not channel_handle.strip():
                return "Please enter a YouTube channel handle."
            if not topic.strip():
                return "Please enter a topic to search for."
            if not os.getenv("HF_TOKEN"):
                return "HuggingFace token is missing — add it in the sidebar or .env file."
            return None

        run_btn = st.button(
            "🚀 Generate Blog Post", type="primary", use_container_width=True
        )

        if run_btn:
            err = validate()
            if err:
                st.error(err)
            else:
                st.session_state.running = True
                st.session_state.blog_result = None
                st.session_state.current_step = "researcher"

        if st.session_state.blog_result:
            dl_col1, dl_col2 = st.columns(2)
            with dl_col1:
                st.download_button(
                    "⬇ Download .md",
                    data=st.session_state.blog_result,
                    file_name=output_filename,
                    mime="text/markdown",
                    use_container_width=True,
                )
            with dl_col2:
                st.download_button(
                    "⬇ Download .txt",
                    data=st.session_state.blog_result,
                    file_name=output_filename.replace(".md", ".txt"),
                    mime="text/plain",
                    use_container_width=True,
                )

    # ── Right Column ──────────────────────────────────────────────────────────
    with col_result:
        if st.session_state.running:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown(
                '<p class="section-label">Chain Status</p>', unsafe_allow_html=True
            )

            steps = [
                ("🔍", "Researcher Chain", "Searching YouTube & building research report…"),
                ("✍️", "Writer Chain", "Drafting Markdown blog post from research…"),
                ("💾", "Output", "Saving file & returning result…"),
            ]
            step_keys = ["researcher", "writer", "output"]
            step_placeholders = []
            for (icon, name, msg), key in zip(steps, step_keys):
                ph = st.empty()
                step_placeholders.append((ph, key, icon, name, msg))
                ph.markdown(
                    f'<div class="status-box">'
                    f'<span class="status-dot"></span>'
                    f'<span><strong>{icon} {name}</strong> — Waiting…</span>'
                    f"</div>",
                    unsafe_allow_html=True,
                )

            st.markdown("</div>", unsafe_allow_html=True)
            progress = st.progress(0, text="Initialising LangChain pipeline…")

            def update_step(active_key: str, msg: str):
                for ph, key, icon, name, default_msg in step_placeholders:
                    if key == active_key:
                        ph.markdown(
                            f'<div class="status-box active">'
                            f'<span class="status-dot"></span>'
                            f'<span><strong>{icon} {name}</strong> — {msg}</span>'
                            f"</div>",
                            unsafe_allow_html=True,
                        )

            def mark_done(done_key: str):
                for ph, key, icon, name, default_msg in step_placeholders:
                    if key == done_key:
                        ph.markdown(
                            f'<div class="status-box done">'
                            f'<span class="status-dot done"></span>'
                            f'<span><strong>{icon} {name}</strong> — ✓ Done</span>'
                            f"</div>",
                            unsafe_allow_html=True,
                        )

            try:
                from agent import run_pipeline

                t0 = time.time()

                # Step 1: Researcher
                update_step("researcher", "Searching YouTube & compiling research report…")
                progress.progress(15, text="Chain 1/2 · Researcher running…")

                # We use a stateful callback that updates the UI
                completed_steps: list[str] = []

                def on_step(step_name: str, message: str):
                    if step_name == "researcher":
                        update_step("researcher", message)
                        progress.progress(30, text="Chain 1/2 · Researcher running…")
                    elif step_name == "writer":
                        mark_done("researcher")
                        completed_steps.append("researcher")
                        update_step("writer", message)
                        progress.progress(65, text="Chain 2/2 · Writer running…")
                    elif step_name == "output":
                        mark_done("writer")
                        completed_steps.append("writer")
                        update_step("output", message)
                        progress.progress(90, text="Saving output…")

                result = run_pipeline(
                    topic=topic.strip(),
                    channel_handle=channel_handle.strip(),
                    output_file=output_filename,
                    on_step=on_step,
                )

                mark_done("output")
                elapsed = round(time.time() - t0, 1)
                words = len(re.findall(r"\w+", result))

                progress.progress(100, text="Done! ✓")

                st.session_state.blog_result = result
                st.session_state.generation_time = elapsed
                st.session_state.word_count = words
                st.session_state.running = False
                st.session_state.history.append(
                    {
                        "topic": topic,
                        "channel": channel_handle,
                        "timestamp": datetime.now().strftime("%d %b %Y %H:%M"),
                    }
                )
                st.rerun()

            except Exception as e:
                st.session_state.running = False
                progress.empty()
                st.error(f"**Pipeline error:** {e}")
                st.info(
                    "💡 Make sure your HF_TOKEN is set and the model endpoint is accessible.",
                    icon="ℹ️",
                )

        elif st.session_state.blog_result:
            g_time = st.session_state.generation_time or 0
            w_count = st.session_state.word_count or 0
            read_min = max(1, w_count // 200)

            st.markdown(
                f"""
                <div class="metric-row">
                    <div class="metric-card">
                        <div class="metric-val">{w_count}</div>
                        <div class="metric-lbl">Words</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-val">{read_min} min</div>
                        <div class="metric-lbl">Read Time</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-val">{g_time}s</div>
                        <div class="metric-lbl">Gen Time</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-val">2</div>
                        <div class="metric-lbl">Chains Run</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            view_md, view_raw = st.tabs(["Rendered", "Raw Markdown"])
            with view_md:
                st.markdown(st.session_state.blog_result)
            with view_raw:
                st.markdown(
                    f'<div class="blog-output">{st.session_state.blog_result}</div>',
                    unsafe_allow_html=True,
                )

            if st.button("🔄 Reset & Start New"):
                st.session_state.blog_result = None
                st.session_state.generation_time = None
                st.session_state.word_count = 0
                st.rerun()

        else:
            st.markdown(
                """
                <div class="glass-card" style="text-align:center; padding: 3rem 2rem;">
                    <div style="font-size:3rem; margin-bottom:1rem;">⛓</div>
                    <p style="font-family:'DM Serif Display',serif; font-size:1.3rem;
                               color:#c4b5fd; margin-bottom:0.5rem;">
                        Two LCEL chains, one blog post.
                    </p>
                    <p style="color:rgba(232,230,240,0.45); font-size:0.9rem; line-height:1.6;">
                        Enter a channel handle and topic on the left.<br>
                        The <strong>Researcher chain</strong> finds videos,<br>
                        the <strong>Writer chain</strong> crafts the post.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ── How It Works Tab ──────────────────────────────────────────────────────────
with tab_about:
    st.markdown(
        """
        <div class="glass-card">
            <p class="section-label">LangChain LCEL Pipeline</p>
            <p style="line-height:1.8; color:rgba(232,230,240,0.8);">
                This app rebuilds the original CrewAI multi-agent system using
                <strong>LangChain Expression Language (LCEL)</strong> and
                <strong>meta-llama/Meta-Llama-3-8B-Instruct</strong> via HuggingFace Inference Endpoints.
                Instead of CrewAI agents, two sequential
                <code>Runnable</code> chains are piped together using the
                <code>|</code> operator.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Visual pipeline diagram
    st.markdown(
        """
        <div class="glass-card">
            <p class="section-label">Pipeline Architecture</p>
            <div style="font-family:'DM Mono',monospace; font-size:0.85rem;
                        color:rgba(232,230,240,0.75); line-height:2.2;">
                <span style="color:#a78bfa;">Input</span>
                &nbsp;{topic, channel_handle}<br>
                &nbsp;&nbsp;&nbsp;&nbsp;↓<br>
                <span style="color:#ec4899;">RunnableLambda</span>
                &nbsp;→ YouTubeSearchTool.run()<br>
                &nbsp;&nbsp;&nbsp;&nbsp;↓<br>
                <span style="color:#ec4899;">RunnablePassthrough.assign</span>
                &nbsp;→ {topic, channel, yt_results}<br>
                &nbsp;&nbsp;&nbsp;&nbsp;↓<br>
                <span style="color:#f59e0b;">ChatPromptTemplate</span>
                &nbsp;(Researcher prompt)<br>
                &nbsp;&nbsp;&nbsp;&nbsp;↓<br>
                <span style="color:#34d399;">HuggingFaceEndpoint</span>
                &nbsp;→ research_report (str)<br>
                &nbsp;&nbsp;&nbsp;&nbsp;↓<br>
                <span style="color:#f59e0b;">ChatPromptTemplate</span>
                &nbsp;(Writer prompt)<br>
                &nbsp;&nbsp;&nbsp;&nbsp;↓<br>
                <span style="color:#34d399;">HuggingFaceEndpoint</span>
                &nbsp;→ blog_post (str)<br>
                &nbsp;&nbsp;&nbsp;&nbsp;↓<br>
                <span style="color:#a78bfa;">Output</span>
                &nbsp;Markdown file + UI display
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    steps_data = [
        (
            "1",
            "🔍",
            "Researcher Chain",
            (
                "Uses <code>RunnablePassthrough.assign</code> to inject YouTube search "
                "results into the context, then passes everything through a "
                "<code>ChatPromptTemplate</code> and meta-llama/Meta-Llama-3-8B-Instruct produce a "
                "3-paragraph research report."
            ),
        ),
        (
            "2",
            "✍️",
            "Writer Chain",
            (
                "Receives the research report as a plain string and writes a "
                "full structured Markdown blog post (500+ words) via a second "
                "<code>ChatPromptTemplate | LLM | StrOutputParser</code> chain."
            ),
        ),
        (
            "3",
            "💾",
            "Output",
            (
                "The final Markdown string is saved to disk and streamed back "
                "to the Streamlit interface for rendering, raw view, and download."
            ),
        ),
    ]

    for num, icon, title, desc in steps_data:
        st.markdown(
            f"""
            <div class="glass-card" style="display:flex; gap:1.2rem; align-items:flex-start;">
                <div class="chain-num">{num}</div>
                <div>
                    <p style="font-size:1rem; font-weight:700; margin:0 0 0.3rem;">
                        {icon} {title}
                    </p>
                    <p style="color:rgba(232,230,240,0.6); font-size:0.9rem;
                               line-height:1.65; margin:0;">{desc}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="glass-card" style="margin-top:0.5rem;">
            <p class="section-label">CrewAI → LangChain Migration Map</p>
            <table style="width:100%; font-size:0.85rem; border-collapse:collapse;
                          color:rgba(232,230,240,0.75);">
                <thead>
                    <tr style="border-bottom:1px solid rgba(123,58,237,0.3);">
                        <th style="text-align:left; padding:0.5rem 0.8rem; color:#a78bfa;">
                            CrewAI concept</th>
                        <th style="text-align:left; padding:0.5rem 0.8rem; color:#a78bfa;">
                            LangChain equivalent</th>
                    </tr>
                </thead>
                <tbody>
                    <tr style="border-bottom:1px solid rgba(123,58,237,0.1);">
                        <td style="padding:0.45rem 0.8rem;"><code>Agent</code></td>
                        <td style="padding:0.45rem 0.8rem;"><code>Runnable</code> chain (prompt | llm | parser)</td>
                    </tr>
                    <tr style="border-bottom:1px solid rgba(123,58,237,0.1);">
                        <td style="padding:0.45rem 0.8rem;"><code>Task</code></td>
                        <td style="padding:0.45rem 0.8rem;"><code>ChatPromptTemplate</code> + invocation</td>
                    </tr>
                    <tr style="border-bottom:1px solid rgba(123,58,237,0.1);">
                        <td style="padding:0.45rem 0.8rem;"><code>Crew(process=sequential)</code></td>
                        <td style="padding:0.45rem 0.8rem;"><code>chain1.invoke() → chain2.invoke()</code></td>
                    </tr>
                    <tr style="border-bottom:1px solid rgba(123,58,237,0.1);">
                        <td style="padding:0.45rem 0.8rem;"><code>YoutubeVideoSearchTool</code></td>
                        <td style="padding:0.45rem 0.8rem;"><code>YouTubeSearchTool</code> + <code>RunnableLambda</code></td>
                    </tr>
                    <tr>
                        <td style="padding:0.45rem 0.8rem;"><code>crew.kickoff(inputs=…)</code></td>
                        <td style="padding:0.45rem 0.8rem;"><code>chain.invoke({…})</code></td>
                    </tr>
                </tbody>
            </table>
        </div>
        """,
        unsafe_allow_html=True,
    )
