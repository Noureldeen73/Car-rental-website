# Car Rental Database

## Overview

This project is a car rental database system designed to manage users, customers, admins, offices, cars, reservations, and payments. The database is implemented using SQL and includes various tables to store and manage the data.

## Database Structure

The database consists of the following tables:
- **User**: Stores user information including email, hashed password, and admin status.
- **Customer**: Stores customer details such as name, phone number, address, and associated user ID.
- **Office**: Stores office details including name, address, and zip code.
- **Admin**: Stores admin details including name, associated user ID, and office ID.
- **Car**: Stores car details including plate number, model, brand, year, availability, office ID, price, number of passengers, and image path.
- **Reservation**: Stores reservation details including reservation date, pick-up date, return date, plate number, and customer ID.
- **Payment**: Stores payment details including payment type, payment date, total price, and reservation ID.

## Setup Instructions

1. Clone the repository:
    ```sh
    git clone git@github.com:Noureldeen73/Car-rental-website.git
    ```

2. Navigate to the project directory:
    ```sh
    cd Car-rental-website
    ```

3. Install PostgreSQL:
    - **Windows**: Download and install PostgreSQL from [here](https://www.postgresql.org/download/windows/).
    - **macOS**: Use Homebrew to install PostgreSQL:
        ```sh
        brew install postgresql
        ```
    - **Linux**: Use your package manager to install PostgreSQL:
        ```sh
        sudo apt-get install postgresql postgresql-contrib
        ```

4. Start PostgreSQL service:
    - **Windows**: Start the PostgreSQL service from the Services app.
    - **macOS** and **Linux**:
        ```sh
        sudo service postgresql start
        ```

5. Import the SQL script to your database:
    ```sh
    psql -U <username> -d <database_name> -f Backend/Database/que.sql
    ```

6. Install FastAPI and Uvicorn:
    ```sh
    pip install fastapi uvicorn
    ```

7. Run the FastAPI server:
    ```sh
    uvicorn Backend.main:app --reload
    ```

8. Install Node.js and npm:
    - **Windows** and **macOS**: Download and install Node.js from [here](https://nodejs.org/).
    - **Linux**:
        ```sh
        sudo apt-get install nodejs npm
        ```

9. Navigate to the frontend directory and install dependencies:
    ```sh
    cd frontend
    npm install
    ```

10. Start the React development server:
    ```sh
    npm start
    ```

## Usage

- The database can be queried to manage car rentals, including adding new users, customers, admins, offices, cars, reservations, and payments.
- Ensure that passwords are hashed before inserting them into the database for security purposes.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request with your changes.