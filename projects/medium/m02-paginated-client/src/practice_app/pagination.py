"""Page traversal with protocol guards."""
from dataclasses import dataclass
from .models import Page, ProtocolError


@dataclass(frozen=True)
class Traversal:
    pages: tuple
    cursors: tuple

    @property
    def page_count(self):
        return len(self.pages)


def traverse(api, dataset, page_size, max_pages):
    if not dataset or page_size <= 0 or max_pages <= 0:
        raise ValueError("Invalid traversal request")
    cursor = None
    seen = set()
    pages = []
    cursors = []
    while True:
        if len(pages) >= max_pages:
            raise ProtocolError("Page limit exceeded")
        if cursor in seen:
            raise ProtocolError("Repeated cursor")
        seen.add(cursor)
        cursors.append(cursor)
        page = Page.from_dict(api.fetch_page(dataset, cursor, page_size))
        pages.append(page)
        if not page.next_cursor:
            break
        cursor = page.next_cursor
    return Traversal(tuple(pages), tuple(cursors))


def collect(traversal):
    accumulated = []
    for page in traversal.pages:
        accumulated = list(page.items)
    seen = set()
    unique = []
    for record in accumulated:
        if record.id not in seen:
            seen.add(record.id)
            unique.append(record)
    return tuple(unique)
