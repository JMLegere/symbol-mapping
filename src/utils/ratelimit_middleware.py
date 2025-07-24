from __future__ import annotations

from collections import deque
from typing import Deque
import asyncio
import time

from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.types import ASGIApp


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory rate limiting middleware."""

    def __init__(
        self, app: ASGIApp, max_requests: int, window_seconds: int
    ) -> None:
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._timestamps: Deque[float] = deque()
        self._lock = asyncio.Lock()

    async def dispatch(self, request: Request, call_next):
        now = time.monotonic()
        async with self._lock:
            while (
                self._timestamps
                and now - self._timestamps[0] > self.window_seconds
            ):
                self._timestamps.popleft()
            if len(self._timestamps) >= self.max_requests:
                return JSONResponse(
                    {"detail": "Too Many Requests"}, status_code=429
                )
            self._timestamps.append(now)
        return await call_next(request)
