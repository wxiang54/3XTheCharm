# 3XTheCharm
[![Build Status](https://travis-ci.org/wxiang54/3XTheCharm.svg?branch=master)](https://travis-ci.org/wxiang54/3XTheCharm.svg)
[![Coverage Status](https://coveralls.io/repos/github/wxiang54/3XTheCharm/badge.svg?branch=master)](https://coveralls.io/github/wxiang54/3XTheCharm?branch=master)

PR #04: Viz Due ? 2017-06-?, 8:00am, EST.

* William Xiang
* Rodda John
* Nancy Cao
* Jiaqi Gao


## How to run the project (in its current state)
1. Install all dependencies:  `$make setup`

  * If you get an `mysql_config` error, that means you need to install the appropriate mysql package for your OS
    * OSX: `$brew install mysql`
    * Linux: `$apt-get install libmysqlclient-dev`
    * Windows: `xd`
  * If you get more errors, especially involving `egg_info`, it just might be over for you.
  
2. Create the database:  `$./manage.py createdb`

3. Migrate the database:  `$./manage.py migratedb`
  
4. (Optional) Generate filler data:  `$./manage.py gen_opportunities`

  >  This generates four entries only. Therefore, given n is the number of times the command is run, your entries in the database will total to the partial sum of the arithmetic sequence a_n = a_1 + 4n 
  
  >  --Stern

5. Run the server:  `$make run`
