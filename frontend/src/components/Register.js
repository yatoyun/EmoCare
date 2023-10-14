import React, { useState } from 'react';
import api, { setAuthToken } from '../api/api';

const Register = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await api.post('register/', { username, password });
            if (response.status === 200) {
                const { access } = response.data;
                localStorage.setItem('token', access);
                setAuthToken(access);
                console.log('Registered in successfully');
            }
        } catch (error) {
            if (error.response && error.response.status === 400) {
                // ユーザー名が既に存在する場合
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

