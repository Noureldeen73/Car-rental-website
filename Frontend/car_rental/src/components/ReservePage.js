import React, {useState, useEffect} from 'react';
import {useParams, useNavigate, useLocation} from 'react-router-dom';
import '../styles/ReservePage.css';
import carImage from '../car.png';

function ReservePage() {
    const [car, setCar] = useState(null);
    const [error, setError] = useState(null);
    const [existingReservations, setExistingReservations] = useState([]);
    const [dates, setDates] = useState({
        pickupDate: '',
        returnDate: ''
    });
    const [paymentMethod, setPaymentMethod] = useState('cash');
    const [totalPrice, setTotalPrice] = useState(0);
    const {carId} = useParams();
    const navigate = useNavigate();
    const location = useLocation();
    const customerId = location.state?.customerId;
    const userId = location.state?.userId;

    console.log('userID in reservation page: ', userId);

    useEffect(() => {
        if (!customerId) {
            navigate('/');
            return;
        }

        const fetchCarDetails = async () => {
            try {
                const queryString = new URLSearchParams({
                    plate_number: carId
                }).toString();

                const response = await fetch(`http://127.0.0.1:8000/Car/get_car_by_plate_num/?${queryString}`);
                if (response.ok) {
                    const data = await response.json();
                    setCar(data);

                } else {
                    const errorData = await response.json();
                    setError(errorData.detail || 'Failed to fetch car details');
                }
            } catch (error) {
                setError('Error connecting to server');
                console.error('Error fetching car details:', error);
            }
        };

        fetchCarDetails();
    }, [carId, customerId, navigate]);

    const handleDateChange = (e) => {
        const {name, value} = e.target;
        setDates(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleLogout = () => {
        navigate(`/`);
    };


    useEffect(() => {
        if (car && dates.pickupDate && dates.returnDate) {
            const start = new Date(dates.pickupDate);
            const end = new Date(dates.returnDate);
            const days = Math.ceil((end - start) / (1000 * 60 * 60 * 24));
            if (days > 0) {
                setTotalPrice(days * car.price);
            } else {
                setTotalPrice(0);
            }
        }
    }, [dates, car]);

    const handleSubmit = async () => {
        if (!customerId) {
            alert('Customer information is missing');
            return;
        }

        try {
            const reservationData = {
                // reservation_date: "2024-12-30",
                pickup_date: dates.pickupDate,
                return_date: dates.returnDate,
                plate_number: car.plate_number,
                user_id: parseInt(userId),
                payment_method: paymentMethod,
                total_price: totalPrice
            };
            console.log(reservationData);
            console.log('Sending reservation data:', reservationData);
            const queryString = new URLSearchParams(reservationData).toString();
            const response = await fetch('http://127.0.0.1:8000/Car/make_reservation/?' + queryString, {
                method: 'POST',
            });
            if (response.ok) {
                alert('Reservation successful!');
                navigate('/customer', {state: {userId}});
            } else {
                const errorData = await response.json();
                alert(`Reservation failed: ${errorData.detail}`);
            }
        } catch (error) {
            alert('Error making reservation: ' + error.message);
        }
    };

    const handleBack = () => {
        navigate('/customer');
    };

    if (error) {
        return (
            <div className="error-container">
                <p>{error}</p>
                <button onClick={handleBack}>Back to Cars</button>
            </div>
        );
    }

    if (!car) {
        return <div className="loading">Loading...</div>;
    }

    return (
        <div className="reserve-page">
            <div className="car-details-card">
                <button
                    className="logout-button"
                    onClick={() => handleLogout()}
                >
                    Logout
                </button>
                <div className="car-image-container">
                    <img src={`/${car.img_path}`} alt={car.model} className="car-detail-image"/>
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
                            <span className="detail-value">{car.city}</span>
                        </div>
                        <div className="detail-item">
                            <span className="detail-label">Plate Number:</span>
                            <span className="detail-value">{car.plate_number}</span>
                        </div>
                        <div className="detail-item">
                            <span className="detail-label">Price per Day:</span>
                            <span className="detail-value">${car.price}</span>
                        </div>
                    </div>

                    <div className="reservation-section">

                        <div className="date-inputs">
                            <div className="date-input-group">
                                <label htmlFor="pickupDate">Pickup Date:</label>
                                <input
                                    type="date"
                                    id="pickupDate"
                                    name="pickupDate"
                                    value={dates.pickupDate}
                                    onChange={handleDateChange}
                                    min={new Date().toISOString().split('T')[0]}
                                    required
                                />
                            </div>
                            <div className="date-input-group">
                                <label htmlFor="returnDate">Return Date:</label>
                                <input
                                    type="date"
                                    id="returnDate"
                                    name="returnDate"
                                    value={dates.returnDate}
                                    onChange={handleDateChange}
                                    min={dates.pickupDate || new Date().toISOString().split('T')[0]}
                                    required
                                />
                            </div>
                        </div>

                        <div className="payment-method">
                            <label htmlFor="paymentMethod">Payment Method:</label>
                            <select
                                id="paymentMethod"
                                value={paymentMethod}
                                onChange={(e) => setPaymentMethod(e.target.value)}
                                required
                            >
                                <option value="cash">Cash</option>
                                <option value="credit">Credit</option>
                            </select>
                        </div>

                        {totalPrice > 0 && (
                            <div className="total-price">
                                <span className="price-label">Total Price:</span>
                                <span className="price-value">${totalPrice}</span>
                            </div>
                        )}

                        <div className="button-group">
                            <button className="back-button" onClick={handleBack}>Back</button>
                            <button
                                className="reserve-button"
                                onClick={handleSubmit}
                                disabled={!dates.pickupDate || !dates.returnDate || totalPrice <= 0}
                            >
                                Confirm Reservation
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default ReservePage; 