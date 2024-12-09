FROM python:3.11

WORKDIR /app

RUN pip install pipenv
RUN pip install numpy
RUN pip install pillow
RUN pip install flask
RUN pip install tensorflow
RUN pip install google-cloud-firestore


COPY . /app/
COPY model_fruit.h5 /app/

EXPOSE 8080
CMD ["python", "app.py"]
