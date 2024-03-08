import reflex as rx

from reflex_intersection_observer import intersection_observer


BATCH_SIZE = 15


class State(rx.State):
    items: list[str] = [f"Item {ix}" for ix in range(BATCH_SIZE)]

    def handle_intersect(self, entry):
        print(f"Intersected! {entry} Load more items.")
        self.items.extend(
            [f"Item {ix}" for ix in range(len(self.items), len(self.items) + BATCH_SIZE)]
        )


def index() -> rx.Component:
    return rx.center(
        rx.scroll_area(
            rx.vstack(
                rx.foreach(State.items, rx.text),
                intersection_observer(
                    "Infinite Scroll Target",
                    root="#scroller",
                    root_margin="0px",
                    threshold=0.9,
                    on_intersect=State.handle_intersect,
                    # The target object doesn't need to be visible.
                    # visibility="hidden"
                ),
                justify="start",
                spacing="3",
                font_size="2em",
            ),
            type="hover",
            id="scroller",
            border="1px solid black",
            width="85vw",
            height="75vh",
        ),
        padding_top="5em",
    )


app = rx.App()
app.add_page(index)