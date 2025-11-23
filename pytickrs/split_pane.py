from typing import Any

from textual import events
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.geometry import Offset, Size
from textual.widget import Widget
from textual.widgets import Rule, Static


class SplitContainerSeparator(Rule):
    pass


class SplitContainer(Horizontal, inherit_bindings=False):
    """
    From https://github.com/Textualize/textual/discussions/4834
    """

    _separator_grabbed: bool = False
    _offset_before_dragged: Offset | None = None
    _size_before_dragged: Size | None = None

    def __init__(self, before: Widget, after: Widget) -> None:
        super().__init__()
        self.before = before
        self.after = after
        self.before.styles.width = '1fr'
        self.after.styles.width = '1fr'

    def compose(self) -> ComposeResult:
        yield self.before
        yield SplitContainerSeparator('vertical')
        yield self.after

    def on_mouse_down(self, event: events.MouseDown) -> None:
        widget, _ = self.screen.get_widget_at(event.screen_x, event.screen_y)
        if isinstance(widget, SplitContainerSeparator):
            self._separator_grabbed = True
            self._offset_before_dragged = event.screen_offset
            self._size_before_dragged = self.before.size

    def on_mouse_move(self, event: events.MouseMove) -> None:
        if self._separator_grabbed:
            assert self._size_before_dragged is not None
            dragged_offset = event.screen_offset - self._offset_before_dragged
            new_dragged_width = self._size_before_dragged.width + dragged_offset.x
            self.before.styles.width = new_dragged_width
        return

    def on_mouse_up(self) -> None:
        self._separator_grabbed = False
        self._offset_before_dragged = None
        self._size_before_dragged = None


class SplitContainerApp(App):
    CSS = """
    SplitContainer {
        width: 100%;
        height: 100%;
    }
    """

    def compose(self) -> ComposeResult:
        yield SplitContainer(
            before=Static('This is some content to the left.'),
            after=Static('This is some content to the right.'),
        )


if __name__ == '__main__':
    app = SplitContainerApp()
    app.run()
