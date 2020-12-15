# yahoo_scrap

Scrapping Yahoo Project

# Requirements
- Docker
- Docker-compose

# Run on localhost
1. Create virtual environments:
> mkvirtualenv yahoo_scrap_envs
   
2. Enter the virtual environment
> workon yahoo_scrap_envs   

3. Install requirements with file requirements.txt
> pip install -r requirements.txt
   
4. Set up environment variables in files .env

DOWNLOAD_DIR:
- view when using docker (path localhost:path in docker):
DOWNLOAD_DIR=/dev/shm:/dev/shm
- view when using just a browser
DOWNLOAD_DIR=/files

SCRAPPER_TYPE_NAME:
docker vs browser

BROWSER_NAME:
firefox vs chrome

The real path to geckodriver of firefox EXECUTABLE_PATH (if you needed):
/home/lw/bin/geckodriver

Url of start page for scraper BASE_URL:
https://finance.yahoo.com/

5. Running docker-compose
> docker-compose up --build -d

6. Stop docker-compose

# Stop docker compose

Stop containers

> docker-compose stop

Remove volumes

> docker-compose rm -v -f

7. Scraping the data of the enterprises specified in ConfigBase.COMPANY_NAMES (settings.py)
> python scrapping.py
   
8. Launching the REST service for obtaining information saved by the scrapper in the database
> python manage.py 
Running on http://127.0.0.1:5000/company/<name>
where <name> - the name of enterprise
 

Information
-----------

# Describes Splinter
https://splinter.readthedocs.io/
