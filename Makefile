clean_image:
	@find app/static/app/img/user/ -type f -not -name "default" -print0 | xargs -0 rm --

clean: clean_image
	@find . -name "*.pyc" -delete

deps:
	@pip install -r requirements.txt

task:
	@DEBUG=true ./manage.py process_tasks &
run: clean deps task
	@DEBUG=true ./manage.py runserver 
