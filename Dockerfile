FROM python:3.7-slim-buster
COPY . /app
EXPOSE 5000
WORKDIR /app
RUN pip3 install -r requirements.txt
CMD ["dvc", "repro", "-f"]