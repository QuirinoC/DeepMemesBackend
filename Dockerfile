FROM python

WORKDIR  /usr/app

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD python3