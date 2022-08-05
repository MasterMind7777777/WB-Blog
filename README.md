# WB-Blog
Задание для стажеров на Backend от WB—Tech

регистрация 
post
/api/users/
{
    "username": "",
    "password": ""
}

получение токена
post
/api/auth/token/login/
{
    "username": "",
    "password": ""
}

список постов
get
/api/posts/

список ползователей
get
/api/users/

создать пост
post
/api/posts/
{
    "name": "test post",
    "text": "test text"
}

посмотреть выбраный пост
get
/api/posts/<pk>/

отметить пост как прочитаный
post
/api/posts/<pk>/read/

посмотреть посты выбраного пользователя
post
/api/users/<pk>/posts/

подписатся на пользователя
post
/api/users/<pk>/subscribe/

посмотреть посты авторов на которых подписан
get
/api/users/subscriptions_posts/
