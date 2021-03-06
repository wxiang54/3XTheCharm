default:
	@echo "Examples:"
	@echo "    make run          # Starts a Flask development server locally"
	@echo "    make production   # Starts the production server, sets up logging to logs/"
	@echo "    make clean        # Cleans all directors"
	@echo "    make test         # Runs unit tests"

setup:
	pip install -r requirements.txt
	./manage.py createdb
	./manage.py migratedb
	./manage.py parseopps

setup-prod:
	pip install -r requirements.txt
	./manage.py createdb
	./manage.py migratedb
	./manage.py parseopps
	chgrp www-data stuybulletin/testing_data
	chgrp www-data stuybulletin/testing_data/stuybulletin.db
	chmod g+w stuybulletin/testing_data
	chmod g+w stuybulletin/testing_data/stuybulletin.db

run:
	./manage.py devserver -p 5000

production:
	./manage.py --config_prod -p 5000 -l logs devserver

clean:
	rm -rf *~
	rm -rf *\#
	rm -rf .\#*
	rm *.log

test:	
	py.test --cov-report html --cov app tests
