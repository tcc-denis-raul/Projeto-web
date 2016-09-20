clean_image:
	@find app/static/app/img/user/ -type f -not -name "default" -print0 | xargs -0 rm --

clean: clean_image
	@find . -name "*.pyc" -delete

deps:
	@pip install -r requirements.txt

run: clean deps 
	@DEBUG=true ./manage.py runserver
