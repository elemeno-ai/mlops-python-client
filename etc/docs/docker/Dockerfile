FROM python:3.8-alpine

ADD . /opt/app

WORKDIR /opt/app

RUN pip install -r requirements.txt && \
  pip install -e .

CMD pdoc mlops_client --logo https://storage.googleapis.com/elemeno-logo/elemeno_icon_1000.png \
  --logo-link https://mlops.elemeno.ai --favicon https://storage.googleapis.com/elemeno-logo/e-symbol-purple.png