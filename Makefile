clean:
	@find . -name "*.pyc" -delete

deps:
	@pip install -r requirements.txt

run: clean deps 
	@DEBUG=true ./manage.py runserver
