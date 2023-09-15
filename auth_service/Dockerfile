FROM python:3.10 as base

WORKDIR /opt/src

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    GID=auth-service \
    UID=auth-service

COPY Pipfile Pipfile.lock ./

RUN pip install --upgrade pip \
    && pip install pipenv==2023.6.2 \
    && pipenv install --system --deploy

COPY src .
COPY migrations /opt/migrations/
COPY alembic.ini /opt/alembic.ini

EXPOSE 8080

RUN groupadd -r ${GID} \
    && useradd -d /home/${UID} -r -g ${GID} ${UID} \
    && chown ${UID}:${UID} -R /opt
USER ${UID}

ENTRYPOINT [ "bash", "entry.sh" ]
