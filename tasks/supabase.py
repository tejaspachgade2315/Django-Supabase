"""Supabase REST (PostgREST) client helpers.

This project uses Supabase via its HTTPS REST API so it can work even when
direct Postgres connections (port 5432) are blocked.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests
from django.conf import settings


class SupabaseConfigError(RuntimeError):
    pass


class SupabaseRequestError(RuntimeError):
    def __init__(self, status_code: int, detail: Any):
        super().__init__(f"Supabase request failed with status {status_code}")
        self.status_code = status_code
        self.detail = detail


def _parse_total_count(content_range: str | None) -> int:
    if not content_range:
        return 0
    # Examples: "0-0/12" or "*/12"
    if "/" not in content_range:
        return 0
    total_part = content_range.split("/", 1)[1].strip()
    try:
        return int(total_part)
    except ValueError:
        return 0


@dataclass(frozen=True)
class SupabaseRestClient:
    rest_url: str
    anon_key: str
    timeout_seconds: int = 15

    @classmethod
    def from_django_settings(cls) -> "SupabaseRestClient":
        url = getattr(settings, "SUPABASE_URL", "") or ""
        anon_key = getattr(settings, "SUPABASE_ANON_KEY", "") or ""
        if not url or not anon_key:
            raise SupabaseConfigError("SUPABASE_URL and SUPABASE_ANON_KEY must be set")

        rest_url = url.rstrip("/") + "/rest/v1"
        return cls(rest_url=rest_url, anon_key=anon_key)

    def _headers(self, *, prefer: str | None = None) -> dict[str, str]:
        headers = {
            "apikey": self.anon_key,
            "Authorization": f"Bearer {self.anon_key}",
            "Content-Type": "application/json",
        }
        if prefer:
            headers["Prefer"] = prefer
        return headers

    def request(
        self,
        method: str,
        table: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any | None = None,
        prefer: str | None = None,
    ) -> tuple[Any | None, dict[str, str]]:
        url = f"{self.rest_url}/{table}"
        response = requests.request(
            method=method.upper(),
            url=url,
            headers=self._headers(prefer=prefer),
            params=params,
            json=json,
            timeout=self.timeout_seconds,
        )

        if response.status_code >= 400:
            try:
                detail: Any = response.json()
            except ValueError:
                detail = response.text
            raise SupabaseRequestError(status_code=response.status_code, detail=detail)

        headers = dict(response.headers)
        if response.status_code == 204 or method.upper() == "HEAD" or not response.content:
            return None, headers

        return response.json(), headers

    def count(self, table: str, *, filters: dict[str, str] | None = None) -> int:
        params: dict[str, Any] = {"select": "id"}
        if filters:
            params.update(filters)

        _data, headers = self.request("HEAD", table, params=params, prefer="count=exact")
        return _parse_total_count(headers.get("Content-Range"))
