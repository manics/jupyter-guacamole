"""The extension entry point."""

from .application import Redirector


def _jupyter_server_extension_points():
    return [
        {"module": "static_redirector.application", "app": Redirector},
    ]


_jupyter_server_extension_paths = _jupyter_server_extension_points
