# Get Brain (CRM-system)

Проект размещен по адресу http://20.42.101.164/

Примеры аккаунтов:

```
login: cafe
password: cafe

login: cafe_subordinate
password: cafe
```

## Ручной запуск

Установить необходимые библиотеки из requirements.txt

БД:
```
sudo -u postgres psql
ALTER USER postgres PASSWORD 'postgres';
create database crm;
```
Запуск:
```
python3 manage.py makemigrations crm
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:80
```


