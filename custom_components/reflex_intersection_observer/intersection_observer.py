"""Reflex custom component IntersectionObserver."""

from jinja2 import Environment

import reflex as rx


INTERSECTION_OBSERVER_JS = """
// reflex_intersection_observer.IntersectionObserver
useEffect(() => {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if ({{ on_intersect }} && entry.isIntersecting) {
                {{ on_intersect }}(extractEntry(entry))
            }
            if ({{ on_non_intersect }} && !entry.isIntersecting) {
                {{ on_non_intersect }}(extractEntry(entry))
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
}, []);
"""


class IntersectionObserver(rx.el.Div):
    root: rx.Var[str]
    root_margin: rx.Var[str]
    threshold: rx.Var[float]

    on_intersect: rx.EventHandler[lambda e0: [e0]]
    on_non_intersect: rx.EventHandler[lambda e0: [e0]]

    @classmethod
    def create(cls, *children, **props):
        if "id" not in props:
            props["id"] = rx.vars.get_unique_variable_name()
        return super().create(*children, **props)

    def _exclude_props(self) -> list[str]:
        return ["root", "root_margin", "threshold", "on_intersect", "on_non_intersect"]

    def _get_imports(self) -> dict[str, list[rx.utils.imports.ImportVar]]:
        return rx.utils.imports.merge_imports(
            super()._get_imports(),
            {
                "react": [rx.utils.imports.ImportVar(tag="useEffect")],
            },
        )

    def _get_custom_code(self) -> str | None:
        return """
const extractEntry = (entry) => ({
    intersection_ratio: entry.intersectionRatio,
    is_intersecting: entry.isIntersecting,
    time: entry.time,
})"""

    def _get_hooks(self) -> str | None:
        on_intersect = self.event_triggers.get("on_intersect")
        on_non_intersect = self.event_triggers.get("on_non_intersect")
        if on_intersect is None and on_non_intersect is None:
            return None
        if isinstance(on_intersect, rx.EventChain):
            on_intersect = rx.utils.format.wrap(
                rx.utils.format.format_prop(on_intersect).strip("{}"),
                "(",
            )
        if isinstance(on_non_intersect, rx.EventChain):
            on_non_intersect = rx.utils.format.wrap(
                rx.utils.format.format_prop(on_non_intersect).strip("{}"),
                "(",
            )
        if on_intersect is None:
            on_intersect = "undefined"
        if on_non_intersect is None:
            on_non_intersect = "undefined"
        return (
            Environment()
            .from_string(INTERSECTION_OBSERVER_JS)
            .render(
                on_intersect=on_intersect,
                on_non_intersect=on_non_intersect,
                root=(
                    f"document.querySelector({rx.utils.format.format_prop(self.root).strip('{}')})"
                    if self.root is not None
                    else "null"
                ),
                root_margin=rx.utils.format.format_prop(
                    self.root_margin if self.root_margin is not None else "0px"
                ).strip("{}"),
                threshold=(
                    self.threshold._var_name_unwrapped
                    if self.threshold is not None
                    else "1.0"
                ),
                ref=self.get_ref(),
            )
        )


intersection_observer = IntersectionObserver.create
