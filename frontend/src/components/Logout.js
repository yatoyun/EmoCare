import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const Logout = () => {
    const history = useNavigate();

    useEffect(() => {
        // Remove the token from local storage
        localStorage.removeItem('token');

        // Redirect to login page
        history('/login');

        console.log('Logged out');
    }, [history]);

    return (
        <div>
            <h2>Logging you out...</h2>
        </div>
    );
};

export default Logout;
