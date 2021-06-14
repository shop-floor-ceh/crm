# CRM
## Пошаговая инструкция для запуска проекта
### 1
Скачиваете [postgres](https://www.postgresql.org/download/)
Устанавливаете и ставите галочку на PgAdmin4
### 2
Открываете PgAdmin4 и запускаете сервер (правой кнопкой мыши по servers)
host: localhost
port: 5432
### 3 
В файле shop_floor/shop_floor/settings.py
В блоке DATABASE пишите свой паароль от PgAdmin4
### 4 
Открываете проект в PyCharm 

В терминале прописываете команды
```pip install -r requirements.txt```

```cd shop_floor```

```python manage.py makemigrations```

```python manage.py migrare```

```python manage.py runserver```
