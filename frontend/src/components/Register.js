import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import api, { setAuthToken } from '../api/api';

const Register = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    const [token, setToken] = useState(null);

    const location = useLocation();

    useEffect(() => {
        const urlParams = new URLSearchParams(location.search);
        const tokenFromUrl = urlParams.get('token');
        setToken(tokenFromUrl);
    }, [location]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await api.post('register/', { username, password, token });
            if (response.status === 201) {
                const { access } = response.data;
                localStorage.setItem('token', access);
                setAuthToken(access);
                console.log('Registered in successfully');
                setMessage('Registered in successfully');
            }
        } catch (error) {
            if (error.response && error.response.status === 400) {
                // ユーザー名が既に存在する場合
                console.log(error.response.data);
                setMessage('A user with that username already exists.');
            } else {
                // その他のエラー
                setMessage('Registration failed.');
            }
        }
    };

    return (
        <div>
            <h2>Register</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <button type="submit">Register</button>
            </form>
            {message && <p>{message}</p>}
        </div>
    );
};

export default Register;

