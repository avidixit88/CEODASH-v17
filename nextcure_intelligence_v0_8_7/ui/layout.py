"""Reusable layout fragments for the dashboard."""

from __future__ import annotations

from html import escape

import streamlit as st

from config.settings import APP_SUBTITLE, APP_TITLE, APP_VERSION


def render_hero() -> None:
    st.markdown(
        f"""
        <div class="hero">
            <div class="status-pill">● {APP_VERSION}</div>
            <div class="eyebrow" style="margin-top: 1.1rem;">{APP_SUBTITLE}</div>
            <h1>{APP_TITLE}</h1>
            <p>
                A CEO-ready market intelligence surface for understanding whether the market is working for NextCure,
                how NXTC is behaving relative to biotech and Nasdaq benchmarks, and where peer momentum is concentrating.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _card_html(label: str, value: str, caption: str = "", detail: str | None = None, card_class: str = "card") -> str:
    detail_html = f'<div class="detail-pill">Detail: {escape(detail)}</div>' if detail else ""
    return (
        f'<div class="{card_class}">'
        f'<div class="metric-label">{escape(label)}</div>'
        f'<div class="metric-value">{escape(value)}</div>'
        f'<div class="muted card-caption">{escape(caption)}</div>'
        f'{detail_html}'
        f'</div>'
    )


def render_kpi_cards(kpis: list[dict[str, str]]) -> None:
    cols = st.columns(len(kpis))
    for col, item in zip(cols, kpis):
        with col:
            st.markdown(
                _card_html(str(item["label"]), str(item["value"]), str(item.get("caption", ""))),
                unsafe_allow_html=True,
            )


def render_dashboard_nav(pages: list[str], active_page: str) -> str:
    """Render a readable button-based navigation bar.

    We avoid binding a widget directly to `st.session_state.active_page` so the
    snapshot/detail buttons can safely update the active page without triggering
    Streamlit's post-instantiation session-state exception.
    """
    st.markdown('<div class="nav-title">Dashboard Sections</div>', unsafe_allow_html=True)
    for start in range(0, len(pages), 4):
        row = pages[start:start + 4]
        cols = st.columns(len(row), gap="small")
        for col, page in zip(cols, row):
            with col:
                label = f"● {page}" if page == active_page else page
                if st.button(label, key=f"nav_{page}"):
                    st.session_state.active_page = page
                    st.rerun()
    return st.session_state.active_page


def _summary_title(line: str) -> str:
    if ":" in line:
        return line.split(":", 1)[0]
    return "Readout"


def _summary_body(line: str) -> str:
    if ":" in line:
        return line.split(":", 1)[1].strip()
    return line


def _is_detail_line(line: str) -> bool:
    lower = line.lower()
    detail_markers = [
        "cdh6 / ovarian adc:",
        "b7-h4 adc:",
        "adc capital flow:",
        "ovarian cancer:",
        "data quality note:",
        "capital is strongest",
        "capital is weakest",
        "nxtc event positioning",
    ]
    return any(marker in lower for marker in detail_markers)


def _build_executive_narrative(insights: list[str]) -> str:
    joined = " ".join(insights).lower()
    activation = next((line for line in insights if line.lower().startswith("market activation")), "")
    action = next((line for line in insights if line.lower().startswith("what you can do")), "")

    if "not currently being rewarded" in joined or "stock-specific weakness" in joined:
        p1 = "The current read is defensive: NXTC is not being rewarded versus XBI and the broader biotech tape is not providing much help."
    elif "outperform" in joined or "constructive" in joined:
        p1 = "The current read is constructive: NXTC is showing signs of better positioning, but the quality of that move still needs to be checked against volume, peers, and catalyst timing."
    else:
        p1 = "The current read is selective: some signals are useful, but the market has not fully aligned behind the story yet."

    if activation:
        activation_body = _summary_body(activation)
        p2 = activation_body
    else:
        p2 = "The practical question is not only whether the technicals improve, but whether investors understand the upcoming catalyst well enough to start positioning ahead of it."

    if action:
        p3 = _summary_body(action)
        return f"{p1} {p2} Operator lens: {p3}"
    return p1 + " " + p2


def render_insights(insights: list[str]) -> None:
    st.markdown('<div class="section-title">Executive Readout</div>', unsafe_allow_html=True)
    if not insights:
        st.markdown('<div class="insight">No executive readout is available yet.</div>', unsafe_allow_html=True)
        return

    top_lines = [line for line in insights if not _is_detail_line(line)][:5]
    detail_lines = [line for line in insights if line not in top_lines]

    st.markdown(
        f'<div class="executive-narrative"><div class="summary-title">Plain-English CEO summary</div>'
        f'<div class="summary-body">{escape(_build_executive_narrative(insights))}</div></div>',
        unsafe_allow_html=True,
    )

    for row_start in range(0, len(top_lines), 2):
        row = top_lines[row_start:row_start + 2]
        cols = st.columns(len(row), gap="medium")
        for col, line in zip(cols, row):
            with col:
                st.markdown(
                    f'<div class="summary-card"><div class="summary-title">{escape(_summary_title(line))}</div>'
                    f'<div class="summary-body">{escape(_summary_body(line))}</div></div>',
                    unsafe_allow_html=True,
                )

    if detail_lines:
        with st.expander("Click to see more granular channel, catalyst, and technical detail"):
            for insight in detail_lines:
                st.markdown(f'<div class="insight">{escape(insight)}</div>', unsafe_allow_html=True)


def _detail_target(label: str) -> str:
    text = label.lower()
    if "technical" in text or "alignment" in text:
        return "Technical + Catalyst"
    if "catalyst" in text or "capital" in text:
        return "Catalyst & Capital"
    if "adc" in text or "ovarian" in text or "quarter" in text:
        return "Channel Intelligence"
    if "attention" in text or "activation" in text:
        return "Strategy & Timing"
    if "market" in text or "nxtc" in text or "driver" in text or "window" in text:
        return "Strategy & Timing"
    return "Relevant tab"


def _priority_watch_items(items: list[dict[str, str]]) -> list[dict[str, str]]:
    keep = {"Market", "NXTC Posture", "Driver", "Window Score", "Market Attention", "Catalyst Phase", "Technical Setup", "Alignment"}
    prioritized = [item for item in items if str(item.get("label", "")) in keep]
    # keep order stable, but avoid showing too many cards at the top
    return prioritized[:8]


def render_watch_items(items: list[dict[str, str]]) -> None:
    if not items:
        return
    st.markdown('<div class="section-title">Intelligence Snapshot</div>', unsafe_allow_html=True)
    visible_items = _priority_watch_items(items)
    if not visible_items:
        visible_items = items[:6]

    for row_start in range(0, len(visible_items), 4):
        row = visible_items[row_start:row_start + 4]
        cols = st.columns(len(row), gap="medium")
        for col, item in zip(cols, row):
            label = str(item.get("label", ""))
            value = str(item.get("value", ""))
            caption = str(item.get("caption", ""))
            target = _detail_target(label)
            with col:
                st.markdown(
                    _card_html(label, value, caption, card_class="snapshot-card"),
                    unsafe_allow_html=True,
                )
                if st.button(f"View {target} →", key=f"detail_{label}_{row_start}"):
                    st.session_state.active_page = target
                    st.rerun()
