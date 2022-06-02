start:
	docker start 0f3f341bfa3b && python manage.py runserver

run:
	python manage.py runserver

#no funciona esta regla
activate-ev:
	source ../eb-virt/bin/activate	

deploy:
	eb deploy

make_migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

docker_status:
	docker ps -f name=django-bbdd

database:
	docker start 0f3f341bfa3b