# intersection-observer

React to a component coming into view using Reflex event handler.

## Installation

```bash
pip install reflex-intersection-observer
```

## Usage

```python
import reflex as rx

from reflex_intersection_observer import intersection_observer

def index():
    return rx.vstack(
        rx.box(height="150vh"), 
        intersection_observer(
            on_intersect=rx.console.log("Component visible!"),
        ),
    )
```