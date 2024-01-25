from dataclasses import dataclass


@dataclass
class UserLevelError:
    message: str


@dataclass
class ItemLevelError:
    item_id: int
    message: str


ValidationError = UserLevelError | ItemLevelError
