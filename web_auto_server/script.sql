-- Database: web_auto_db

-- DROP DATABASE IF EXISTS web_auto_db;

CREATE DATABASE web_auto_db
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Russian_Russia.1251'
    LC_CTYPE = 'Russian_Russia.1251'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

-- Таблица users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    login VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Таблица cars
CREATE TABLE cars (
    id SERIAL PRIMARY KEY,
    make VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    year INT CHECK (year >= 1886) NOT NULL,  -- Проверка на год выпуска (первый автомобиль создан в 1886 году)
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    owner INT REFERENCES users(id) ON DELETE CASCADE  -- Внешний ключ на пользователя (владелец)
);

-- Таблица comments
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    car INT REFERENCES cars(id) ON DELETE CASCADE,  -- Внешний ключ на автомобиль
    author INT REFERENCES users(id) ON DELETE CASCADE  -- Внешний ключ на автора комментария
);

-- Добавляем пользователей
INSERT INTO users (login, password) VALUES
('user1', 'password1'),
('user2', 'password2'),
('user3', 'password3'),
('user4', 'password4'),
('user5', 'password5');

-- Добавляем автомобили
INSERT INTO cars (make, model, year, description, owner) VALUES
('Toyota', 'Camry', 2021, 'Компактный седан с отличной экономией топлива и современными технологиями безопасности.', 1),
('Ford', 'Mustang', 2020, 'Спортивный автомобиль с мощным двигателем и агрессивным дизайном.', 2),
('Honda', 'Civic', 2020, 'Надежный и экономичный седан, идеален для городской эксплуатации.', 3),
('BMW', 'X5', 2021, 'Роскошный кроссовер с мощным двигателем и современными технологиями.', 4),
('Audi', 'A6', 2022, 'Элегантный седан с высоким уровнем комфорта и передовыми системами безопасности.', 5),
('Mercedes', 'C-Class', 2021, 'Стильный и мощный седан с передовыми технологиями.', 1),
('Chevrolet', 'Malibu', 2019, 'Надежный и экономичный седан с удобным салоном.', 2),
('Tesla', 'Model S', 2021, 'Электрический автомобиль с высокой производительностью и автономностью.', 3),
('Lexus', 'RX 350', 2022, 'Комфортный и мощный кроссовер с высококлассной отделкой.', 4),
('Volkswagen', 'Passat', 2020, 'Экономичный седан с удобным салоном и хорошей динамикой.', 5);

-- Добавляем комментарии к каждому автомобилю (по 2 комментария)
INSERT INTO comments (content, car, author) VALUES
('Отличная машина, но дорогая в обслуживании.', 1, 1),
('Экономичная и надёжная, рекомендую.', 1, 2),
('Очень мощный автомобиль, звук двигателя впечатляет.', 2, 3),
('Дизайн на высоте, но высокая цена.', 2, 4),
('Идеальная для города, расход топлива небольшой.', 3, 5),
('Надежная и неприхотливая в эксплуатации.', 3, 1),
('Кроссовер с отличной проходимостью, стоит своих денег.', 4, 2),
('Технологии на уровне, но не хватает драйва.', 4, 3),
('Комфортный и быстрый, отличный вариант для дальних поездок.', 5, 4),
('Цена высоковата, но стоит своих денег.', 5, 5),
('Отличное сочетание стиля и производительности.', 6, 1),
('Подвеска немного жёсткая, но управляемость отличная.', 6, 2),
('Удобный автомобиль для семейных поездок.', 7, 3),
('Бюджетный вариант, но качественный.', 7, 4),
('Электромобиль с впечатляющей динамикой, очень тихий.', 8, 5),
('Технологичен, но дорогой.', 8, 1),
('Просторный салон и мощный двигатель.', 9, 2),
('Удобный в управлении и очень комфортный.', 9, 3),
('Экономичный и приятный в эксплуатации.', 10, 4),
('Немного слабоват в плане динамики, но комфортен.', 10, 5);
