FROM python:3.5
ENV PYTHONUNBUFFERED=1
RUN mkdir /hdfclife_feature_service
WORKDIR /hdfclife_feature_service/
ADD . /hdfclife_feature_service/
RUN python3 -m pip install --upgrade pip
RUN pip install -r requirement.txt
RUN mkdir -p /hdfclife_feature_service/logs
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8002"]