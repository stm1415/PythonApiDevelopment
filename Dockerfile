# specify our base image
FROM python:3.12

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# copy the content of the local directory to the working directory
COPY . .

# command to run on container start
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]