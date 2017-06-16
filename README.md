StuyBulletin
============
William Xiang, Rodda John, Nancy Cao, Jiaqi Gao pd 8
SoftDev Final Project

>  A continuous source of opportunities compiled for Stuyvesant High School students

[![Build Status](https://travis-ci.org/wxiang54/3XTheCharm.svg?branch=master)](https://travis-ci.org/wxiang54/3XTheCharm.svg)
[![Coverage Status](https://coveralls.io/repos/github/wxiang54/3XTheCharm/badge.svg?branch=master)](https://coveralls.io/github/wxiang54/3XTheCharm?branch=master)

[logo]:docs/stuybulletin.png

StuyBulletin is platform built for Stuyvesant High School students to effectively find opportunities that best suit their interests. With a collection of programs and events curated by Stuyvesant's own Internship Coordinator, students can select filters such as age requirement and approaching deadlines, as well as star opportunities that they would like to apply for.

## How to run the project
1. Install all dependencies:  `$make setup`

  * If you get an `mysql_config` error, that means you need to install the appropriate mysql package for your OS
    * OSX: `$brew install mysql`
    * Linux: `$apt-get install libmysqlclient-dev`
    * Windows: `xd`
  * If you get more errors, especially involving `egg_info`, it just might be over for you.

2. Create the database:  `$./manage.py createdb`

3. Migrate the database:  `$./manage.py migratedb`

4. Run the server:  `$make run`
