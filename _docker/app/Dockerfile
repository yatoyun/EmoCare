FROM unit:python3.12

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive
ENV APP_ROOT /usr/src/app

WORKDIR $APP_ROOT

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl nginx supervisor build-essential gcc \
    && rm -rf /var/lib/apt/lists/*

COPY ./backend/requirements.txt $APP_ROOT/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt \
    && rm -rf ~/.cache/pip

RUN mkdir -p $APP_ROOT && rm -f /etc/nginx/nginx.conf
COPY ./backend/nginx.conf /etc/nginx/nginx.conf
RUN useradd -r nginx

RUN mkdir -p /etc/supervisor
COPY ./backend/supervisord.conf /etc/supervisor/supervisord.conf

COPY --chown=nobody:nogroup ./backend $APP_ROOT

ENV PYTHONPATH $APP_ROOT

# [local, prod]
ARG STAGE
ARG AWS_REGION
ARG AWS_SECRET_NAME
ARG CLIENT_HOST
COPY ./backend/config.json /tmp/config.json
RUN set -x && unitd \
    && curl -X PUT -d @/tmp/config.json \
    --unix-socket /var/run/control.unit.sock \
    http://localhost/config

# EXPOSE 443
EXPOSE 8002

CMD ["supervisord", "--nodaemon", "-c", "/etc/supervisor/supervisord.conf"]
