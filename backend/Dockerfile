# Use the official Python slim image as a base
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the CSV data files from the data directory into the container
COPY data/*.csv /app/data/

# Install dependencies required for psycopg2 binary
RUN apt-get update && apt-get install -y libpq-dev gcc wget curl

# Install dockerize
ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

# Install Python dependencies, including pandas
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Verify installation by listing installed packages
RUN pip list

# Copy the rest of the application
COPY . /app

# Run migrations and start the application
CMD dockerize -wait tcp://db:5432 -timeout 60s && \
    flask db upgrade && \
    flask populate_db && \
    flask load-industry-types && \
    flask run --host=0.0.0.0 --port=5002
