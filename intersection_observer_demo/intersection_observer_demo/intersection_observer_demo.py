import reflex as rx
from reflex_intersection_observer import (
    IntersectionObserverEntry,
    intersection_observer,
)

from . import readme, repro_foreach, scroll_to_bottom

BATCH_SIZE = 15
BOTTOM_ELEMENT_ID = "bottom"


class State(rx.State):
    items: rx.Field[list[str]] = rx.field([f"Item {ix}" for ix in range(BATCH_SIZE)])

    @rx.event
    def reset_items(self):
        self.reset()

    @rx.event
    def handle_intersect(self, entry: IntersectionObserverEntry):
        print(f"Intersected! {entry} Load more items.")  # noqa: T201
        self.items.extend(
            [
                f"Item {ix}"
                for ix in range(len(self.items), len(self.items) + BATCH_SIZE)
            ]
        )

    @rx.event
    def handle_non_intersect(self, entry: IntersectionObserverEntry):
        print(f"Non-intersected! {entry}")  # noqa: T201


def index() -> rx.Component:
    return rx.vstack(
        rx.heading("Infinite Scroll Demo"),
        rx.hstack(
            rx.text(f"{State.items.length()} items"),
            rx.icon_button(
                rx.icon("rotate-ccw"),
                on_click=State.reset_items,
            ),
            rx.icon_button(
                rx.icon("arrow_down_to_line"),
                on_click=rx.scroll_to(BOTTOM_ELEMENT_ID),
            ),
        ),
        rx.scroll_area(
            rx.vstack(
                rx.foreach(State.items, rx.text),
                intersection_observer(
                    "Infinite Scroll Target",
                    id=BOTTOM_ELEMENT_ID,
                    root="#scroller",
                    root_margin="0px",
                    threshold=0.9,
                    on_intersect=State.handle_intersect,
                    on_non_intersect=State.handle_non_intersect,
                    # The target object doesn't need to be visible.
                    # visibility="hidden"  # noqa: ERA001
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
        rx.text("This is outside scroll area"),
        rx.link("Scroll to Bottom Demo", href="/scroll-to-bottom"),
        align="center",
    )


app = rx.App()
app.add_page(index)
app.add_page(
    scroll_to_bottom.page,
    route="/scroll-to-bottom",
)
app.add_page(
    readme.page,
    route="/readme",
)
app.add_page(
    repro_foreach.page,
    route="/repro-foreach",
)
