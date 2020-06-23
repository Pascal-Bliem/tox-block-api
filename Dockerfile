FROM python:3.7.0

# Create the user that will run the app
RUN adduser --disabled-password --gecos '' tox-block-api-user

WORKDIR /opt/tox_block_api

ENV FLASK_APP run.py

# Install requirements, including from Gemfury
ADD ./ /opt/tox_block_api/
RUN pip install --upgrade pip
RUN pip install -r /opt/tox_block_api/requirements.txt

RUN chmod +x /opt/tox_block_api/run.sh
RUN chown -R tox-block-api-user:tox-block-api-user ./

USER tox-block-api-user

EXPOSE 5000

CMD ["bash", "./run.sh"]