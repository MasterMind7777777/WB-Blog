# WB-Blog
Задание для стажеров на Backend от WB—Tech

## Технологии
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)

## Описание
API для создания блога c функионалом:
1. Регистрироваться новым пользователям и выполнять вход существующих.
2. Авторизованным пользователям создавать посты. Пост имеет заголовок и текст
поста.
3. Просматривать список пользователей с возможностью сортировки по количеству
постов.
4. Просматривать список постов других пользователей, отсортированный по дате
создания, сначала свежие.
5. Авторизованным пользователям подписываться и отписываться на посты других
пользователей.
6. Авторизованным пользователям формировать ленту из постов пользователей, на
которые была осуществлена подписка. В ленту попадают новые посты
пользователей после выполнения подписки. Сортировка по дате создания поста,
сначала свежие. Список постов отдается страницами по 10шт.
7. Авторизованным пользователям помечать посты в ленте как прочитанные.
8. Администратору управлять пользователями и контентом средствами Django admin.

## Установка
склонируйте проект с реппозитория GitHub
> **https://github.com/MasterMind7777777/WB-Blog.git**

перейдите в директорию WB-Blog/
> **cd WB-Blog/infra/**

запустите docker-compose

> **docker-compose up -d**

проведите миграции

> **docker-compose exec backend python manage.py makemigrations**
> **docker-compose exec backend python manage.py migrate**


##### Автор
*Нестерёнок Георгий Дмитриевич*
