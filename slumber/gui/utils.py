from PySide6.QtWidgets import QWidget

from slumber import settings


def _scale_widget(widget: QWidget, scale_factor: float) -> None:
    if not hasattr(widget, "setZoomFactor"):
        font = widget.font()
        current_size = font.pointSizeF()
        if current_size > 0:
            font.setPointSizeF(current_size * scale_factor)
            widget.setFont(font)
    else:  # For QWebView/QWebEngineView
        widget.setZoomFactor(scale_factor)


def scale_widget(
    widget: QWidget, scale_factor: float = settings["gui"]["scale_factor"]
) -> None:
    """Utility function to scale fonts for a widget and its children"""
    # Handle the parent widget itself
    _scale_widget(widget, scale_factor)

    # Handle all child widgets
    for child_widget in widget.findChildren(QWidget):
        _scale_widget(child_widget, scale_factor)
