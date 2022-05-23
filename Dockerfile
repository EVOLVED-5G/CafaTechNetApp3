FROM python:3.8
COPY ./src /
RUN apt-get update
RUN apt-get install nano
RUN apt-get install -y iproute2
RUN pip3 install evolved5g
RUN pip3 install flask
EXPOSE 1191
EXPOSE 5555
ENTRYPOINT ["./entrypoint.sh"]
