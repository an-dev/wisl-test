FROM python:3.9

WORKDIR /wisl

COPY ./requirements.txt /wisl/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /wisl/requirements.txt

COPY ./docker-entrypoint.sh /wisl/docker-entrypoint.sh

USER root
RUN chmod +x /wisl/docker-entrypoint.sh

COPY ./alembic.ini /wisl/alembic.ini
COPY ./alembic /wisl/alembic
COPY ./app /wisl/app

EXPOSE 8001

CMD ["bash", "-c", "/wisl/docker-entrypoint.sh"]
