from dataclasses import dataclass


class HXViewMixin:
    @dataclass
    class HXHeaders:
        boosted: bool
        current_url: str
        history_restore_request: bool
        prompt: str
        target: str
        trigger_name: str
        trigger: str

    def is_hx_request(self, request) -> bool:
        return request.headers.get("HX-Request") == "true"

    def hx_headers(self, request):
        h = request.headers

        return self.HXHeaders(
            h["HX-Boosted"] == "true",
            h["HX-Current-URL"],
            h["HX-History-Restore-Request"] == "true",
            h["HX-Prompt"],
            h["HX-Target"],
            h["HX-Trigger-Name"],
            h["HX-Trigger"],
        )
