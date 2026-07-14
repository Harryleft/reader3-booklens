from pathlib import Path


READER_TEMPLATE = Path(__file__).parents[1] / "templates" / "reader.html"


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
