import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { loginUser } from '../redux/auth/authActions';
import { useNavigate } from 'react-router-dom';
import './Login.css';

import 'bootstrap/dist/css/bootstrap.min.css';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    const dispatch = useDispatch();
    const history = useNavigate();
    const error = useSelector(state => state.auth.error);

    const handleSubmit = () => {
        if (!username || !password) {
            setMessage('Username and Password cannot be empty');
            return;
        }
        dispatch(loginUser(username, password));
    };

    // React Routerのナビゲーションを更新するための効果
    const user = useSelector(state => state.auth.user);

    useEffect(() => {
        if (user) {
            history('/userProfile');
        } else if (error) {
            setMessage(error);
        }
    }, [user, error, history]);

    return (
        <div className="container mt-5">
            <div className="row justify-content-center">
                <div className="col-md-6">
                    <div className="card">

                        <div className='login-form-main'>
                            <h1 className="card-title text-center">Login</h1>
                        </div>
                        <div className="card-body">
                            <form className="login-form" onSubmit={(e) => { e.preventDefault(); handleSubmit(); }}>
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
                                <button type="submit" className="btn btn-primary w-100 mt-4">
                                    submit
                                </button>
                            </form>
                            {message && <div className="alert alert-danger mt-3">{message}</div>}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Login;
