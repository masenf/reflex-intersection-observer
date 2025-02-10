import reflex as rx
from reflex_intersection_observer import intersection_observer


class ForeachState(rx.State):
    messages: rx.Field[list[str]] = rx.field([])

    @rx.event
    def add_message(self):
        for _ in range(100):
            self.messages.append(f"New message {len(self.messages) + 1}!")


# When using the intersection observer inside a memoization leaf (like
# foreach/cond), it is preferred to use `rx.memo`, so the observer lifecycle is
# tied to the specific target div, rather than the parent memoization leaf.
@rx.memo
def memo_observer():
    return intersection_observer(
        "Mid Scroll Target",
        id="mid-target",
        root="#scroller",
        root_margin="0px",
        threshold=0.9,
        on_intersect=rx.toast("Mid Intersected"),
        on_non_intersect=rx.toast("Mid Non-intersected"),
    )


def page():
    return rx.vstack(
        rx.heading("Repro Foreach example"),
        rx.button("Add Message", on_click=ForeachState.add_message),
        rx.scroll_area(
            rx.vstack(
                rx.foreach(
                    ForeachState.messages,
                    lambda x, i: rx.fragment(
                        rx.cond(
                            i == ForeachState.messages.length() - 5,
                            memo_observer(),
                        ),
                        rx.text(x),
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
