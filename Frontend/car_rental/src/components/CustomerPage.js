import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import '../styles/CustomerPage.css';
import carImage from '../car.png';

function CustomerPage() {
  const [cars, setCars] = useState([]);
  const [customerId, setCustomerId] = useState(null);
  const [filters, setFilters] = useState({
    model: '',
    year: '',
    city: ''
  });
  const navigate = useNavigate();
  const location = useLocation();
  const [results, setResults] = useState(null);
  const userId = location.state?.userId;

  useEffect(() => {
    const fetchCustomerId = async () => {
      if (!userId) {
        navigate('/'); // Redirect to login if no userId
        return;
      }

      try {
        const response = await fetch(`http://127.0.0.1:8000/user/customer_id_by_user_id/?user_id=${parseInt(userId)}`);
        if (response.ok) {
          const data = await response.json();
          setCustomerId(data.customer_id);
          console.log(userId);
          console.log(data);
          console.log('Customer ID:', customerId);
        } else {
          console.error('Failed to fetch customer ID');
        }
      } catch (error) {
        console.error('Error fetching customer ID:', error);
      }
    };

    fetchCustomerId();
  }, [userId, navigate]);

  const handleFilterChange = (e) => {
    setFilters({
      ...filters,
      [e.target.name]: e.target.value
    });
  };

  const fetchCars = async () => {
    try {
      const queryString = new URLSearchParams({
        model: filters.model || '',
        year: filters.year || '0',
        city: filters.city || ''
      }).toString();

      const response = await fetch(`http://127.0.0.1:8000/Car/get_car_by_filter/?${queryString}`);
      if (response.ok) {
        const data = await response.json();
        setCars(data);
        console.log(cars);
      }
      else
        setCars([]);
    } catch (error) {
      console.error('Error fetching cars:', error);
    }
  };


  const handleReserve = (plateNum) => {
    if (!customerId) {
      alert('Please wait while we load your customer information');
      return;
    }
    navigate(`/reserve/${plateNum}`, { 
      state: { 
        customerId,
        userId
      } 
    });
  };

  const updateAvailability = async () => {
    try {
      await fetch('http://127.0.0.1:8000/Admin/update_av/');
    } catch (error) {
      console.error('Error updating availability:', error);
    }
  };

  const handleCustomerReservations = async () => {
    try {
      await updateAvailability();
      const response = await fetch(`http://127.0.0.1:8000/Admin/get_reservations_by_customer/?customer_id=${customerId}`);
      if (response.ok) {
        const data = await response.json();
        setResults(data);
        console.log(data);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleLogout = () => {
    navigate(`/`);
  };

  useEffect(() => {
    fetchCars();
  }, [filters]);

  return (
      <div className="customer-page">
        <button
            className="logout-button"
            onClick={() => handleLogout()}
        >
          Logout
        </button>
        <button
            className="logout-button"
            onClick={() => handleCustomerReservations()}
        >
          Get All Reservations
        </button>
        <div className="filters-section">
          <input
              type="text"
              name="model"
              placeholder="Car Model"
              value={filters.model}
              onChange={handleFilterChange}
          />
          <input
              type="number"
              name="year"
              placeholder="Year"
              value={filters.year}
              onChange={handleFilterChange}
          />
          <input
              type="text"
              name="city"
              placeholder="City"
              value={filters.city}
              onChange={handleFilterChange}
          />
        </div>

        <div className="cars-grid">
          {cars.map((car) => (
              <div key={car.plate_number} className="car-card">
                <img src={`/${car.img_path}`} alt={car.model} className="car-image"/>
                <div className="car-info">
                  <h3>{car.model}</h3>
                  <p>Year: {car.year}</p>
                  <p>City: {car.city}</p>
                  <button
                      className="reserve-button"
                      onClick={() => handleReserve(car.plate_number)}
                  >
                    Reserve
                  </button>
                </div>
              </div>
          ))}
        </div>

        { results &&
          <div className="results-section">
            <div className="customer-info">
              <h3>Customer Information</h3>
              <p><strong>Name:</strong> {results.customer_data.first_name} {results.customer_data.last_name}</p>
              <p><strong>Phone:</strong> {results.customer_data.phone_number}</p>
              <p>
                <strong>Address:</strong> {results.customer_data.street}, {results.customer_data.city}, {results.customer_data.zip_code}
              </p>
            </div>
            <div className="results-table">
              <h3>Customer Reservations</h3>
              <table>
                <thead>
                <tr>
                  <th>Car Model</th>
                  <th>Office</th>
                  <th>Pickup Date</th>
                  <th>Return Date</th>
                  <th>Total Price</th>
                </tr>
                </thead>
                <tbody>
                {results.reservations.map((reservation, index) => (
                    <tr key={index}>
                      <td>{reservation.model} ({reservation.year})</td>
                      <td>{reservation.office_name} - {reservation.city}</td>
                      <td>{new Date(reservation.pick_up_date).toLocaleDateString()}</td>
                      <td>{new Date(reservation.return_date).toLocaleDateString()}</td>
                      <td>${reservation.total_price}</td>
                    </tr>
                ))}
                </tbody>
              </table>
            </div>
          </div>
          }
        </div>
          );
        }

        export default CustomerPage;
