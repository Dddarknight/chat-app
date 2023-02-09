FROM tiangolo/uvicorn-gunicorn-fastapi

WORKDIR /

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt \
    && rm -rf /root/.cache/pip

COPY . /replicator/
