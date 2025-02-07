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
            on_intersect=rx.console_log,
        ),
    )
```

See [intersection_observer_demo](./intersection_observer_demo/) app for further examples.

### Props

The following props are understood by `intersection_observer`:

* `root` - ID of the element that is used as the viewport for checking
  visibility of the target. Must be the id of a parent of the target. Default is
  the browser viewport.
* `root_margin` - An offset rectangle applied to the root's bounding box when
  calculating intersections, effectively shrinking or growing the root for
  calculation purposes. The value returned by this property may not be the same
  as the one specified when calling the constructor as it may be changed to
  match internal requirements. Each offset can be expressed in pixels (px) or as
  a percentage (%). The default is "0px 0px 0px 0px".
* `threshold` - value between 0 and 1 indicating the percentage that should be
  visible before the event is triggered. Default is 1.

The following events are emitted by `intersection_observer`:

* `on_intersect` - fired when the target element intersects with the root element.
* `on_non_intersect` - fired when the target element does not intersect with the root element.

Both of these events provide an `IntersectionObserverEntry` with intersection details:

* `intersection_ratio`: how much of the target element is intersection (0 - 1).
* `is_intersecting`: true/false based on whether the observer is intersecting or not
* `time`: relative timestamp when the intersection occurred

See [IntersectionObserver API](https://developer.mozilla.org/en-US/docs/Web/API/IntersectionObserver)
docs on MDN for more information about how the API works.