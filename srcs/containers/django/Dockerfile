FROM python:latest
WORKDIR /work_dir
ENV PYTHONUNBUFFERED=1

COPY ./containers/django/requirements.txt /work_dir/
RUN pip install Django==5.0.6 -r requirements.txt

COPY ./containers/django/tr_test/ /work_dir
CMD ["python3", "./work_dir/manage.py", "runserver"]