FROM tiangolo/uvicorn-gunicorn-fastapi

WORKDIR /

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt \
    && rm -rf /root/.cache/pip

COPY . /chat_app/

CMD uvicorn chat_app.server:app --host 0.0.0.0 --port 5000