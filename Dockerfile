FROM python:3.7.4-alpine
WORKDIR /usr/src/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk add jpeg-dev zlib-dev libjpeg \
    && pip install Pillow \
    && pip install cryptography \
    && apk del build-deps
RUN pip install --upgrade pip
COPY requirements.txt /usr/src/app/
RUN pip install -r requirements.txt
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
ADD . /usr/src/app/
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]