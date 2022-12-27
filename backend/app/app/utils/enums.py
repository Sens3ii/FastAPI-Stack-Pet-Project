from enum import Enum


class Gender(str, Enum):
    MAN = "MAN"
    WOMAN = "WOMAN"
    OTHER = "OTHER"


class OrderStatus(str, Enum):
    WAITING = "WAITING"
    PURCHASED = "PURCHASED"
    CANCELED = "CANCELED"
