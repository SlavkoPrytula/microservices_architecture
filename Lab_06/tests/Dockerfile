#docker run -d --net=host -e 'CONSUL_LOCAL_CONFIG={"leave_on_terminate": true, "enable_script_checks": true}' consul_common

#FROM python:3.8-alpine
#
#EXPOSE 8080
#
#WORKDIR /app
#RUN mkdir -p /app
#COPY requirements.txt /app
#
#RUN pip install --upgrade pip && \
#	pip install -U -r requirements.txt
#
#COPY consul_common/consul_service.py /app
#
#ENTRYPOINT ["python"]
#CMD ["app.py", "--log-file", "-"]