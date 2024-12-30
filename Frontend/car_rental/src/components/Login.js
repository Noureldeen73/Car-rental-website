import React, { useState } from 'react';
import '../styles/LoginRegister.css';
import { useNavigate } from 'react-router-dom';

function Login() {
    const [formData, setFormData] = useState({
        email: '',
        password: ''
      });
    
      const navigate = useNavigate();
    
      const handleSubmit = async (e) => {
        e.preventDefault();
        try {
          const queryString = new URLSearchParams(formData).toString();
    
          const response = await fetch('http://127.0.0.1:8000/login/authenticate/?' + queryString, {
            method: 'GET',
          });
          
          if (response.ok) {
            const data = await response.json();
            if (data.is_admin) {
              navigate('/admin');
            } else {
              navigate('/customer', { state: { userId: data.user_id } });
            }
          } else {
            alert('Login failed');
          }
        } catch (error) {
          alert('Error during login: ' + error.message);
        }
      };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="login-container">
      <form className="login-form" onSubmit={handleSubmit}>
        <h2>Login</h2>
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
        <button type="submit" className="submit-button">Login</button>
      </form>
    </div>
  );
}

export default Login; 