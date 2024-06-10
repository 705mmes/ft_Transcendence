FROM django:latest

WORKDIR /work_dir

#COPY ./containers/django/requirements.txt /work_dir/
#RUN python3 -m pip install django

COPY . /work_dir/

EXPOSE 8000

CMD ["python3", "./tr_test/manage.py", "runserver", "0.0.0.0:8000"]