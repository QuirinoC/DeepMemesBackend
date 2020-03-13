FROM python

WORKDIR  /usr/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN chmod +x hooks/deploy.sh

CMD python3 app.py