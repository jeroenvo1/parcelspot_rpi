# Delete all images + containers
# docker rm $(docker ps -a -q); docker rmi $(docker images -q)

# Build image
# docker image build -t parcelspot_rpi .

# Run
# docker run -p 5000:5000 --rm parcelspot_rpi

# Run in background
# docker run -d -p 5000:5000 --rm parcelspot_rpi
# docker build -t jeroenvo/parcelspot-rpi .
# docker run -d -p 5000:5000 --name parcelspot-rpi --rm jeroenvo/parcelspot-rpi
# docker run -d -p 5000:5000 --name parcelspot-rpi --rm jeroenvo/parcelspot-rpi --device=/dev/video0:/dev/video0
# docker run --device=/dev/video0:/dev/video0 -d -p 5000:5000 --name parcelspot-rpi --rm jeroenvo/parcelspot-rpi:71400f4

# sudo modprobe bcm2835-v4l2


# Docker hub
# docker push jeroenvo/parcelspot-rpi:test1
# docker pull jeroenvo/parcelspot-rpi:test1
# docker run -d -p 5000:5000 --name parcelspot-rpi --rm jeroenvo/parcelspot-rpi:71400f4

# Commands in container
# docker exec -it CONTAINER_ID /bin/bash

FROM mohaseeb/raspberrypi3-python-opencv:latest

# Create app directory
WORKDIR /app

# Update ubuntu
# RUN apt-get update
# RUN apt-get upgrade -y

# Install ZBar
RUN apt-get install zbar-tools -y
RUN apt-get install libzbar-dev -y

# Copy project in container
COPY . /app

# Update pip
RUN pip install --upgrade pip

# Install libs
RUN pip install --no-cache-dir -r requirements.txt

# Run application
CMD export FLASK_APP=__init__.py; flask run --host=0.0.0.0 --port=5000

# Expose port
EXPOSE 5000