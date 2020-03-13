FROM python

WORKDIR  /usr/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD python3 app.py