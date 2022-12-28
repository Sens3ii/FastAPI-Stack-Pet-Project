from enum import Enum


class Gender(str, Enum):
    MAN = "MAN"
    WOMAN = "WOMAN"
    OTHER = "OTHER"


class CardKind(str, Enum):
    JUSAN = "JUSAN"
    OTHER = "OTHER"


class TransactionLogKind(str, Enum):
    TRANSFER = "TRANSFER"
    PURCHASE = "PURCHASE"
    PAYMENT = "PAYMENT"


class OrderType(str, Enum):
    ASC = "asc"
    DESC = "desc"
