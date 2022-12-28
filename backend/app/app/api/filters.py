from typing import Optional

from fastapi import Query

from app.utils.enums import TransactionLogKind


class ItemFilterParams:
    def __init__(
            self,
            category_id: Optional[int] = Query(None, title="Filter by category"),
    ):
        self.category_id = category_id


class TransactionFilterParams:
    def __init__(
            self,
            kind: Optional[TransactionLogKind] = Query(None, title="Filter by kind"),
    ):
        self.kind = kind
