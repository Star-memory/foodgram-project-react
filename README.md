# Foodgram

- Foodgram — «Продуктовый помощник». В этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Проект реализован на `Django` и `DjangoRestFramework`. Доступ к данным реализован через API-интерфейс. Документация к API написана с использованием `Redoc`. Помимо этого, проект 
работает в 3 контейнирах `Docker`: foodgram_frontend, foodgram_backend и foodgram_gatewey(
в свою очередь, в этом контейнере раюотает nginx. Его настроки лежат в папке /infra)

Для развертывания проекта нужно сделать:
  
  1. Установите на сервер `docker`.
     - `sudo apt install docker.io`
  2. Создайте файл `.env` на сервере.
     ```
     # database
     POSTGRES_USER=foodgram_user
     POSTGRES_PASSWORD=<Your_password>
     POSTGRES_DB=foodgram

     DB_NAME=foodgram
     DB_HOST=db
     DB_PORT=5432

     # settings.py
     SECRET_KEY=<Project_key>
     DEBUG=False_or_True
     ALLOWED_HOSTS=<Your_host>
     ```
  3. Скопируйте файл `docker-compose.yml`.
  4. Выполните команду `docker-compose up -d --buld` на сервере.
  5. Необходимые команды для работы проекта
     - `docker-compose exec backend python manage.py migrate`.
     - `docker-compose exec backend python manage.py createsuperuser`.
     - `docker-compose exec backend python manage.py collectstatic`.
     - Заполните базу ингредиентами `docker-compose exec backend python manage.py import_csv`.
     - Создайте пару тэгов, для правлильной фильтрации рецептов. В проекте подразумеваются: `завтрак`, `обед`, `ужин`, но это не обязательно.
     - Документация к API : http://<Your_host>/api/docs/redoc.html. Там есть примеры запросов, и ответы на эти запросы.

- Автор:
   https://github.com/Star-memory
