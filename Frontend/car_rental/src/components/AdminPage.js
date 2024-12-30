import React, { useState } from 'react';
import '../styles/AdminPage.css';

function AdminPage() {
  const [activeSection, setActiveSection] = useState(null);
  const [periodData, setPeriodData] = useState({ startDate: '', endDate: '' });
  const [carData, setCarData] = useState({ plateNumber: '' });
  const [customerData, setCustomerData] = useState({ customerId: '' });
  const [results, setResults] = useState(null);
  const [addCarForm, setAddCarForm] = useState({
    plateNumber: '',
    model: '',
    brand: '',
    year: '',
    officeId: '',
    price: '',
    numPassengers: ''
  });

  const handlePeriodSubmit = async (endpoint) => {
    try {
      const queryString = new URLSearchParams({
        start_date: periodData.startDate,
        end_date: periodData.endDate
      }).toString();
      
      const response = await fetch(`http://127.0.0.1:8000/Admin/${endpoint}/?${queryString}`);
      if (response.ok) {
        const data = await response.json();
        setResults(data);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleCarReservations = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/Admin/get_reservations_by_car/?plat_id=${carData.plateNumber}`);
      if (response.ok) {
        const data = await response.json();
        setResults(data);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleCustomerReservations = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/Admin/get_reservations_by_customer/?customer_id=${customerData.customerId}`);
      if (response.ok) {
        const data = await response.json();
        setResults(data);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleAddCar = async (e) => {
    e.preventDefault();
    try {
      const queryString = new URLSearchParams({
        plate_number: addCarForm.plateNumber,
        model: addCarForm.model,
        brand: addCarForm.brand,
        year: parseInt(addCarForm.year),
        office_id: parseInt(addCarForm.officeId),
        price: parseFloat(addCarForm.price),
        num_passengers: parseInt(addCarForm.numPassengers)
      }).toString();

      const response = await fetch(`http://127.0.0.1:8000/Admin/add_car/?${queryString}`, {
        method: 'POST'
      });

      if (response.ok) {
        alert('Car added successfully');
        setAddCarForm({
          plateNumber: '',
          model: '',
          brand: '',
          year: '',
          officeId: '',
          price: '',
          numPassengers: ''
        });
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="admin-page">
      <div className="admin-menu">
        <button onClick={() => setActiveSection('period')}>Period Reservations</button>
        <button onClick={() => setActiveSection('daily')}>Daily Payments</button>
        <button onClick={() => setActiveSection('car')}>Car Reservations</button>
        <button onClick={() => setActiveSection('customer')}>Customer Reservations</button>
        <button onClick={() => setActiveSection('addCar')}>Add New Car</button>
      </div>

      <div className="admin-content">
        {activeSection === 'period' && (
          <div className="section">
            <h2>Period Reservations</h2>
            <input
              type="date"
              value={periodData.startDate}
              onChange={(e) => setPeriodData({...periodData, startDate: e.target.value})}
            />
            <input
              type="date"
              value={periodData.endDate}
              onChange={(e) => setPeriodData({...periodData, endDate: e.target.value})}
            />
            <button onClick={() => handlePeriodSubmit('get_all_reservations_in_period')}>
              Get Reservations
            </button>
          </div>
        )}

        {activeSection === 'daily' && (
          <div className="section">
            <h2>Daily Payments</h2>
            <input
              type="date"
              value={periodData.startDate}
              onChange={(e) => setPeriodData({...periodData, startDate: e.target.value})}
            />
            <input
              type="date"
              value={periodData.endDate}
              onChange={(e) => setPeriodData({...periodData, endDate: e.target.value})}
            />
            <button onClick={() => handlePeriodSubmit('get_daily_pay_in_period')}>
              Get Payments
            </button>
          </div>
        )}

        {activeSection === 'car' && (
          <div className="section">
            <h2>Car Reservations</h2>
            <input
              type="text"
              placeholder="Plate Number"
              value={carData.plateNumber}
              onChange={(e) => setCarData({plateNumber: e.target.value})}
            />
            <button onClick={handleCarReservations}>Get Car Reservations</button>
          </div>
        )}

        {activeSection === 'customer' && (
          <div className="section">
            <h2>Customer Reservations</h2>
            <input
              type="number"
              placeholder="Customer ID"
              value={customerData.customerId}
              onChange={(e) => setCustomerData({customerId: e.target.value})}
            />
            <button onClick={handleCustomerReservations}>Get Customer Reservations</button>
          </div>
        )}

        {activeSection === 'addCar' && (
          <div className="section">
            <h2>Add New Car</h2>
            <form onSubmit={handleAddCar}>
              <input
                type="text"
                placeholder="Plate Number"
                value={addCarForm.plateNumber}
                onChange={(e) => setAddCarForm({...addCarForm, plateNumber: e.target.value})}
                required
              />
              <input
                type="text"
                placeholder="Model"
                value={addCarForm.model}
                onChange={(e) => setAddCarForm({...addCarForm, model: e.target.value})}
                required
              />
              <input
                type="text"
                placeholder="Brand"
                value={addCarForm.brand}
                onChange={(e) => setAddCarForm({...addCarForm, brand: e.target.value})}
                required
              />
              <input
                type="number"
                placeholder="Year"
                value={addCarForm.year}
                onChange={(e) => setAddCarForm({...addCarForm, year: e.target.value})}
                required
              />
              <input
                type="number"
                placeholder="Office ID"
                value={addCarForm.officeId}
                onChange={(e) => setAddCarForm({...addCarForm, officeId: e.target.value})}
                required
              />
              <input
                type="number"
                placeholder="Price"
                value={addCarForm.price}
                onChange={(e) => setAddCarForm({...addCarForm, price: e.target.value})}
                required
              />
              <input
                type="number"
                placeholder="Number of Passengers"
                value={addCarForm.numPassengers}
                onChange={(e) => setAddCarForm({...addCarForm, numPassengers: e.target.value})}
                required
              />
              <button type="submit">Add Car</button>
            </form>
          </div>
        )}

        {results && (
          <div className="results-section">
            <pre>{JSON.stringify(results, null, 2)}</pre>
          </div>
        )}
      </div>
    </div>
  );
}

export default AdminPage;
  