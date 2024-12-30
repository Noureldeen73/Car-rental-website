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

  useEffect(() => {
    fetchCars();
  }, [filters]);

  return (
    <div className="customer-page">
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
            <img src={carImage} alt={car.model} className="car-image" />
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
    </div>
  );
}

export default CustomerPage;
