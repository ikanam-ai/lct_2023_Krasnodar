# lct_2023_Krasnodar
Репозиторий команды ikanam
"Веб-сервис для видеодетекции объектов нестационарной незаконной торговли"
- Ссылка на прототип - http://89.232.160.30:7484/


**Описание проекта**
Этот репозиторий содержит исходный код и ресурсы для веб-сервиса, разработанного с целью выявления объектов нестационарной незаконной торговли. Проект интегрирует современные технологии в области компьютерного зрения, нейронных сетей, визуализации аналитики и веб-приложений.

**Архитектура решения**
**Технологии**
- **Разметка изображений**: CVAT
- **Нейронные сети**: Pytorch, YoloV8, TorchVision, Scikit-learn
- **Визуализация аналитики**: Plotly
- **Веб-приложение**: Streamlit
- **Брокер сообщений**: RabbitMQ
- **Хранение данных**: MongoDb 

**Структура репозитория**
- worker/: Код микросервиса для распознавания архивов и rtc трансляций, внути него есть yolo модель
- notif/: Код микросервиса для рассылки уведомлений о детектах
- lct/: Код микросервиса для выставления задач распознавания и просмотрв результатов

**Использование**
+ 1 вариант, без docker 
  - Клонируйте репозиторий: git clone https://github.com/yourusername/illegal-trade-detection.git
  - Установите зависимости в каждом микросервисе: poetry install  
  - Установить переменные окружения для rabbitMq и mongoDb
  - Запустить каждый микросервис: poetry run start
+ 2 вариант, в docker
  - Клонируйте репозиторий: git clone https://github.com/yourusername/illegal-trade-detection.git
  - запустить все миикросервисы из docker-compose: docker-compose up
    
*Список всех переменных окружения:
```
MONGO_HOST: Адрес сервера MongoDB.
MONGO_PORT: Порт сервера MongoDB (по умолчанию 27017).
MONGO_DATABASE: Имя базы данных MongoDB.
MONGO_USERNAME: Имя пользователя MongoDB для аутентификации.
MONGO_PASSWORD: Пароль пользователя MongoDB для аутентификации.
NOTIF_PORT: Порт для сервиса уведомлений.
ADMIN_NOTIF_PSWD: Пароль для создания уведомлений.
NOTIF_PSWD: Пароль для получения уведомлений.
NOTIF_URL: URL сервиса уведомлений.
RABBITMQ_HOST: Адрес сервера RabbitMQ.
RABBITMQ_PORT: Порт сервера RabbitMQ (по умолчанию 5672).
RABBITMQ_USER: Имя пользователя RabbitMQ для аутентификации.
RABBITMQ_PASSWORD: Пароль пользователя RabbitMQ для аутентификации.
RABBITMQ_VHOST: Виртуальный хост RabbitMQ.
EXCHANGE_NAME: Имя обмена RabbitMQ для входных видео.
DEQUE_NAME: Имя очереди RabbitMQ для входных видео.
BINDING_KEY: Ключ привязки RabbitMQ (используется при маршрутизации сообщений).
MODEL_PATH: Путь к файлу yolo модели.
USER_LOGIN: Логин для авторизации на сервисе
USER_PASSWORD: Пароль для авторизации на сервисе
```
*Дефотные данные для входа:
- Логин: jsmith
- Пароль: abc

**Ресурсы**
- Наборы видеопотоков из системы "Умный город".
- Кадры размещения различных стационарных и нестационарных объектов уличной торговли.

**Дополнительная информация**
Для подробной документации и инструкций по использованию обратитесь к документации проекта.

**Заключение** 
Этот проект предоставляет мощное средство для борьбы с нестационарной незаконной торговлей, объединяя в себе современные технологии в области компьютерного зрения и веб-разработки. Надеемся, что он станет эффективным инструментом в улучшении общественной безопасности и контроля за незаконной торговлей.
