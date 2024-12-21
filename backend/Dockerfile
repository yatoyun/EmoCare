FROM unit:python3.12-slim

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive
ENV APP_ROOT /usr/src/app

WORKDIR $APP_ROOT

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl nginx supervisor build-essential gcc \
    && rm -rf /var/lib/apt/lists/*d

COPY requirements.txt $APP_ROOT/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt \
    && rm -rf ~/.cache/pip

RUN mkdir -p $APP_ROOT && rm -f /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/nginx.conf
RUN useradd -r nginx

RUN mkdir -p /etc/supervisor
COPY supervisord.conf /etc/supervisor/supervisord.conf

COPY --chown=nobody:nogroup . $APP_ROOT

ENV PYTHONPATH $APP_ROOT

COPY config.json /tmp/config.json
RUN unitd \
    && curl -X PUT -d @/tmp/config.json \
    --unix-socket /var/run/control.unit.sock \
    http://localhost/config

EXPOSE 8002

CMD ["supervisord", "--nodaemon", "-c", "/etc/supervisor/supervisord.conf"]