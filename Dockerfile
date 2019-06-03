FROM python:3.7.3-alpine

RUN mkdir /app

COPY github_gists.py /app/

COPY requirements.txt /app

RUN pip install -r /app/requirements.txt

ENTRYPOINT ["/app/github_gists.py"]
