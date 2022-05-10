FROM python:3.8
COPY ./src /
RUN apt-get update
RUN apt-get install nano
RUN apt-get install -y iproute2
RUN pip3 install evolved5g
EXPOSE 1191
ENTRYPOINT ["python3", "qos_awereness.py"]
