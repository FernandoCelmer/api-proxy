ARG APP_PATH=/usr/src

FROM python:3
ARG APP_PATH

RUN mkdir $APP_PATH/proxy/
COPY . $APP_PATH/proxy/

WORKDIR $APP_PATH
EXPOSE 8000

RUN pip install -r proxy/requirements.txt --no-cache-dir

CMD ["uvicorn", "proxy.main:app", "--host", "0.0.0.0", "--port", "8000"]