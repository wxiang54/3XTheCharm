<p align="center"><img src="docs/stuybulletin.png" alt="stuybulletin" width="450" height="auto"></p>

StuyBulletin
============
William Xiang, Rodda John, Nancy Cao, Jiaqi Gao pd 8
SoftDev Final Project

>  A continuous source of opportunities compiled for Stuyvesant High School students

[![Build Status](https://travis-ci.org/wxiang54/3XTheCharm.svg?branch=master)](https://travis-ci.org/wxiang54/3XTheCharm.svg)
[![Coverage Status](https://coveralls.io/repos/github/wxiang54/3XTheCharm/badge.svg?branch=master)](https://coveralls.io/github/wxiang54/3XTheCharm?branch=master)

[logo]:docs/stuybulletin.png

StuyBulletin is platform built for Stuyvesant High School students to effectively find opportunities that best suit their interests. With a collection of programs and events curated by Stuyvesant's own Internship Coordinator, students can select filters such as age requirement and approaching deadlines, as well as star opportunities that they would like to apply for.

## Setup
1. Install dependencies and perform preliminary DB setup
* __Deploying locally: run `make setup`__
  * If you get an `mysql_config` error, that means you need to install the appropriate mysql package for your OS
    * OSX: `$brew install mysql`
    * Linux: `$apt-get install libmysqlclient-dev`
    * Windows: `xd`
  * If you get more errors, especially involving `egg_info`, it just might be over for you
* __Deploying live: `$sudo make setup-prod`__
  * Sudo privileges are required to change group and ownership of the DB as well as its directory
    * By default, they should be __$REPO_ROOT/app/testing_data__ and  __$REPO_ROOT/app/testing_data/app.db__, respectively

2. Create the __client_secrets.json__ file in __$REPO_ROOT/app/oauth/client_secrets.json__
  * The file should follow this format:
```javascript
{"web":
	{"client_id":"<YOUR CLIENT ID HERE>",
   	 "project_id":"<YOUR PROJECT ID HERE>",
     	 "auth_uri":"https://accounts.google.com/o/oauth2/auth",
       	 "token_uri":"https://accounts.google.com/o/oauth2/token",
         "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
	 "client_secret":"<YOUR CLIENT SECRET HERE>",
	 "redirect_uris":["http://127.0.0.1/oauth2callback"],
	 "javascript_origins":["http://127.0.0.1"]
	}
}
```
  * You can obtain your PROJECT_ID, CLIENT_ID and CLIENT_SECRET credentials by creating a project in [Google's API Console](https://console.developers.google.com).


## Running
* If deploying locally, run the local server: `$make run`
* If deploying live (assuming via Apache), copy the __stuybulletin.conf__ file from the repo's root directory to where it's supposed to go, supposedly __/etc/apache2/sites-enabled/__.
  * If your domain happens to not exactly be "stuybulletin.stuycs.org", be sure to modify the "ServerName" line in __stuybulletin.conf__ to reflect your different domain.

## Known Bugs
* Opportunities don't actually hold as much info as they should (e.g. most don't have links or organizations or etc.)
  * This is partly because some of the data wasn't present in the original PDF files, and partly because I didn't do the best job at parsing
* When listing opportunities, the tags on the left hand side (under Catagory, Grade level, Type) currently do not work
  * Their intended function was to filter results by what tags were checked