import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { logout } from '../redux/auth/authActions';

const Logout = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();


    useEffect(() => {
        try {
            dispatch(logout());
            setTimeout(() => {
                navigate('/login');
            }, 100); 
        } catch (error) {
            console.log('Logout failed', error);
        }
    }, [dispatch, navigate]);

    return (
        <div>
            <h2>Logging you out...</h2>
        </div>
    );
};

export default Logout;
