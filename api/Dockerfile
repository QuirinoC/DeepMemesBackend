FROM python

WORKDIR  /usr/app

COPY ./python_modules/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
RUN rm requirements.txt

COPY ./api/ .


CMD python3 app.py