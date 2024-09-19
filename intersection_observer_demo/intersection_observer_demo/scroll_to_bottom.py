import asyncio

import reflex as rx

from reflex_intersection_observer import intersection_observer


BOTTOM_ELEMENT_ID = "bottom"


class ScrollHandlingState(rx.State):
    def scroll_to_bottom(self):
        return rx.call_script(
            f"document.getElementById('{BOTTOM_ELEMENT_ID}').scrollIntoView()"
        )


class MessageGenerator(rx.State):
    messages: list[str]
    should_load: bool = False

    def on_load(self):
        self.messages = ["Hello, world!"]
        self.should_load = True
        return MessageGenerator.add_messages

    @rx.background
    async def add_messages(self):
        while self.should_load:
            async with self:
                self.messages.append(f"New message {len(self.messages) + 1}!")
                if not self.should_load:
                    break
            await asyncio.sleep(min(len(self.messages) / 20, 3))


def message_control_button():
    return rx.cond(
        MessageGenerator.should_load,
        rx.button("Stop", on_click=MessageGenerator.set_should_load(False)),
        rx.button(
            "Start",
            on_click=[
                MessageGenerator.set_should_load(True),
                MessageGenerator.add_messages,
            ],
        ),
    )


def page() -> rx.Component:
    return rx.vstack(
        rx.heading("Scroll to New Message Demo"),
        rx.hstack(
            message_control_button(),
            rx.icon_button(
                rx.icon("arrow_down_to_line"),
                on_click=ScrollHandlingState.scroll_to_bottom,
            ),
        ),
        rx.scroll_area(
            rx.vstack(
                rx.foreach(MessageGenerator.messages, rx.text),
                intersection_observer(
                    height="1px",
                    id=BOTTOM_ELEMENT_ID,
                    root="#scroller",
                    on_non_intersect=ScrollHandlingState.scroll_to_bottom(),
                    # The target object doesn't need to be visible.
                    # visibility="hidden",
                    border=f"1px solid {rx.color("accent", 12)}",
                ),
                spacing="3",
                font_size="2em",
            ),
            id="scroller",
            border=f"1px solid {rx.color("accent", 12)}",
            width="85vw",
            height="75vh",
        ),
        rx.text("This is outside scroll area"),
        rx.link("Infinite Scroll Demo", href="/"),
        align="center",
    )
