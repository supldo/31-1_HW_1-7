'''Database SQL Queries'''

'''Telegram Users'''
# Создание таблицы для Telegram Users
create_user_table_query = """
        CREATE TABLE IF NOT EXISTS telegram_users(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        telegram_id INTEGER,
        username CHAR(50), 
        first_name CHAR(50), 
        last_name CHAR(50),
        reference_link TEXT NULL,
        UNIQUE (telegram_id))
"""
# Добавление пользователя в таблицу Telegram Users
insert_user_table_query = """
    INSERT OR IGNORE INTO telegram_users (telegram_id, username, first_name, last_name) VALUES (?,?,?,?)
"""
# Вывод все пользователей из таблицы Telegram Users
select_user_table_query = """
    SELECT * FROM telegram_users
"""


'''Quiz'''
# Создание таблицы для Quiz   # hw1   # 3.0.
create_quiz = """
    CREATE TABLE IF NOT EXISTS quiz (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER,
        quiz CHAR(10),
        quiz_option INTEGER,
        FOREIGN KEY (telegram_id) REFERENCES telegram_users (telegram_id)
    )
"""
# Добавление ответов в таблицу Quiz
insert_quiz = """
    INSERT OR IGNORE INTO quiz (telegram_id, quiz, quiz_option) VALUES (?, ?, ?)
"""


'''User ban'''  # hw2
# Создание таблицы для User Ban
create_user_ban = """
    CREATE TABLE IF NOT EXISTS user_ban (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER,
        group_id INTEGER,
        datetime DATETIME DEFAULT (datetime('now', '+6 hours')) NOT NULL,
        reasons TEXT,
        FOREIGN KEY (telegram_id) REFERENCES telegram_users (telegram_id)
    )
"""
# Добавление плохих пользователей в таблицу User Ban
insert_user_ban = """
    INSERT INTO user_ban(telegram_id, group_id, reasons) VALUES (?, ?, ?)
"""
# Вывод плохого пользователя за последние 24 часа из таблицы User Ban
select_user_ban = """
    SELECT telegram_id FROM user_ban WHERE telegram_id == ? AND group_id == ? AND datetime('now', '-18 hours') < datetime('now', '+6 hours')
"""
# Вывод всех пользователей потенциальных на бан
select_potential_user_ban = """
    SELECT * FROM
        telegram_users
    INNER JOIN
        user_ban
    ON
        telegram_users.telegram_id = user_ban.telegram_id
    WHERE datetime('now', '-18 hours') < datetime('now', '+6 hours')
    GROUP BY telegram_users.telegram_id
    ORDER BY user_ban.datetime DESC;
"""


'''User survey'''  # hw3
# Создание таблицы для User survey
create_user_survey = """
    CREATE TABLE IF NOT EXISTS user_survey (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        idea TEXT,
        problems TEXT,
        assessment INTEGER,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES telegram_users (telegram_id)
    )
"""
# Добавление опроса в таблицу User survey
insert_user_survey = """
    INSERT INTO user_survey (idea, problems, assessment, user_id) VALUES (?, ?, ?, ?)
"""
# Выбор опросов из таблицы User survey
select_user_survey = """
    SELECT * FROM user_survey
"""
# Выбор опроса по ID из таблицы User survey
select_user_survey_by_id = """
    SELECT * FROM
        telegram_users
    LEFT JOIN 
        user_survey
    ON user_survey.user_id = telegram_users.telegram_id
    WHERE user_survey.id = ?
"""


'''Complaint'''     # hw4
create_complaint = """
    CREATE TABLE IF NOT EXISTS complaint(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER,
        telegram_id_bad_user INTEGER,
        reason TEXT,
        count INTEGER
    )
"""
insert_complaint = """
    INSERT OR IGNORE INTO complaint(telegram_id, telegram_id_bad_user, reason, count)
    VALUES (?, ?, ?, ?)
"""
select_id_by_username = """
    SELECT telegram_id FROM telegram_users WHERE username = ?
"""
select_complaint = """
    SELECT count FROM complaint WHERE telegram_id_bad_user = ?
"""
select_complaint_check = """
    SELECT telegram_id FROM complaint WHERE telegram_id = ? AND telegram_id_bad_user = ?
"""


'''Wallet'''     # hw5
create_wallet = """
    CREATE TABLE IF NOT EXISTS wallet (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        point INTEGER,
        FOREIGN KEY (user_id) REFERENCES telegram_users (telegram_id),
        UNIQUE(user_id)
    )
"""
insert_wallet = """
    INSERT OR IGNORE INTO wallet(user_id, point) VALUES (?, 0)
"""
select_wallet = """
    SELECT point FROM wallet WHERE user_id = ?
"""
update_wallet = """
    UPDATE wallet SET point = point + ? WHERE user_id = ?
"""


'''Referral'''     # hw5
create_referral = """
    CREATE TABLE IF NOT EXISTS referral (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner_link_telegram_id INTEGER,
        referral_telegram_id INTEGER,
        UNIQUE(referral_telegram_id)
    )
"""
insert_referral = """
    INSERT INTO referral(owner_link_telegram_id, referral_telegram_id) VALUES (?, ?)
"""
select_referral = """
    SELECT * FROM referral WHERE referral_telegram_id = ?
"""
select_all_referrals = """
    SELECT
        user.username, user.first_name, user.last_name
    FROM referral AS ref
    LEFT JOIN telegram_users AS user
    ON ref.referral_telegram_id = user.telegram_id
    WHERE owner_link_telegram_id = ?
"""


'''Reference link'''     # hw5
update_user_reference_link_query = """
    UPDATE telegram_users SET reference_link = ? WHERE telegram_id = ?
"""
select_user_by_id_return_link_query = """
    SELECT reference_link FROM telegram_users WHERE telegram_id = ?
"""
select_user_by_link = """
    SELECT telegram_id FROM telegram_users WHERE reference_link LIKE ?
"""


"""Scraper note"""     # hw6
create_scraper_note = """
    CREATE TABLE IF NOT EXISTS scraper_note(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_user INTEGER,
        link_anime TEXT,
        FOREIGN KEY (id_user) REFERENCES telegram_users (id),
        UNIQUE (id_user, link_anime)
    )
"""
insert_scraper_note = """
    INSERT OR IGNORE INTO scraper_note(id_user, link_anime) VALUES (?, ?)
"""
select_scraper_note = """
    SELECT id_user, link_anime FROM scraper_note WHERE id_user = ?
"""