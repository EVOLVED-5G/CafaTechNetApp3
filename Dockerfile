FROM python:3.8
COPY ./src /netapp/
COPY entrypoint.sh /
RUN apt-get update
RUN apt-get install nano
RUN apt-get install -y iproute2
RUN apt-get install iputils-ping
RUN pip3 install evolved5g==0.8.5
RUN pip3 install requests --upgrade
RUN pip3 install flask
RUN pip3 install -U flask-cors
EXPOSE 1191
EXPOSE 5555
ENTRYPOINT ["./entrypoint.sh"]
