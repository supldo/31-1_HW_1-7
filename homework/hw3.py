'''ДЗ #3'''
# 1.0. Добавить дополнительную логику Fsmcontext для прохождения опроса.
# 1.1. В таблице базы данных для опросника добавить такие поля как
# 1.1.0. ID
# 1.1.1. idea(новые идеи для улучшения бота)
# 1.1.2. problems(с какими проблемами встретились
# 1.1.3. telegram_id (должен быть связан с таблицей пользователей с помощью связи ForeignKey как на уроке)
# 1.2. К этому опроснику добавить еще одно поле с тематическим вопросом (на свое усмотрение)
# 2.0. Вывод списка опросов с id. После вывода списка ждать сообщения с выбором опроса по id и дать ему только тот опрос который он выбрал по id.
# 2.1. Вывод доступен только для админов
# 2.2. Список админов сохранить в config.py
# 2.3. Проверять админов по message.from_user.id (телеграм id)