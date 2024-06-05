FROM django:latest

WORKDIR /work_dir

COPY ./containers/django/requirements.txt /work_dir/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /work_dir/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]