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
Install dependencies and perform preliminary DB setup:  `$make setup`

  * If you get an `mysql_config` error, that means you need to install the appropriate mysql package for your OS
    * OSX: `$brew install mysql`
    * Linux: `$apt-get install libmysqlclient-dev`
    * Windows: `xd`
  * If you get more errors, especially involving `egg_info`, it just might be over for you

## Running
* If deploying locally, run the local server: `$make run`
* If deploying live (assuming via Apache), copy the __stuybulletin.conf__ file from the repo's root directory to where it's supposed to go, supposedly __/etc/apache2/sites-enabled/__.
  * If your domain happens to not exactly be "stuybulletin.stuycs.org", be sure to modify the "ServerName" line in __stuybulletin.conf__ to reflect your different domain.