import './App.css';
import Register from './components/Register';
import Login from './components/Login';
import CustomerPage from './components/CustomerPage';
import AdminPage from './components/AdminPage';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <Router>
      <div className="App">
        <h1 className='app-title'>Car Rental App</h1>
        <Routes>
          <Route path="/" element={
            <div className="auth-container">
              <Login />
              <Register />
            </div>
          } />
          <Route path="/customer" element={<CustomerPage />} />
          <Route path="/admin" element={<AdminPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;