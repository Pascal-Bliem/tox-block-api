# ToxBlock API

This is a Flask-based REST API serving the [ToxBlock](https://github.com/Pascal-Bliem/tox-block) Python package (available on [PyPI](https://pypi.org/project/tox-block/)), a machine learning application for recognizing toxic language in text.

The API can be used to get predicted probabilities for classifying English text into six categories of verbal toxicity: toxic, severe toxic, obscene, threat, insult, and identity hate.

For more information on the underlying Python package, `tox-block`, check out its [repository](https://github.com/Pascal-Bliem/tox-block).

*Disclaimer: the usage examples presented here contain toxic language that may be considered profane, vulgar, or offensive. If you do not wish to be exposed to toxic language, DO NOT proceed to read any further.*

## Usage

The API currently (`version 0.1.0`) provides two endpoints to which HTTP POST requests can be send.

Predictions for single strings of text can me made via sending a POST request to the endpoint `/v1/make_single_prediction`. The request's body should contain JSON data with the key `input_data` and string as value:

```python
{
    "input_data": "I will kill you, you fucking idiot!"
}
```
The response will contain a JSON with the machine learning model and API version, the original text, and the predicted probabilities for each category of toxicity:

```python
{
    "api_version": "0.1.0",
    "model_version": "0.1.2",
    "predictions": {
        "identity_hate": 0.1710592806339264,
        "insult": 0.9883397221565247,
        "obscene": 0.9885633587837219,
        "severe_toxic": 0.7870364189147949,
        "text": "I will kill you, you fucking idiot!",
        "threat": 0.8483908176422119,
        "toxic": 0.9998680353164673  
    }
}
```

Predictions for multiple strings of text can me made via sending a POST request to the endpoint `/v1/make_predictions`. The request's body should contain JSON data with the key `input_data` and a list of strings as value:

```python
{
    "input_data": ["Good morning my friend, I hope you're having a fantastic day!",
                  "I will kill you, you fucking idiot!",
                  "I do strongly disagree with the fascist views of this joke that calls itself a political party."]
}
```

The response will contain a JSON with the machine learning model and API version, and for each input element, the original text, and the predicted probabilities for each category of toxicity:

```python
{
    "api_version": "0.1.0",
    "model_version": "0.1.2",
    "predictions": {
        "0": {
            "identity_hate": 0.0021067343186587095,
            "insult": 0.00757843442261219,
            "obscene": 0.004466842859983444,
            "severe_toxic": 0.0006274481420405209,
            "text": "Good morning my friend, I hope you're having a fantastic day!",
            "threat": 0.009578478522598743,
            "toxic": 0.05347811430692673
        },
        "1": {
            "identity_hate": 0.17105941474437714,
            "insult": 0.9883397221565247,
            "obscene": 0.9885633587837219,
            "severe_toxic": 0.7870364785194397,
            "text": "I will kill you, you fucking idiot!",
            "threat": 0.8483907580375671,
            "toxic": 0.9998679757118225
        },
        "2": {
            "identity_hate": 0.0022098885383456945,
            "insult": 0.0029190650675445795,
            "obscene": 0.0009493007673881948,
            "severe_toxic": 7.187385926954448e-05,
            "text": "I do strongly disagree with the fascist views of this joke that calls itself a political party.",
            "threat": 0.0001232452632393688,
            "toxic": 0.02619001641869545
        }
    }
}
```

## Run the ToxBlock API yourself

The API is build with Flask, a Python micro web framework. There are several ways to deploy this application.

First of all, clone this repo to wherever you want to run the app. The entry point for the app is `run.py`. Flask itself has a build-in webserver which can be used for development purposes. Just set the environment variable
```bash
export FLASK_APP=run.py
```
and then you can (given that you have Flask installed) run
```bash
flask run
```
Flask's build-in server is very simple and shouldn't be used in production. You can instead run the Flask app on [`gunicorn`](https://gunicorn.org/), which is a Python WSGI HTTP Server for UNIX. You can find an example in the shell script `run.sh`:
```bash
#!/usr/bin/env bash
export IS_DEBUG=${DEBUG:-false}
exec gunicorn --bind 0.0.0.0:5000 --access-logfile - --error-logfile - run:application
```
Another great option is to run the app as a [Docker](https://www.docker.com/) container. The build commands for the Docker image are specified in the [`Dockerfile`](./Dockerfile).

Whatever way you chose, you will have to specify a [secret key](https://flask.palletsprojects.com/en/1.1.x/config/) for the Flask app (stored in `tox_block_api.config.Config.SECRET_KEY`) as an environment variable `FLASK_CONFIG_SECRET_KEY="<your secret random string>"`. You can store it in a `.env` file from where it will be loaded by `python-dotenv` or, if you're using Docker, specify it in your `Dockerfile` by adding the line
```docker
ENV FLASK_CONFIG_SECRET_KEY <your secret random string>
```