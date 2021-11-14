FROM python:3.9-slim
RUN useradd -ms /bin/bash uvicorn
USER uvicorn
COPY / /home/uvicorn
RUN pip install -r /home/uvicorn/requirements.txt
WORKDIR /home/uvicorn
ENTRYPOINT /home/uvicorn/.local/bin/uvicorn main:app --host 0.0.0.0 --port $PORT