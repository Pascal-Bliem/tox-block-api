from flask import Flask
from tox_block_api.config import get_logger, Config


_logger = get_logger(logger_name=__name__)


def create_app(config_object: Config) -> Flask:
    """Create a flask app instance."""

    flask_app = Flask("tox_block_api")
    flask_app.config.from_object(config_object)

    # import blueprints
    from tox_block_api.controller import tox_block_app
    flask_app.register_blueprint(tox_block_app)
    _logger.debug("Application instance created")

    return flask_app
