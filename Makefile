install:
	pip install -r requirements.txt

server:
	FLASK_APP=p2.py FLASK_ENV=${VIRTUAL_ENV} flask run