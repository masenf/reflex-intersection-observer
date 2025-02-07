import reflex as rx

from reflex_intersection_observer import intersection_observer


BOTTOM_ELEMENT_ID = "bottom"


def page():
    return rx.vstack(
        rx.heading("Repro Foreach example"),
        rx.scroll_area(
            rx.vstack(
                rx.foreach([f"item {x}" for x in range(10)], rx.text),
                rx.foreach(
                    [1],
                    lambda _: intersection_observer(
                        "Infinite Scroll Target",
                        id=BOTTOM_ELEMENT_ID,
                        root="#scroller",
                        root_margin="0px",
                        threshold=0.9,
                        on_intersect=rx.toast("Intersected"),
                        on_non_intersect=rx.toast("Non-intersected"),
                        # The target object doesn't need to be visible.
                        # visibility="hidden"
                    ),
                ),
                justify="start",
                spacing="3",
                font_size="2em",
            ),
            type="hover",
            id="scroller",
            border=f"1px solid {rx.color('accent', 12)}",
            width="85vw",
            height="75vh",
        ),
        align="center",
    )