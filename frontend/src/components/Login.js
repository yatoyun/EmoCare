import React, { useState } from 'react';
import api, { setAuthToken } from '../api/api';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = async () => {
        try {
            const response = await api.post('login/', { username, password });
            if (response.status === 200) {
                const { access } = response.data;
        localStorage.setItem('token', access);
        setAuthToken(access);
                console.log('Logged in successfully');
            }
        } catch (error) {
            // Handle error
            console.log('Login failed', error);
        }
    };

    return (
        <div>
            <h2>Login</h2>
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
            <button onClick={handleSubmit}>Login</button>
        </div>
    );
};

export default Login;