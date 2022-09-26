FROM nginxinc/nginx-unprivileged:1-alpine
LABEL maintainer="sloniupck"

COPY ./nginx/* /etc/nginx/
COPY ./run.sh /run.sh

ENV LISTEN_PORT=8000
ENV APP_HOST=app
ENV APP_PORT=9000

USER root

USER root

RUN apk add --no-cache openssl bash
RUN chmod +x /run.sh

VOLUME /vol/static
VOLUME /vol/www

CMD ["/run.sh"]