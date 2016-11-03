# Set the base image to use to Ubuntu
FROM amazon/aws-eb-python:3.4.2-onbuild-3.5.1

MAINTAINER Prasanna Rishiraj

RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["~/Containerized-Virtualized-Sensor-Management/entrypoint.sh"]
