import io
import json
import math
import os

from tox_block import __version__ as _version
from tox_block.config import config as model_config
from tox_block_api import __version__ as api_version

def test_health(flask_test_client):
    # action
    response = flask_test_client.get("/health")

    # assertion
    assert response.status_code == 200


def test_version(flask_test_client):
    # action
    response = flask_test_client.get("/version")

    # assertion
    assert response.status_code == 200
    response_json = json.loads(response.data)
    assert response_json["model_version"] == _version
    assert response_json["api_version"] == api_version

def test_api_make_predictions(flask_test_client):
    # setup 
    nontoxic_texts = ["Good morning my friend, I hope you're having a fantastic day!"]
    toxic_texts = ["I will kill you, you fucking idiot!"]

    # action
    res_nontoxic = flask_test_client.post("/v1/make_predictions",
                                          json={"input_data": nontoxic_texts})
    res_toxic = flask_test_client.post("/v1/make_predictions",
                                          json={"input_data": toxic_texts})

    # assertion
    for response in [res_nontoxic, res_toxic]:
        assert response.status_code == 200
        response_json = json.loads(response.data)
        prediction = response_json["predictions"]["0"]
        for key in ["text"] + model_config.LIST_CLASSES:
            assert key in prediction
        model_version = response_json["model_version"]
        api_v = response_json["api_version"]
        assert model_version == _version
        assert api_v == api_version
    
    # check predicted probabilities are always below 10% for non-toxic text
    pred_nontoxic = json.loads(res_nontoxic.data)["predictions"]["0"]
    for key in model_config.LIST_CLASSES:
        assert pred_nontoxic[key] < 0.1

    # check any of the predicted probabilities is above 80% for toxic text
    pred_toxic = json.loads(res_toxic.data)["predictions"]["0"]
    assert any([pred_toxic[key] > 0.8 for key in model_config.LIST_CLASSES])

def test_api_make_single_prediction(flask_test_client):
    # setup 
    nontoxic_text = "Good morning my friend, I hope you're having a fantastic day!"
    toxic_text = "I will kill you, you fucking idiot!"

    # action
    res_nontoxic = flask_test_client.post("/v1/make_single_prediction",
                                          json={"input_data": nontoxic_text})
    res_toxic = flask_test_client.post("/v1/make_single_prediction",
                                          json={"input_data": toxic_text})

    # assertion
    for response in [res_nontoxic, res_toxic]:
        assert response.status_code == 200
        response_json = json.loads(response.data)
        prediction = response_json["predictions"]
        for key in ["text"] + model_config.LIST_CLASSES:
            assert key in prediction
        model_version = response_json["model_version"]
        api_v = response_json["api_version"]
        assert model_version == _version
        assert api_v == api_version
    
    # check predicted probabilities are always below 10% for non-toxic text
    pred_nontoxic = json.loads(res_nontoxic.data)["predictions"]
    for key in model_config.LIST_CLASSES:
        assert pred_nontoxic[key] < 0.1

    # check any of the predicted probabilities is above 80% for toxic text
    pred_toxic = json.loads(res_toxic.data)["predictions"]
    assert any([pred_toxic[key] > 0.8 for key in model_config.LIST_CLASSES])
