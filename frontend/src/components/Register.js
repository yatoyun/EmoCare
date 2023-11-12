import React, { useState, useEffect } from 'react';
import api from '../api/api';
import { useLocation, useNavigate, Link } from 'react-router-dom';
import PasswordStrengthMeter from './PasswordStrengthMeter';

import 'bootstrap/dist/css/bootstrap.min.css';
import './Register.css'; // CSSファイルのインポート

const Register = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    const [token, setToken] = useState(null);
    const [strengthMessage, setStrengthMessage] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const history = useNavigate();


    const location = useLocation();

    useEffect(() => {
        const urlParams = new URLSearchParams(location.search);
        const tokenFromUrl = urlParams.get('token');
        setToken(tokenFromUrl);
    }, [location]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!username || !password) {
            setMessage('Username and Password cannot be empty');
            return;
        }
        if (username.length < 4) {
            setMessage('Username must be at least 4 characters long');
            return;
        }
        if (password !== confirmPassword) {
            setMessage('Passwords do not match');
            return;
        }
        if (strengthMessage) {
            setMessage(strengthMessage);
            return;
        }
        try {
            await api.post('register/', { username, password, token });
            console.log('Registered successfully');

            // 登録成功後、自動ログイン
            const loginResponse = await api.post('api/token/', { username, password });
            if (loginResponse.data && loginResponse.data.access) {
                // ログイン成功時の処理
                console.log('Logged in successfully');

                history('/userProfile');
            }
        } catch (error) {
            if (error.response && error.response.status === 400) {
                console.log(error.response.data);
                setMessage('A user with that username already exists.');
            } else {
                // その他のエラー
                console.log('Registration failed', error);
                setMessage('Registration failed. Try again from LINE chat.');
            }
        }
    };

    return (
        <div className="container mt-5">
            <div className="row col justify-content-center">
                <div className="col-md-6">
                    <div className="card">
                        <div className='register-form-main'>
                            <h1 className="text-center">Register</h1>
                        </div>
                        <div className="card-body">
                            <form onSubmit={handleSubmit} className="register-form">
                                <div className="mb-3">
                                    <label htmlFor="username" className="form-label">Username</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        id="username"
                                        value={username}
                                        onChange={(e) => setUsername(e.target.value)}
                                    />
                                </div>
                                <div className="mb-3">
                                    <label htmlFor="password" className="form-label">Password</label>
                                    <input
                                        type="password"
                                        className="form-control"
                                        id="password"
                                        value={password}
                                        onChange={(e) => setPassword(e.target.value)}
                                    />
                                </div>
                                <div className="mb-3">
                                    <label htmlFor="confirmPassword" className="form-label">Confirm Password</label>
                                    <input
                                        type="password"
                                        className="form-control"
                                        id="confirmPassword"
                                        value={confirmPassword}
                                        onChange={(e) => setConfirmPassword(e.target.value)}
                                    />
                                </div>
                                <PasswordStrengthMeter password={password} setStrengthMessage={setStrengthMessage} />
                                <button type="submit" className="btn btn-primary w-100 mt-4">submit</button>
                            </form>
                            {message && <div className="alert alert-danger mt-3">{message}</div>}
                            <p className="text-center mt-4">
                                Already have an account? <Link to="/login" className="alert-link">Login here</Link>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Register;

