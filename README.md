# real_time_chat

Чат, работающий с обновлениями данных в режиме реального времени с помощью 
SSE (Server Sent Events)

В проекте реализованы пользователи без авторизации и один общий чат, 
отображающий сообщения.

# Установка (локально):
<ul>
 <li> Скопируйте репозиторий </li>
 <li>Установите зависимости</li>
</ul>

    pip install -r requirements.txt

<ul>
 <li> Не забудьте активировать виртуальное окружение! </li>
</ul>

    source venv/bin/activate

<ul>
 <li> Совершите миграции БД через flask shell</li>
</ul>

    export FLASK_APP=sse_app
    flask shell
    db.drop_all()
    db.create_all()

<ul>
 <li> Готово! Теперь можно запустить сервер</li>
</ul>

    gunicorn sse_app:app --worker-class gevent --bind 127.0.0.1:8000
    
Осталось только перейти во вкладку  http://127.0.0.1:8000 и начать пользоваться!

# Установка образа (docker):
Будет позднее...

# И немного скриншотиков

<img src="screens/два%20экрана.png">

<img src="screens/выбор%20пользователя.png">