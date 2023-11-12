// ResetPassword.js の例
import React, { useState } from 'react';
import api from '../api/api';  // APIリクエスト用のインスタンス
import PasswordStrengthMeter from './PasswordStrengthMeter';

const ResetPassword = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();
        // APIを呼び出してパスワードをリセット
        // ...
    };

    return (
        <form onSubmit={handleSubmit}>
            <input 
                type="text" 
                value={username} 
                onChange={(e) => setUsername(e.target.value)} 
                placeholder="Username or Email" 
            />
            <input 
                type="password" 
                value={password} 
                onChange={(e) => setPassword(e.target.value)} 
                placeholder="New Password" 
            />
            <PasswordStrengthMeter password={password} />
            <button type="submit">Reset Password</button>
        </form>
    );
};

export default ResetPassword;
