# api_yamdb

![Logo](https://cdn-irec.r-99.com/sites/default/files/product-images/399872/EOXOqQkXnjTMTRnIpMUSvQ.jpg)


Проект Yamdb собирает отзывы (Review) пользователей на произведения (Titles).\
Работы разделены на категории: «Книги», «Фильмы», «Музыка».\
Сами произведения в Yamdb не хранятся; здесь нельзя смотреть кино или слушать музыку.\
В каждой категории есть работы: книги, фильмы или музыка.\
Произведению может быть присвоен жанр (Жанр) из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).\
Новые жанры может создавать только администратор.\
Благодарные или возмущенные пользователи оставляют текстовые отзывы (Review) на работы и оценивают в диапазоне от одного до десяти; рейтинг формируется из оценок пользователей.

### Настройка и запуск сервера:
**Клонировать репозиторий**
```bash
git clone https://github.com/p1rt-py/api_yamdb
```
**Создать и активировать виртуальную среду:**
```bash
python -m venv venv
```
``` bash
source venv/Scripts/activate
```

**Установить зависимости из файла requirements.txt:**
```bash
python -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

**Перейдите в основную папку:**
```bash
cd api_yamdb
```

**Создайте базу данных из CSV файлов:**
```bash
python manage.py dbpop
```

**Выполните миграцию:**
```bash
python manage.py migrate
```

**Запустите проект:**
```bash
python manage.py runserver
```

### Зависимости
_Request==2.26.0
Django==2.2.16
Djangorestframework==3.12.4
PyJWT==2.1.0
Pytest==6.2.4\
Pytest-django==4.4.0
Pytest-pythonpath==0.7.3
Django-filter==2.2.0
Djangorestframework-simplejwt=5.2.0_

### Технологии:
_Python 3.8
Django 2.2.16
Djangorestframework 3.12.4
Redoc_

### Авторы  🔗

- [Yana Bubnova](https://github.com/Kasaress)
- [p1rt-py](https://github.com/p1rt-py)
- [am-practicum](https://github.com/am-practicum)
