from enum import Enum


class LogType(Enum):
    BOOK = "book"
    USER = "user"

class LogAction(Enum):
    EDIT = "edit"
    DELETE = "delete"
    CREATE = "create"

class BookStatus(Enum):
    STOCK = "stock"
    ISSUED = "issued"

