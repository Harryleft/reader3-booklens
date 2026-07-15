from pathlib import Path

from fastapi.testclient import TestClient

import server


READER_TEMPLATE = Path(__file__).parents[1] / "templates" / "reader.html"


def test_book_reader_entry_redirects_to_first_chapter():
    response = TestClient(server.app).get(
        "/read/design-demo_data",
        follow_redirects=False,
    )

    assert response.status_code == 307
    assert response.headers["location"].endswith("/read/design-demo_data/0")


def test_reader_notes_feature_is_not_rendered_or_initialized():
    template = READER_TEMPLATE.read_text(encoding="utf-8")

    removed_markers = (
        "阅读笔记",
        'data-action="notes"',
        'id="notes-sheet"',
        "booklens-notes-",
        "renderNotes",
        "sheet-notes-open",
    )

    assert all(marker not in template for marker in removed_markers)


def test_ai_book_chat_consumes_server_sent_events_incrementally():
    template = READER_TEMPLATE.read_text(encoding="utf-8")

    assert "readAnswerStream" in template
    assert "response.body.getReader()" in template
    assert "text/event-stream" in template
    assert "event==='token'" in template


def test_reader_header_and_content_share_sidebar_animation_track():
    template = READER_TEMPLATE.read_text(encoding="utf-8")

    assert ".app.sheet-left-open{grid-template-columns:320px minmax(0,1fr) 0}" in template
    assert ".app.sheet-ai-open{grid-template-columns:0 minmax(0,1fr) var(--ai-panel-width)}" in template
    assert "transition:grid-template-columns .26s ease" in template
    assert ".topbar{grid-column:2;grid-row:1" in template
    assert ".reader-shell{grid-column:2;grid-row:2" in template
    assert "#main{height:100%;overflow:auto;scroll-behavior:smooth;scrollbar-gutter:stable both-edges;padding:0 92px;transition:padding .26s ease}" in template
    assert "padding:38px 115px 40px" in template and "padding .26s ease" in template
    assert "font-size:14px;transition:padding .26s ease" in template
    assert ".app.sheet-left-open .topbar" not in template
    assert ".app.sheet-left-open .reader-shell" not in template
    assert ".app.sheet-ai-open .topbar" not in template
    assert ".app.sheet-ai-open .reader-shell" not in template
    assert "transform:translateX(100%)" in template
    assert ".app:has(.side-sheet.open) .toolbar{max-width:0" in template
    assert ".app:has(.side-sheet.open) .toolbar{display:none}" not in template
