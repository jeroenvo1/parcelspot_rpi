#!/bin/bash
modprobe bcm2835-v4l2
docker run --device=/dev/video0:/dev/video0 -d -p 5000:5000 --name parcelspot-rpi --rm jeroenvo/parcelspot-rpi:71400f4


# application.service
[Unit]
Description=Flask_application
After=network.target

[Service]
ExecStart=/opt/application/run.sh
ExecReload=/bin/kill -HUP $MAINPID
KillMode=process
Restart=on-failure
Type=simple

[Install]
WantedBy=multi-user.target