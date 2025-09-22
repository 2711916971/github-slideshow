from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, List, Optional


class HTTPException(Exception):
    def __init__(self, status_code: int, detail: str) -> None:
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"HTTP {status_code}: {detail}")


@dataclass
class Route:
    path: str
    method: str
    handler: Callable[..., Any]


class APIRouter:
    def __init__(self, prefix: str = "", tags: Optional[List[str]] = None) -> None:
        self.prefix = prefix
        self.tags = tags or []
        self.routes: List[Route] = []

    def post(self, path: str, response_model: Any | None = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            self.routes.append(Route(self.prefix + path, "POST", func))
            return func

        return decorator

    def get(self, path: str, response_model: Any | None = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            self.routes.append(Route(self.prefix + path, "GET", func))
            return func

        return decorator


class FastAPI:
    def __init__(self, title: str = "FastAPI") -> None:
        self.title = title
        self.routes: List[Route] = []
        self.startup_handlers: List[Callable[[], Any]] = []

    def include_router(self, router: APIRouter) -> None:
        self.routes.extend(router.routes)

    def on_event(self, event: str) -> Callable[[Callable[[], Any]], Callable[[], Any]]:
        if event != "startup":
            raise ValueError("Only startup event supported in stub")

        def decorator(func: Callable[[], Any]) -> Callable[[], Any]:
            self.startup_handlers.append(func)
            return func

        return decorator

    def startup(self) -> None:
        for handler in self.startup_handlers:
            handler()

    def get(self, path: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            self.routes.append(Route(path, "GET", func))
            return func

        return decorator
