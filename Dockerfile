# Python Runtime
FROM ubuntu:18.04
FROM python:3.7.3-stretch
# Mosquitto. MQTT Broker
FROM eclipse-mosquitto:1.5.8

# Set the working dir
WORKDIR /device

# Copy the directory into the container
COPY . /device


# Install pip for python3

# Install needed packages
RUN python -m pip --version
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make ports available to the world outside this container

EXPOSE 7000 # Discovery service

# Run command
CMD ["python3", "device.py"]

