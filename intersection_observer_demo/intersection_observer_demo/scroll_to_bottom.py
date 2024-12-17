import reflex as rx

from reflex_intersection_observer import intersection_observer


BOTTOM_ELEMENT_ID = "bottom"
INITIAL_UPDATE_INTERVAL_MS = 200


class MessageGenerator(rx.State):
    messages: list[str] = ["Hello, world!"]
    update_interval_ms: int = INITIAL_UPDATE_INTERVAL_MS

    @rx.event
    def add_message(self):
        self.messages.append(f"New message {len(self.messages) + 1}!")
        if self.update_interval_ms > 0:
            self.update_interval_ms = int(min(len(self.messages) / 20, 3) * 1000)


def message_control_button():
    return rx.cond(
        MessageGenerator.update_interval_ms > 0,
        rx.button("Stop", on_click=MessageGenerator.set_update_interval_ms(0)),
        rx.button(
            "Start",
            on_click=[
                MessageGenerator.set_update_interval_ms(INITIAL_UPDATE_INTERVAL_MS),
            ],
        ),
    )


def page() -> rx.Component:
    return rx.vstack(
        rx.heading("Scroll to New Message Demo"),
        rx.hstack(
            message_control_button(),
            rx.icon_button(
                rx.icon("plus"),
                on_click=MessageGenerator.add_message,
            ),
            rx.icon_button(
                rx.icon("arrow_down_to_line"),
                on_click=rx.scroll_to(BOTTOM_ELEMENT_ID),
            ),
        ),
        rx.scroll_area(
            rx.vstack(
                rx.foreach(MessageGenerator.messages, rx.text),
                intersection_observer(
                    height="1px",
                    id=BOTTOM_ELEMENT_ID,
                    root="#scroller",
                    # Remove lambda after reflex-dev/reflex#4552
                    on_non_intersect=lambda _: rx.scroll_to(BOTTOM_ELEMENT_ID),
                    # The target object doesn't need to be visible.
                    # visibility="hidden",
                    border=f"1px solid {rx.color('accent', 12)}",
                ),
                spacing="3",
                font_size="2em",
            ),
            id="scroller",
            border=f"1px solid {rx.color('accent', 12)}",
            width="85vw",
            height="75vh",
        ),
        rx.moment(
            interval=MessageGenerator.update_interval_ms,
            on_change=MessageGenerator.add_message.temporal,
            display="none",
        ),
        rx.text("This is outside scroll area"),
        rx.link("Infinite Scroll Demo", href="/"),
        align="center",
    )
