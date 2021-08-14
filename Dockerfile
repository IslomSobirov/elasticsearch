FROM python:3.6

ENV PYTHONUNBUFFERED 1

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /var/www/aiohttp
WORKDIR /var/www/aiohttp

EXPOSE 8000

CMD ["python", "/var/www/aiohttp/app.py"]