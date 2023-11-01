import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import api, { setAuthToken } from '../api/api';
import { useNavigate, Link } from 'react-router-dom';

import 'bootstrap/dist/css/bootstrap.min.css';



const Register = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    const [token, setToken] = useState(null);
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
        try {
            const response = await api.post('register/', { username, password, token });
            if (response.status === 201) {
                const { access } = response.data;
                localStorage.setItem('token', access);
                setAuthToken(access);
                console.log('Registered in successfully');
                setMessage('Registered in successfully');
                history('/userProfile');
            }
        } catch (error) {
            if (error.response && error.response.status === 400) {
                // ユーザー名が既に存在する場合
                console.log(error.response.data);
                setMessage('A user with that username already exists.');
            } else {
                // その他のエラー
                console.log('Registration failed', error);
                setMessage('Registration failed.');
            }
        }
    };

    return (
        <div className="container mt-5">
            <div className="row justify-content-center">
                <div className="col-md-6">
                    <div className="card">
                        <div className="card-body">
                            <h2 className="card-title text-center">Register</h2>
                            <form onSubmit={handleSubmit}>
                                <div className="form-group">
                                    <input
                                        type="text"
                                        className="form-control"
                                        placeholder="Username"
                                        value={username}
                                        onChange={(e) => setUsername(e.target.value)}
                                    />
                                </div>
                                <div className="form-group">
                                    <input
                                        type="password"
                                        className="form-control"
                                        placeholder="Password"
                                        value={password}
                                        onChange={(e) => setPassword(e.target.value)}
                                    />
                                </div>
                                <button type="submit" className="btn btn-primary btn-block">
                                    Register
                                </button>
                            </form>
                            {message && <div className="alert alert-danger mt-3">{message}</div>}
                            <p className="text-center mt-3">
                                Already have an account?{" "}
                                <Link to="/login" className="alert-link">
                                    Login here
                                </Link>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Register;

