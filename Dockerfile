FROM python:3.8
COPY ./src /netapp/
COPY entrypoint.sh /
RUN apt-get update
RUN apt-get install -y jq
RUN apt-get install nano
RUN apt-get install -y iproute2
RUN apt-get install iputils-ping
RUN pip3 install -r /netapp/requirements.txt
EXPOSE 1191
EXPOSE 5555
ENTRYPOINT ["./entrypoint.sh"]
