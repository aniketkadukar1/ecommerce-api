django-admin startproject ecommerce


python manage.py runserver



from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())


pip freeze > requirements.txt

python manage.py spectacular --file schema.yml

pytest or pytest-coverage