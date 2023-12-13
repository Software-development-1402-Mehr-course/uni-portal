from dataclasses import dataclass
from typing import Optional

from django.http import HttpRequest


@dataclass
class HTMXHeaders:
    boosted: bool
    current_url: str
    history_restore_request: bool
    prompt: Optional[str]
    target: str
    trigger_name: str
    trigger: Optional[str]

    @classmethod
    def from_request(cls, request: HttpRequest):
        if request.headers.get("HX-Request") != "true":
            return

        headers = request.headers
        return cls(
            headers.get("HX-Boosted") == "true",
            headers["HX-Current-URL"],
            headers.get("HX-History-Restore-Request") == "true",
            headers.get("HX-Prompt"),
            headers["HX-Target"],
            headers["HX-Trigger-Name"],
            headers.get("HX-Trigger"),
        )
