FROM python:3.5
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

ENTRYPOINT ["python"]
CMD ["app.py"]
EXPOSE 8089