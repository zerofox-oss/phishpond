FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

WORKDIR /backend
COPY ./ /backend
EXPOSE 5000
RUN pip3 install -r /backend/requirements.txt
