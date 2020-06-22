import json


def test_validate_multiple_inputs(flask_test_client):
    
    # setup
    no_list = 123
    list_with_empty_string = ["a","","b"]
    list_with_no_string = ["a",1,"b"]
    empty_list = []
    valid_list_of_strings = ["Hi","I'm","Pascal"]

    # action
    res_no_list = flask_test_client.post("/v1/make_predictions",
                                         json={"input_data": no_list})
    res_list_with_empty_string = flask_test_client.post("/v1/make_predictions",
                                         json={"input_data": list_with_empty_string})
    res_list_with_no_string = flask_test_client.post("/v1/make_predictions",
                                          json={"input_data": list_with_no_string})
    res_empty_list = flask_test_client.post("/v1/make_predictions",
                                          json={"input_data": empty_list})
    res_wrong_key = flask_test_client.post("/v1/make_predictions",
                                          json={"wrong_key": valid_list_of_strings})
    res_valid_list_of_strings = flask_test_client.post("/v1/make_predictions",
                                          json={"input_data": valid_list_of_strings})
    
    # assertions
    assert res_no_list.status_code == 400
    assert res_no_list.data == b"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>400 Bad Request</title>
<h1>Bad Request</h1>
<p>Errors occurred when validating the input data: The passed object is not a list of strings.</p>
"""
    assert res_list_with_empty_string.status_code == 400
    assert res_list_with_empty_string.data == b"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>400 Bad Request</title>
<h1>Bad Request</h1>
<p>Errors occurred when validating the input data: The list item at position 1 is an empty string.</p>
"""
    assert res_list_with_no_string.status_code == 400
    assert res_list_with_no_string.data == b"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>400 Bad Request</title>
<h1>Bad Request</h1>
<p>Errors occurred when validating the input data: The list item at position 1 is not a string.</p>
"""
    assert res_empty_list.status_code == 400
    assert res_empty_list.data == b"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>400 Bad Request</title>
<h1>Bad Request</h1>
<p>Errors occurred when validating the input data: Passed an empty list.</p>
"""
    assert res_wrong_key.status_code == 400
    assert res_wrong_key.data == b"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>400 Bad Request</title>
<h1>Bad Request</h1>
<p>Errors occurred when validating the input data: &quot;The key 'input_data' was not found in the received JSON.&quot;</p>
"""
    assert res_valid_list_of_strings.status_code == 200
    valid_response = res_valid_list_of_strings.get_json()
    api_version = valid_response.get("api_version", None)
    model_version = valid_response.get("model_version", None)
    predictions = valid_response.get("predictions", None)
    assert not api_version is None
    assert not model_version is None
    assert not predictions is None
    assert len(predictions) == len(valid_list_of_strings)


def test_validate_single_input(flask_test_client):
    
    # setup
    no_string = 123
    empty_string = ""
    valid_string = "Hi, I'm Pascal"
    
    # action
    res_no_string = flask_test_client.post("/v1/make_single_prediction",
                                         json={"input_data": no_string})
    res_empty_string = flask_test_client.post("/v1/make_single_prediction",
                                         json={"input_data": empty_string})
    res_valid_string = flask_test_client.post("/v1/make_single_prediction",
                                         json={"input_data": valid_string})
    
    # assertions
    assert res_no_string.status_code == 400
    assert res_no_string.data == b"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>400 Bad Request</title>
<h1>Bad Request</h1>
<p>Errors occurred when validating the input data: The passed object is not a string.</p>
"""
    assert res_empty_string.status_code == 400
    assert res_empty_string.data == b"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>400 Bad Request</title>
<h1>Bad Request</h1>
<p>Errors occurred when validating the input data: Passed an empty string.</p>
"""
    assert res_valid_string.status_code == 200
    valid_response = res_valid_string.get_json()
    api_version = valid_response.get("api_version", None)
    model_version = valid_response.get("model_version", None)
    predictions = valid_response.get("predictions", None)
    assert not api_version is None
    assert not model_version is None
    assert not predictions is None