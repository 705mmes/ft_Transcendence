FROM python:latest
WORKDIR /work_dir
ENV PYTHONUNBUFFERED=1

COPY ./containers/django/requirements.txt /work_dir/
RUN apt-get update && apt-get upgrade -y && \
    pip install -r requirements.txt
COPY ./containers/django/tr_test/ /work_dir
CMD ["python3", "./work_dir/manage.py", "runserver"]