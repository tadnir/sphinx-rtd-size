from typing import Any, Union
from pathlib import Path
import importlib.metadata

from sphinx.application import Sphinx
from sphinx.config import Config
from sphinx.util import logging


def add_html_static(app: Sphinx, static_path: str) -> None:
    def _add_static(_app):
        if _app.config.html_static_path is None:
            _app.config.html_static_path = []

        _app.config.html_static_path.append(
            str(Path(__file__).parent.joinpath(static_path).absolute())
            )

    app.connect("builder-inited", _add_static)


def add_config_value(app: Sphinx, name: str, default: Any, rebuild: Union[bool, str], types: Any = ()) -> None:
    app.add_config_value(name=name, default=default, rebuild=rebuild, types=types)

    def _add_to_context(_app: Sphinx, config: Config):
        if config.html_context is None:
            config.html_context = {}

        config.html_context.update({name: config[name]})

    app.connect("config-inited", _add_to_context)


def setup(app: Sphinx) -> dict:
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
