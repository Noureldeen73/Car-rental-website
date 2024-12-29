import React, { useState } from 'react';
import '../styles/LoginRegister.css';

function Register() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://127.0.0.1:8000/register/create_user/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `email=${encodeURIComponent(formData.email)}&password=${encodeURIComponent(formData.password)}&admin=${false}`,
      });
      
      if (response.ok) {
        alert('Registration successful!');
      } else {
        const error = await response.json();
        alert(`Registration failed: ${error.detail}`);
      }
    } catch (error) {
      alert('Registration failed: ' + error.message);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="register-container">
      <form className="register-form" onSubmit={handleSubmit}>
        <h2>Register</h2>
        <div className="form-group">
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>
        <button type="submit" className="submit-button">Register</button>
      </form>
    </div>
  );
}

export default Register; 