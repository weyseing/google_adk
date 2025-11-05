FROM python:3.11-slim

# worker dir
WORKDIR /app

# install python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy app code
COPY . /app

# entrypoint
CMD ["tail", "-f", "/dev/null"]