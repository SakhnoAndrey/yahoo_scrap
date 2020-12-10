# yahoo_scrap

Scrapping Yahoo Project

# Describes dockerfile and docker-compose
https://github.com/dimmg/dockselpy

# Information

Recent struggle with finding a docker image for Selenium that supports headless versions for both Firefox and Chrome, led to the process of building my own version.

The image is build with the following dependencies:

    latest Chrome and chromedriver
    latest Firefox and geckodriver
    latest stable PhantomJS webkit (v2.1.1)
    Selenium
    Python 3
    Xvfb and the python wrapper - pyvirtualdisplay

# Running:

    docker

    docker build -t selenium_docker .
    docker run --privileged -p 4000:4000 -d -it selenium_docker 

    docker-compose

    docker-compose stop && docker-compose build && docker-compose up -d

# Stop docker compose

> Stop containers

docker-compose stop

> Remove volumes

docker-compose rm -v -f