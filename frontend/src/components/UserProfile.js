import React, { useState, useEffect } from 'react';
import api from '../api/api';
import { refreshToken } from '../api/auth';
import { useNavigate, Link } from 'react-router-dom';
import Header from './Header';
import { Container, Row, Col, Form, Button, Card, Alert, Modal } from 'react-bootstrap';
import './UserProfile.css';

const UserProfile = () => {
    const [profile, setProfile] = useState(null);
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [userId, setUserId] = useState(null);
    const [message, setMessage] = useState('');
    const [showModal, setShowModal] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                const response = await api.get('/userProfile/');
                if (response.status === 200) {
                    const data = response.data[0];
                    setProfile(data);
                    setName(data.user.username);
                    setEmail(data.user.email);
                    setUserId(data.user.id);
                }
            } catch (error) {
                if (error.response && error.response.status === 401) {
                    const refreshed = await refreshToken();
                    if (refreshed) {
                        fetchProfile(); // リフレッシュ成功後、プロファイル情報を再度取得
                    } else {
                        setTimeout(() => {
                            navigate('/login');
                        }, 100);
                    }
                } else {
                    console.log('Error fetching profile data:', error);
                    setTimeout(() => {
                        navigate('/login');
                    }, 100);
                }
            }
        };
        fetchProfile();
    }, [navigate]);

    const handleUpdate = async () => {
        try {
            const updatedProfile = { username: name, email };
            const response = await api.patch(`/users/${userId}/update_user/`, updatedProfile);
            if (response.status === 200) {
                setProfile({ ...profile, ...updatedProfile });
                setMessage('Profile updated');
            }
        } catch (error) {
            console.log('Update failed', error);
            setMessage('Update failed.');
        }
    };
    const confirmDelete = async () => {
        setShowModal(true);
    };

    const handleDelete = async () => {
        // setShowModal(false);
        try {
            const response = await api.delete(`users/${userId}/delete_user/`);
            console.log(response);
            if (response.status === 200) {
                navigate('/logout');
            }
        } catch (error) {
            console.log('Delete failed', error);
        }
    };
    
    const handleResetPassword = async () => {
        try {
            navigate('/resetPassword');
        } catch (error) {
            console.log('Reset password failed', error);
            setMessage('Reset password failed');
        }
    }

    return (
        <div>
            <Header />
        <Container className="user-profile mt-5">
            <Row className='justify-content-center'>
                <Col md={6} className="offset">
                    <Card>
                    <div className='profile-login-form-main'>
                        <h1 className="card-title text-center">User Profile</h1>
                    </div>
                        <Card.Body>
                            <Form>
                                <Form.Group className="mb-3 black" controlId="formBasicEmail">
                                    <Form.Label>Username</Form.Label>
                                    <Form.Control type="text" placeholder="Enter username" value={name} onChange={(e) => setName(e.target.value)} />
                                </Form.Group>
                                <Form.Group className="mb-3" controlId="formBasicPassword">
                                    <Form.Label>Email address</Form.Label>
                                    <Form.Control type="email" placeholder="Enter email" value={email} onChange={(e) => setEmail(e.target.value)} />
                                </Form.Group>
                                {message && <Alert variant="info">{message}</Alert>}
                                <Button variant="outline-primary" onClick={handleUpdate}>Update</Button>
                                <Button variant="outline-dark" onClick={handleResetPassword}>Reset Password</Button>
                                <div className='mt-6'>
                                    <Link to="/logout" className="btn btn-secondary">Logout</Link>
                                    <Button variant="danger" onClick={confirmDelete}>Delete</Button>
                                </div>
                            </Form>
                        </Card.Body>
                    </Card>
                </Col>
            </Row>

            <Modal show={showModal} onHide={() => setShowModal(false)}>
                <Modal.Header closeButton>
                    <Modal.Title>Confirm Delete</Modal.Title>
                </Modal.Header>
                <Modal.Body>Are you sure you want to delete your account?</Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={() => setShowModal(false)}>Close</Button>
                    <Button variant="danger" onClick={handleDelete}>Delete</Button>
                </Modal.Footer>
            </Modal>
        </Container>
        </div>
    );
}

export default UserProfile;
