FROM python:3.8-slim-buster as base

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.0.1 \
  TRELLO_BOARD=$TRELLO_BOARD \
  TRELLO_KEY=$TRELLO_KEY \
  TRELLO_TOKEN=$TRELLO_TOKEN

# System deps:
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY poetry.lock pyproject.toml /code/

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

#------------#
# PRODUCTION #
#------------#

# Setting up the production image
FROM base as production

# Creating folders, and files:
COPY . /code

# Kick off the production app using gunicorn
ENTRYPOINT poetry run gunicorn -e TRELLO_BOARD=$TRELLO_BOARD -e TRELLO_KEY=$TRELLO_KEY -e TRELLO_TOKEN=$TRELLO_TOKEN --bind 0.0.0.0:8000 'todo_app:create_app()'

# Export the port
EXPOSE 8000

#-------------#
# DEVELOPMENT #
#-------------#

FROM base as development

# Kick off the development app using Flask dev server
ENTRYPOINT poetry run flask run --host=0.0.0.0 --port=5000

# Export the port
EXPOSE 5000

#---------#
# TESTING #
#---------#

FROM base as test

RUN  apt-get update \
  && apt-get install -y \
  fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 \
  libnspr4 libnss3 lsb-release xdg-utils libxss1 libdbus-glib-1-2 \
  curl unzip wget \
  xvfb

# install geckodriver and firefox

RUN GECKODRIVER_VERSION=`curl https://github.com/mozilla/geckodriver/releases/latest | grep -Po 'v[0-9]+.[0-9]+.[0-9]+'` && \
    wget https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz && \
    tar -zxf geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz -C /usr/local/bin && \
    chmod 777 /usr/local/bin/geckodriver && \
    rm geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz

RUN FIREFOX_SETUP=firefox-setup.tar.bz2 && \
    apt-get purge firefox && \
    wget -O $FIREFOX_SETUP "https://download.mozilla.org/?product=firefox-latest&os=linux64" && \
    tar xjf $FIREFOX_SETUP -C /opt/ && \
    ln -s /opt/firefox/firefox /usr/bin/firefox && \
    rm $FIREFOX_SETUP
    
# Creating folders, and files:
COPY . /code

# Kick off the tests
ENTRYPOINT poetry run pytest tests/unit && poetry run pytest tests/integration && poetry run pytest tests_e2e