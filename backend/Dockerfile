FROM python:3.10-slim

RUN mkdir /usr/src/app

RUN pip install --upgrade pip==22.2

COPY requirements.txt /usr/src/app

WORKDIR /usr/src/app

RUN pip install -r requirements.txt

#COPY . /usr/src/app

EXPOSE 8008

# option: --reload only in development or local
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8008", "--reload"]


RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get -y install curl
RUN apt-get install libgomp1