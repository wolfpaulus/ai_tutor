# Dokerfile to create the container for the ERAU CS 399 Server
FROM python:3.11
MAINTAINER Wolf Paulus <wolf@paulus.com>

COPY ./requirements.txt .
COPY ./ws.py .
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

#  prevents Python from writing .pyc files to disk
#  ensures that the python output is sent straight to terminal (e.g. your container log) without being first buffered
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
CMD ["python3.11", "ws.py"]