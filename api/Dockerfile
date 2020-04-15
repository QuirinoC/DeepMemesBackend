FROM python

WORKDIR  /usr/app

COPY ./python_modules/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY ./api/ .

RUN ls -la

CMD python3 app.py