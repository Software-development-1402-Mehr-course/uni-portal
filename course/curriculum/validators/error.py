from dataclasses import dataclass


@dataclass
class ListLevelError:
    message: str


@dataclass
class ItemLevelError:
    item_id: int
    message: str


ValidationError = ListLevelError | ItemLevelError
