ARG python_version=3.10
FROM python:${python_version}-slim


RUN apt-get update \
    && apt-get install -y git zsh curl\
    && apt-get install -y vim build-essential cmake\
    && pip install -U pip \
    && pip install poetry \
    && apt-get autoremove \
    && apt-get clean
RUN apt-get install -y rsyslog
RUN echo "cron.*      /var/log/cron.log" >> /etc/syslog.conf



RUN mkdir -p /usr/src/app
COPY ./rddl_info /usr/src/app/rddl_info
COPY poetry.lock /usr/src/app
COPY pyproject.toml /usr/src/app
COPY README.md /usr/src/app
COPY rddl-info.crontab /etc/cron.d/rddl-info
RUN chown 600 /etc/cron.d/rddl-info

RUN /etc/init.d/rsyslog start
RUN /etc/init.d/cron start

WORKDIR /usr/src/app
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction
RUN poetry install --no-dev


