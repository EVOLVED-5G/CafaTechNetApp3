FROM python
COPY ./src /
RUN pip3 install evolved5g
EXPOSE 1191
ENTRYPOINT ["python3", "qos_awereness.py"]
