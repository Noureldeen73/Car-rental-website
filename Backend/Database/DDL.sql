CREATE TABLE IF NOT EXISTS "User"(
    user_id int PRIMARY KEY,
    email varchar(255) NOT NULL,
    password varchar(255) NOT NULL,
    is_admin boolean NOT NULL
);
CREATE TABLE IF NOT EXISTS Customer(
    customer_id int PRIMARY KEY,
    first_name varchar(255) NOT NULL,
    last_name varchar(255) NOT NULL,
    phone_number varchar(17) NOT NULL,
    city varchar(255) NOT NULL,
    street varchar(255) NOT NULL,
    zip_code varchar(10) NOT NULL,
    user_id int NOT NULL,
    FOREIGN KEY (user_id) REFERENCES "User"(user_id)
);
CREATE TABLE IF NOT EXISTS Office(
    office_id int PRIMARY KEY,
    office_name varchar(255) NOT NULL,
    city varchar(255) NOT NULL,
    street varchar(255) NOT NULL,
    zip_code varchar(10) NOT NULL
);
CREATE TABLE IF NOT EXISTS Admin(
    admin_id int PRIMARY KEY,
    first_name varchar(255) NOT NULL,
    last_name varchar(255) NOT NULL,
    user_id int NOT NULL,
    office_id int NOT NULL,
    FOREIGN KEY (user_id) REFERENCES "User"(user_id),
    FOREIGN KEY (office_id) REFERENCES Office(office_id)
);
CREATE TABLE IF NOT EXISTS Car
(
    car_id       int PRIMARY KEY,
    plate_number varchar(10)  NOT NULL,
    model        varchar(255) NOT NULL,
    year         int          NOT NULL,
    free       boolean      NOT NULL,
    office_id    int          NOT NULL,
    FOREIGN KEY (office_id) REFERENCES Office (office_id)
);
CREATE TABLE IF NOT EXISTS Reservation
(
    reservation_id   int PRIMARY KEY,
    reservation_date timestamp NOT NULL,
    pick_up_date     timestamp NOT NULL,
    return_date      timestamp NOT NULL,
    car_id           int       NOT NULL,
    customer_id      int       NOT NULL,
    FOREIGN KEY (car_id) REFERENCES Car (car_id),
    FOREIGN KEY (customer_id) REFERENCES Customer (customer_id)
);
CREATE TABLE IF NOT EXISTS Payment
(
    payment_id     int PRIMARY KEY,
    payment_type  varchar(255) NOT NULL,
    payment_date  timestamp NOT NULL,
    amount        float        NOT NULL,
    reservation_id int         NOT NULL,
    FOREIGN KEY (reservation_id) REFERENCES Reservation (reservation_id)
);

