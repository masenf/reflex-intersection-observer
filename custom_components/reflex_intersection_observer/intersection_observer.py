"""Reflex custom component IntersectionObserver."""

from __future__ import annotations

import reflex as rx
from jinja2 import Environment

INTERSECTION_OBSERVER_JS = """
// reflex_intersection_observer.IntersectionObserver
const [enableObserver_{{ ref }}, setEnableObserver_{{ ref }}] = useState(1)
useEffect(() => {
    if (!{{ root }}) {
        // The root element is not found, so trigger the effect again, later.
        console.log("Warning: observation target " + {{ root }} + " not found, will try again.")
        const timeout = setTimeout(
            () => setEnableObserver_{{ ref }}((cnt) => cnt + 1),
            enableObserver_{{ ref }} * 100,
        )
        return () => clearTimeout(timeout)
    }
    const on_intersect = {{ on_intersect }}
    const on_non_intersect = {{ on_non_intersect }}
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (on_intersect !== undefined && entry.isIntersecting) {
                on_intersect(extractEntry(entry))
            }
            if (on_non_intersect !== undefined && !entry.isIntersecting) {
                on_non_intersect(extractEntry(entry))
            }
        });
    }, {
        root: {{ root }},
        rootMargin: {{ root_margin }},
        threshold: {{ threshold }},
    })
    if ({{ ref }}.current) {
        observer.observe({{ ref }}.current)
        return () => observer.disconnect()
    }
}, [ enableObserver_{{ ref }} ]);
"""


class IntersectionObserverEntry(rx.Base):
    intersection_ratio: float
    is_intersecting: bool
    time: float


def _intersect_event_signature(
    data: rx.Var[IntersectionObserverEntry],
) -> tuple[rx.Var[IntersectionObserverEntry]]:
    return (data,)


class IntersectionObserver(rx.el.Div):
    root: rx.Var[str]
    root_margin: rx.Var[str] = rx.Var.create("0px")
    threshold: rx.Var[float] = rx.Var.create(1.0)

    on_intersect: rx.EventHandler[_intersect_event_signature]
    on_non_intersect: rx.EventHandler[_intersect_event_signature]

    @classmethod
    def create(cls, *children, **props):
        if "id" not in props:
            props["id"] = rx.vars.get_unique_variable_name()
        return super().create(*children, **props)

    def _exclude_props(self) -> list[str]:
        return ["root", "root_margin", "threshold", "on_intersect", "on_non_intersect"]

    def add_imports(self) -> rx.ImportDict | list[rx.ImportDict]:
        return {
            "react": [
                rx.ImportVar(tag="useEffect"),
                rx.ImportVar(tag="useState"),
            ],
        }

    def add_custom_code(self) -> list[str]:
        return [
            """
const extractEntry = (entry) => ({
    intersection_ratio: entry.intersectionRatio,
    is_intersecting: entry.isIntersecting,
    time: entry.time,
})"""
        ]

    def add_hooks(self) -> list[str | rx.Var]:
        on_intersect = self.event_triggers.get("on_intersect")
        on_non_intersect = self.event_triggers.get("on_non_intersect")
        if on_intersect is None and on_non_intersect is None:
            return []
        on_intersect = (
            rx.Var.create(on_intersect) if on_intersect is not None else "undefined"
        )
        on_non_intersect = (
            rx.Var.create(on_non_intersect)
            if on_non_intersect is not None
            else "undefined"
        )
        return [
            Environment()
            .from_string(INTERSECTION_OBSERVER_JS)
            .render(
                on_intersect=on_intersect,
                on_non_intersect=on_non_intersect,
                root=(
                    f"document.querySelector({self.root!s})"
                    if self.root is not None
                    else "document"
                ),
                root_margin=self.root_margin,
                threshold=self.threshold,
                ref=self.get_ref(),
            )
        ]


intersection_observer = IntersectionObserver.create
