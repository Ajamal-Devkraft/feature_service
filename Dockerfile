FROM python:3.5
ENV PYTHONUNBUFFERED=1
ENV REDIS_HOST "redis"
RUN mkdir /hdfclife_backend_code
WORKDIR /hdfclife_backend_code
ADD . /hdfclife_backend_code/
RUN python3 -m pip install --upgrade pip
EXPOSE 8000
RUN pip install -r new_requirements.txt
RUN mkdir -p /hdfclife_backend_code/logs
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8001"]