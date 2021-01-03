DROP TABLE IF EXISTS weather_hourly;
DROP TABLE IF EXISTS weather_daily;
DROP TABLE IF EXISTS metro;
DROP TABLE IF EXISTS rain;
DROP TABLE IF EXISTS bikes;

CREATE TABLE weather_hourly(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    weather_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    latitude FLOAT,
    longitude FLOAT,
    weather_weekday TEXT,
    hour INTEGER,
    temp INTEGER,
    icon TEXT
);

CREATE TABLE weather_daily(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    weather_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    latitude FLOAT,
    longitude FLOAT,
    weather_weekday TEXT,
    weather_day INT,
    temp_min INT,
    temp_max INT,
    icon TEXT
);

CREATE TABLE metro(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    metro_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    metro_line TEXT,
    slug TEXT,
    title TEXT,
    metro_message TEXT
);

CREATE TABLE rain(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    latitude FLOAT,
    longitude FLOAT,
    rain_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    next_hour FLOAT,
    next_12_hours FLOAT
);

CREATE TABLE bikes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    latitude FLOAT,
    longitude FLOAT,
    bikes_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    bikes_name TEXT,
    mechanical INTEGER,
    ebike INTEGER,
    taux_remplissage INTEGER
)