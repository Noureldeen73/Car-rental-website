-- Insert dummy data into the User table
INSERT INTO "User" (email, password, is_admin)
VALUES
('john.doe@example.com', 'password123', false),
('jane.smith@example.com', 'securepass456', false),
('alice.johnson@example.com', 'mypassword789', false),
('bob.brown@example.com', 'adminpassword0', true),
('charlie.williams@example.com', 'charliepass321', false);

INSERT INTO Customer (first_name, last_name, phone_number, city, street, zip_code, user_id)
VALUES
('John', 'Doe', '+201012345678', 'Cairo', '123 Main St', '12345', 1),
('Jane', 'Smith', '+201098765432', 'Giza', '456 Elm St', '54321', 2),
('Alice', 'Johnson', '+201055555555', 'Alexandria', '789 Ocean Ave', '98765', 3),
('Bob', 'Brown', '+201022222222', '6th of October', '202 Industrial Blvd', '11111', 4),
('Charlie', 'Williams', '+201077777777', 'Cairo', '456 Airport Rd', '67890', 5);

INSERT INTO Office (office_name, city, street, zip_code)
VALUES
('Downtown Office', 'Cairo', '123 Main St', '12345'),
('Airport Office', 'Cairo', '456 Airport Rd', '67890'),
('Suburban Office', 'Giza', '789 Suburb St', '54321'),
('Coastal Office', 'Alexandria', '101 Beach Ave', '98765'),
('Industrial Office', '6th of October', '202 Industrial Blvd', '11111');


INSERT INTO Car (plate_number, model, brand, year, available, office_id, num_passengers)
VALUES
('ABC12345', 'Corolla', 'Toyota', 2020, true, 1, 5),
('XYZ98765', 'Civic', 'Honda', 2019, false, 2, 7),
('LMN45678', 'Focus', 'Ford', 2018, true, 1, 4),
('PQR11223', 'Malibu', 'Chevrolet', 2021, false, 3, 2),
('TUV55667', 'Altima', 'Nissan', 2019, true, 2, 6),
('JKL88990', '3 Series', 'BMW', 2022, false, 1, 7),
('RST00112', 'A4', 'Audi', 2021, true, 3, 4),
('WXY34567', 'Passat', 'Volkswagen', 2020, true, 2, 2),
('FGH23456', 'C-Class', 'Mercedes-Benz', 2019, false, 1, 9),
('IJK67890', 'Impreza', 'Subaru', 2018, true, 3, 5);

INSERT INTO Reservation (reservation_date, pick_up_date, return_date, plate_number, customer_id)
VALUES
('2024-12-01 10:00:00', '2024-12-03 09:00:00', '2024-12-10 15:00:00', 'ABC12345', 1),
('2024-12-02 14:30:00', '2024-12-04 12:00:00', '2024-12-08 16:00:00', 'LMN45678', 2),
('2024-12-05 11:00:00', '2024-12-06 08:00:00', '2024-12-12 18:00:00', 'RST00112', 3),
('2024-12-06 09:15:00', '2024-12-07 10:00:00', '2024-12-14 11:30:00', 'FGH23456', 4),
('2024-12-07 16:45:00', '2024-12-09 14:00:00', '2024-12-15 19:00:00', 'IJK67890', 5);
