# Geo-Advertising

## Steps to Run
* [Clone repo](#clone-repo)
* [Install current packages](#install-current-packages)
* [Set up database](#set-up-database)
* [Run Server](#run-server)

### Clone Repo
run `git clone https://github.com/mlafaive/GeoAdvertising.git`

### Install Current Packages
if necessary, install lastest [python3 release](https://www.python.org/downloads/)
	(on mac: `brew install python3`)

run `pip3 install -r requirements.txt`

### Set up Database
[install PostgreSQL](https://www.postgresql.org/download/)
	(on mac: `brew install postgresql`)

run `postgres -D /usr/local/var/postgres &`

seed database with `python3 seeds.py` (example data)

### Run Server
run `python3 app.py` and go to http://localhost:3000/


