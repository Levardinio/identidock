FROM python:3.13

RUN pip install Flask==3.1.1
WORKDIR /app
COPY app /app/
CMD [ "python", "identidock.py" ]