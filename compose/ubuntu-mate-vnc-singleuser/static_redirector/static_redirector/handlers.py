"""API handlers for the Jupyter Server example."""

from jupyter_server.base.handlers import JupyterHandler
from jupyter_server.extension.handler import ExtensionHandlerJinjaMixin, ExtensionHandlerMixin


class BaseTemplateHandler(ExtensionHandlerJinjaMixin, ExtensionHandlerMixin, JupyterHandler):
    """A base template handler."""


class IndexHandler(BaseTemplateHandler):
    """The root API handler."""

    def get(self):
        """Get the root response."""
        self.write(self.render_template("index.html", destination=self.config.destination))


class ErrorHandler(BaseTemplateHandler):
    """An error handler."""

    def get(self, path):
        """Handle the error."""
        self.write_error(400)
