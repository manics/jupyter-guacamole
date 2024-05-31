"""A simple Jupyter Server extension example."""

import os

from traitlets import Unicode

from jupyter_server.extension.application import ExtensionApp, ExtensionAppJinjaMixin

from .handlers import ErrorHandler, IndexHandler

DEFAULT_STATIC_FILES_PATH = os.path.join(os.path.dirname(__file__), "static")
DEFAULT_TEMPLATE_FILES_PATH = os.path.join(os.path.dirname(__file__), "templates")


class Redirector(ExtensionAppJinjaMixin, ExtensionApp):
    """A simple application."""

    # The name of the extension.
    name = "static_redirector"

    # The url that your extension will serve its homepage.
    extension_url = "/static_redirector"

    # Should your extension expose other server extensions when launched directly?
    load_other_extensions = False

    # Local path to static files directory.
    static_paths = [DEFAULT_STATIC_FILES_PATH]  # type:ignore[assignment]

    # Local path to templates directory.
    template_paths = [DEFAULT_TEMPLATE_FILES_PATH]  # type:ignore[assignment]

    destination = Unicode(os.getenv("STATIC_REDIRECTOR_DESTINATION", ""), config=True, help="Redirect destination.")

    def initialize_handlers(self):
        """Initialize handlers."""
        self.handlers.extend(
            [
                (r"/static_redirector/?", IndexHandler),
                (r"/static_redirector/(.*)", ErrorHandler),
            ]
        )

    def initialize_settings(self):
        """Initialize settings."""
        self.log.info(f"Config {self.config}")


# -----------------------------------------------------------------------------
# Main entry point
# -----------------------------------------------------------------------------

main = launch_new_instance = Redirector.launch_instance
