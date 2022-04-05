"""Sphinx extension for resizing your RTD theme"""

from typing import Any, Union
from pathlib import Path
import importlib.metadata

from sphinx.application import Sphinx
from sphinx.config import Config
from sphinx.util import logging


def add_html_static(app: Sphinx, static_path: str) -> None:
    """
    Add the given path as static html/resource to the sphinx app.

    :param app: The sphinx app to add to.
    :param static_path: The path to add.
    """

    # Set a callback to after the builder of the site was inited,
    # The callback will register our static path to the app.
    def _add_static(_app):
        if _app.config.html_static_path is None:
            _app.config.html_static_path = []

        _app.config.html_static_path.append(
            str(Path(__file__).parent.joinpath(static_path).absolute())
            )

    app.connect("builder-inited", _add_static)


def add_config_value(app: Sphinx, name: str, default: Any,
                     rebuild: Union[bool, str], types: Any = ()) -> None:
    """
    Declare a configuration value for this extension,
    And make it available for any templates.

    :param app: The sphinx app to declare to.
    :param name: The name of the configuration.
    :param default: The default value of the configuration.
    :param rebuild: Whether to rebuild the site when this configuration changes.
    :param types: The expected type of the configuration.
    """

    # Add the configuration.
    app.add_config_value(name=name, default=default, rebuild=rebuild, types=types)

    # Set a callback to after the configuration was received,
    # The callback shall make the configuration available to the templates.
    def _add_to_context(_app: Sphinx, config: Config):
        if config.html_context is None:
            config.html_context = {}

        config.html_context.update({name: config[name]})

    app.connect("config-inited", _add_to_context)


def setup(app: Sphinx) -> dict:
    """
    Resize the RTD theme by given configuration.

    :param app: The sphinx app to resize.
    :return: Extension MetaData.
    """

    # Log that we started.
    logging.getLogger(__name__).verbose("Resizing RTD...")

    # Add our static files to sphinx.
    add_html_static(app, "_static")

    # Register our configurations (so it may be used in templates).
    add_config_value(app, name='sphinx_rtd_size_width', default=None, rebuild='html', types=[str])

    # Configure the entire site to import our css file.
    app.add_css_file("css/sphinx_rtd_size.css")

    return {
        'version': importlib.metadata.version('sphinx_rtd_size'),
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
