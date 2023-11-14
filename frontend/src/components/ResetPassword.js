import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/api';
import PasswordStrengthMeter from './PasswordStrengthMeter';
import './ResetPassword.css'; // CSSファイルのインポート

const ResetPassword = () => {
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [oneTimePassword, setOneTimePassword] = useState('');
    const [strengthMessage, setStrengthMessage] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const requestOneTimePassword = async () => {
        try {
            await api.post('/tempCode/');
            setError('');
        } catch (error) {
            setError('Failed to send one-time password. Please try again.');
        }
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!password) {
            setError('Username and Password cannot be empty');
            return;
        }
        if (password !== confirmPassword) {
            setError('Passwords do not match');
            return;
        }
        if (strengthMessage) {
            setError(strengthMessage);
            return;
        }
        if (!oneTimePassword) {
            setError('One Time Password cannot be empty');
            return;
        }

        try {
            await api.post('/resetPassword/', { password, oneTimePassword });
            setError('');
            navigate('/login');
        } catch (error) {
            setError('Failed to reset password. Please request a new one-time password.');
            setOneTimePassword('');
        }
    };

    return (
        <div className="reset-password-container">
            <form onSubmit={handleSubmit} className="reset-password-form">
                <input 
                    type="password" 
                    value={password} 
                    onChange={(e) => setPassword(e.target.value)} 
                    placeholder="New Password" 
                />
                <input 
                    type="password" 
                    value={confirmPassword} 
                    onChange={(e) => setConfirmPassword(e.target.value)} 
                    placeholder="Confirm New Password" 
                />
                <PasswordStrengthMeter password={password} setStrengthMessage={setStrengthMessage} />
                <input 
                    type="text" 
                    value={oneTimePassword} 
                    onChange={(e) => setOneTimePassword(e.target.value)} 
                    placeholder="One Time Password" 
                />
                {error && <div className="error-message">{error}</div>}
                <button type="submit" className="submit-button">Reset Password</button>
                <button type="button" onClick={requestOneTimePassword} className="otp-button">Send One Time Password</button>
            </form>
        </div>
    );
};

export default ResetPassword;
