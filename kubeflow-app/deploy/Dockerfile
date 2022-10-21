From python:3.9-slim-buster
WORKDIR /opt/app
COPY  ./dist/ ./
RUN pip install -r requirements.txt

RUN apt-get update \
    && apt-get install -y --no-install-recommends libgomp1 unzip \
    && apt-get clean

ENV PYTHONPATH="/opt/app"
COPY ./src/ .

CMD ["python" , "kubeflow/train.py"]