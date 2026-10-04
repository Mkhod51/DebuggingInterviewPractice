"""Tenant authorization and route selection."""
from dataclasses import dataclass


class RoutingError(ValueError):
    pass


@dataclass(frozen=True)
class Route:
    default: str
    allowed: frozenset
    fallback: str | None = None

    def __post_init__(self):
        if self.default not in self.allowed or (self.fallback is not None and self.fallback not in self.allowed):
            raise ValueError("Routes must be authorized")

    @classmethod
    def from_dict(cls, row):
        return cls(row["default"], frozenset(row["allowed"]), row.get("fallback"))

    def as_dict(self):
        return dict(default=self.default, allowed=sorted(self.allowed), fallback=self.fallback)


@dataclass(frozen=True)
class Selection:
    primary: str
    fallback: str | None


class Router:
    def __init__(self, routes):
        self._routes = dict(routes)

    def select(self, request):
        if request.tenant not in self._routes:
            raise RoutingError("Unknown tenant")
        route = self._routes[request.tenant]
        selected = route.default
        if selected not in route.allowed:
            raise RoutingError("Unauthorized model")
        fallback = route.fallback if route.fallback != selected else None
        return Selection(selected, fallback)

    def tenants(self):
        return tuple(sorted(self._routes))

    def export(self):
        return {tenant: route.as_dict() for tenant, route in sorted(self._routes.items())}
