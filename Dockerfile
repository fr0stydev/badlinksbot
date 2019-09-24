FROM python:3.6

WORKDIR /app

COPY . .

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install -r ./requirement.txt

CMD [ "python", "maliciouslinkBOT.py" ]