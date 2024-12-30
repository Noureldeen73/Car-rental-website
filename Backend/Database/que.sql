-- Insert into User table
INSERT INTO "User" (email, password, is_admin) VALUES
('john.doe@example.com', 'password123', FALSE),
('jane.smith@example.com', 'securepassword', FALSE),
('admin.one@example.com', 'adminpass', TRUE),
('admin.two@example.com', 'strongpass', TRUE),
('customer.one@example.com', 'custpassword1', FALSE),
('customer.two@example.com', 'custpassword2', FALSE),
('customer.three@example.com', 'custpassword3', FALSE),
('customer.four@example.com', 'custpassword4', FALSE),
('customer.five@example.com', 'custpassword5', FALSE),
('test.user@example.com', 'testpassword', FALSE);

-- Insert into Customer table
INSERT INTO Customer (first_name, last_name, phone_number, city, street, zip_code, user_id) VALUES
('John', 'Doe', '+1234567890', 'New York', '5th Ave', '10001', 1),
('Jane', 'Smith', '+9876543210', 'Los Angeles', 'Hollywood Blvd', '90028', 2),
('Alice', 'Brown', '+1231231234', 'Chicago', 'Michigan Ave', '60611', 5),
('Bob', 'White', '+3213214321', 'Houston', 'Main St', '77001', 6),
('Charlie', 'Davis', '+4567891234', 'Phoenix', 'Central Ave', '85001', 7),
('David', 'Clark', '+7891234567', 'Philadelphia', 'Broad St', '19104', 8),
('Emily', 'Martinez', '+3216549870', 'San Antonio', 'Commerce St', '78205', 9),
('Frank', 'Thompson', '+6549873210', 'San Diego', 'Park Blvd', '92101', 10);

-- Insert into Office table
INSERT INTO Office (office_name, city, street, zip_code) VALUES
('Office A', 'New York', '5th Ave', '10001'),
('Office B', 'Los Angeles', 'Hollywood Blvd', '90028');

-- Insert into Admin table
INSERT INTO Admin (first_name, last_name, user_id, office_id) VALUES
('Admin', 'One', 3, 1),
('Admin', 'Two', 4, 2);

-- Insert into Car table
INSERT INTO Car (plate_number, model, brand, year, available, office_id, price, num_passengers) VALUES
('XYZ123', 'Civic', 'Honda', 2020, TRUE, 1, 50.00, 5),
('ABC456', 'Accord', 'Honda', 2019, TRUE, 1, 60.00, 5),
('DEF789', 'Camry', 'Toyota', 2021, TRUE, 2, 55.00, 5),
('GHI012', 'Corolla', 'Toyota', 2018, TRUE, 2, 45.00, 5),
('JKL345', 'Escape', 'Ford', 2020, TRUE, 1, 65.00, 7),
('MNO678', 'Focus', 'Ford', 2019, TRUE, 1, 50.00, 5),
('PQR901', 'Model 3', 'Tesla', 2022, TRUE, 2, 100.00, 5),
('STU234', 'Model Y', 'Tesla', 2021, TRUE, 2, 120.00, 7),
('VWX567', 'Tahoe', 'Chevrolet', 2020, TRUE, 1, 90.00, 8),
('YZA890', 'Impala', 'Chevrolet', 2018, TRUE, 1, 60.00, 5);

-- Insert into Reservation table
INSERT INTO Reservation (reservation_date, pick_up_date, return_date, plate_number, customer_id) VALUES
('2024-12-25 08:00:00', '2024-12-26 09:00:00', '2024-12-30 10:00:00', 'XYZ123', 1),
('2024-12-20 08:00:00', '2024-12-22 09:00:00', '2024-12-28 10:00:00', 'ABC456', 2),
('2024-12-15 08:00:00', '2024-12-16 09:00:00', '2024-12-22 10:00:00', 'DEF789', 3),
('2024-11-01 08:00:00', '2024-11-10 09:00:00', '2024-11-15 10:00:00', 'GHI012', 4),
('2024-12-18 08:00:00', '2024-12-19 09:00:00', '2024-12-20 10:00:00', 'JKL345', 5),
('2025-03-05 08:00:00', '2025-04-05 08:00:00', '2025-05-30 10:00:00', 'MNO678', 1),
('2023-12-20 08:00:00', '2024-03-05 08:00:00', '2024-12-28 10:00:00', 'STU234', 2),
('2024-12-16 08:00:00', '2024-12-17 09:00:00', '2024-12-22 10:00:00', 'PQR901', 3),
('2024-11-04 08:00:00', '2024-11-09 09:00:00', '2024-11-15 10:00:00', 'VWX567', 4),
('2024-12-28 08:00:00', '2025-01-19 09:00:00', '2025-01-20 10:00:00', 'YZA890', 5);

-- Insert into Payment table
INSERT INTO Payment (payment_type, payment_date, total_price, reservation_id) VALUES
('Credit Card', '2024-12-25 08:00:00', 200.00, 1),
('Debit Card', '2024-12-20 08:00:00', 180.00, 2),
('PayPal', '2024-12-15 08:00:00', 330.00, 3),
('Credit Card', '2024-11-01 08:00:00', 400.00, 4),
('Cash', '2024-12-18 08:00:00', 150.00, 5),
('Credit Card', '2025-03-05 08:00:00', 200.00, 6),
('Debit Card', '2023-12-20 08:00:00', 180.00, 7),
('PayPal', '2024-12-16 08:00:00', 330.00, 8),
('Credit Card', '2024-11-04 08:00:00', 400.00, 9),
('Cash', '2024-12-28 08:00:00', 150.00, 10);
