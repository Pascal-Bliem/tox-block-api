from flask import Blueprint, request, jsonify, abort
from tox_block.prediction import make_single_prediction, make_predictions
from tox_block import __version__ as _version
import os
from tox_block_api.config import get_logger
from tox_block_api.validation import validate_multiple_inputs, validate_single_input
from tox_block_api import __version__ as api_version


_logger = get_logger(logger_name=__name__)

tox_block_app = Blueprint("tox_block_app", __name__)

@tox_block_app.route("/health", methods=["GET"])
def health():
    if request.method == "GET":
        _logger.info("Health status OK :)")
        return "ok"

@tox_block_app.route("/version", methods=["GET"])
def version():
    if request.method == "GET":
        return jsonify({"model_version": _version,
                        "api_version": api_version})

@tox_block_app.route("/v1/make_predictions", methods=["POST"])
def api_make_predictions():
    if request.method == "POST":
        # Step 1: Extract POST data from request body as JSON
        input_json = request.get_json()
        _logger.debug(f"Inputs: {input_json}")
        
        # Step 2: Validate the input using marshmallow schema
        input_data, errors = validate_multiple_inputs(input=input_json)
        if not errors is None:
            abort(400, f"Errors occurred when validating the input data: {errors}")

        # Step 3: Model prediction
        prediction = make_predictions(input_texts=input_data)
        _logger.debug(f'Outputs: {prediction}')

        # Step 5: Return the response as JSON
        return jsonify({"predictions": prediction,
                        "model_version": _version,
                        "api_version": api_version,
                        })
        
@tox_block_app.route("/v1/make_single_prediction", methods=["POST"])
def api_make_single_prediction():
    if request.method == "POST":
        # Step 1: Extract POST data from request body as JSON
        input_json = request.get_json()
        _logger.debug(f"Inputs: {input_json}")
        
        # Step 2: Validate the input using marshmallow schema
        input_data, errors = validate_single_input(input=input_json)
        if not errors is None:
            abort(400, f"Errors occurred when validating the input data: {errors}")

        # Step 3: Model prediction
        prediction = make_single_prediction(input_text=input_data)
        _logger.debug(f'Outputs: {prediction}')

        # Step 5: Return the response as JSON
        return jsonify({"predictions": prediction,
                        "model_version": _version,
                        "api_version": api_version,
                        })