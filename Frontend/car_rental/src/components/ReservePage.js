import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import '../styles/ReservePage.css';
import carImage from '../car.png';

function ReservePage() {
  const [car, setCar] = useState(null);
  const { carId } = useParams();

  useEffect(() => {
    const fetchCarDetails = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/Car/get_car_by_plate_num/?plate_number=${carId}`);
        if (response.ok) {
          const data = await response.json();
          setCar(data);
        }
      } catch (error) {
        console.error('Error fetching car details:', error);
      }
    };

    fetchCarDetails();
  }, [carId]);

  if (!car) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="reserve-page">
      <div className="car-details-card">
        <div className="car-image-container">
          <img src={carImage} alt={car.model} className="car-detail-image" />
        </div>
        <div className="car-details-info">
          <h2>{car.model}</h2>
          <div className="details-grid">
            <div className="detail-item">
              <span className="detail-label">Year:</span>
              <span className="detail-value">{car.year}</span>
            </div>
            <div className="detail-item">
              <span className="detail-label">City:</span>
              <span className="detail-value">{car.office_city}</span>
            </div>
            <div className="detail-item">
              <span className="detail-label">Plate Number:</span>
              <span className="detail-value">{car.plate_number}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ReservePage; 