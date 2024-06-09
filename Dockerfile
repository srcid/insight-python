FROM python:3.12.2

COPY . /app
WORKDIR /app
RUN pip install -r ./requirements.txt

CMD [ "python", "main.py" ]


EXPOSE 80