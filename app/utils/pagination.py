from typing import Tuple

def apply_pagination(query, page: int, per_page: int) -> Tuple[list, int]:
    """Apply offset/limit to a SQLAlchemy query and return (items, total)."""
    page = int(page) if page and int(page) > 0 else 1
    per_page = int(per_page) if per_page and int(per_page) > 0 else 10
    total = query.count()
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    return items, total
