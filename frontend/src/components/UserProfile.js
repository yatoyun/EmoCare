import React, { useState, useEffect } from 'react';
import api, { setAuthToken } from '../api/api';
import { useNavigate, Link } from 'react-router-dom';
import Header from './Header';

import 'bootstrap/dist/css/bootstrap.min.css';

const UserProfile = () => {
    const [profile, setProfile] = useState(null);
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [userId, setUserId] = useState(null);  // For dynamic ID
    const [message, setMessage] = useState('');
    const history = useNavigate();

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                const token = localStorage.getItem('token');
                if (!token) {
                    history('/login');
                    return;
                }
                setAuthToken(token);
                const response = await api.get('userProfile/');
                console.log(response);
                if (response.status === 200) {
                    const data = response.data[0];
                    setProfile(data);
                    setName(data.user.username);
                    setEmail(data.user.email);
                    setUserId(data.user.id);  // Set dynamic ID
                }
            } catch (error) {
                console.log("Error fetching profile data:", error);
                history('/login');
            }
        };
        fetchProfile();
    }, [history]);

    const handleUpdate = async () => {
        try {
            const username = name;
            const updatedProfile = { username, email };
            const response = await api.patch(`users/${userId}/update_user/`, updatedProfile);
            if (response.status === 200) {
                setProfile({ ...profile, ...updatedProfile });
                console.log('Profile updated');
                setMessage('Profile updated');
            }
        } catch (error) {
            console.log('Update failed', error);
            setMessage('Update failed.');
        }
    };

    const handleDelete = async () => {
        try {
            const response = await api.delete(`users/${userId}/delete_user/`);
            console.log(response);
            if (response.status === 200) {
                localStorage.removeItem('token');
                history('/');
                console.log('User deleted');
            }
        } catch (error) {
            console.log('Delete failed', error);
        }
    };

    return (
        <div className="apps">
            <Header />
            <div className="container mt-5">
                <div className="row justify-content-center">
                    <div className="col-md-6">
                        <div className="card">
                            <div className="card-header bg-primary text-white text-center">
                                <h1>User Profile</h1>
                            </div>
                            <div className="card-body">
                                <form onSubmit={(e) => { e.preventDefault(); handleUpdate(); }}>
                                    <div className="form-group">
                                        <label htmlFor="name">Name</label>
                                        <input
                                            type="text"
                                            id="name"
                                            className="form-control"
                                            value={name}
                                            onChange={(e) => setName(e.target.value)}
                                        />
                                    </div>
                                    <div className="form-group">
                                        <label htmlFor="email">Email</label>
                                        <input
                                            type="email"
                                            id="email"
                                            className="form-control"
                                            value={email}
                                            onChange={(e) => setEmail(e.target.value)}
                                        />
                                    </div>
                                    {message && (
                                        <div className={`alert mt-3 ${message === 'Profile updated' ? 'alert-primary' : 'alert-danger'}`}>
                                            {message}
                                        </div>
                                    )}
                                    <button type="submit" className="btn btn-outline-primary">
                                        Update Profile
                                    </button>
                                </form>
                                <div className="mt-3 d-flex justify-content-between">
                                    <Link to="/logout" className="alert-link">
                                        Logout
                                    </Link>
                                    <button onClick={handleDelete} className="btn btn-outline-danger">
                                        Delete User
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default UserProfile;
