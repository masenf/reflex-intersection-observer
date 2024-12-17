import reflex as rx

from reflex_intersection_observer import intersection_observer

from . import readme, scroll_to_bottom


BATCH_SIZE = 15
BOTTOM_ELEMENT_ID = "bottom"


class State(rx.State):
    items: list[str] = [f"Item {ix}" for ix in range(BATCH_SIZE)]

    def reset_items(self):
        self.reset()

    def handle_intersect(self, entry):
        print(f"Intersected! {entry} Load more items.")
        self.items.extend(
            [
                f"Item {ix}"
                for ix in range(len(self.items), len(self.items) + BATCH_SIZE)
            ]
        )

    def handle_non_intersect(self, entry):
        print(f"Non-intersected! {entry}")


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
                on_click=rx.call_script(
                    f"document.getElementById('{BOTTOM_ELEMENT_ID}').scrollIntoView()"
                ),
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
                    # visibility="hidden"
                ),
                justify="start",
                spacing="3",
                font_size="2em",
            ),
            type="hover",
            id="scroller",
            border=f"1px solid {rx.color("accent", 12)}",
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
    on_load=scroll_to_bottom.MessageGenerator.on_load,
)
app.add_page(
    readme.page,
    route="/readme",
)
