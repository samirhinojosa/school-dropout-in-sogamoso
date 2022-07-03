FROM python:3.10-slim

RUN mkdir /backend

RUN pip install --upgrade pip==22.1.2

COPY requirements.txt /backend

WORKDIR /backend

RUN pip install -r requirements.txt

COPY ./app /backend/app

EXPOSE 8008

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8008"]

# RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
# RUN apt-get -y install curl
# RUN apt-get install libgomp1