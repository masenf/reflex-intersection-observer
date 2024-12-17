import reflex as rx

from reflex_intersection_observer import intersection_observer


def page():
    return rx.vstack(
        rx.box(height="150vh"),
        intersection_observer(
            on_intersect=rx.console_log,
        ),
    )
