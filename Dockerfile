# Dockerfile

FROM python:3.11-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app ./

# Add this line to copy the templates folder
COPY templates ./templates/

CMD ["python", "main.py"]