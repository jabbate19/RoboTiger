FROM python:3.9.8-bullseye
LABEL maintainer="Joseph Abbate <josephabbateny@gmail.com>"

WORKDIR /app/
COPY ./ /app/
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt

CMD [ "python3", "main.py" ]

