import React, { useState, useEffect } from 'react';
import api, { setAuthToken } from '../api/api';
import { useNavigate, Link } from 'react-router-dom';
import Header from './Header';
import { Container, Row, Col, Card, Form, Button, Alert } from 'react-bootstrap';

const UserProfile = () => {
    const [profile, setProfile] = useState(null);
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [userId, setUserId] = useState(null);
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
        <div>
            <Header />
            <Container className="mt-5">
                <Row className="justify-content-md-center">
                    <Col xs={12} md={6}>
                        <Card>
                            <Card.Body>
                            <Card.Title className="text-center mb-4">User Profile</Card.Title>
                                <Form onSubmit={(e) => { e.preventDefault(); handleUpdate(); }}>
                                    <Form.Group>
                                        <Form.Label>Name</Form.Label>
                                        <Form.Control
                                            type="text"
                                                                                        value={name}
                                            onChange={(e) => setName(e.target.value)}
                                        />
                                    </Form.Group>
                                    <Form.Group>
                                        <Form.Label>Email</Form.Label>
                                        <Form.Control
                                            type="email"
                                                                                        value={email}
                                            onChange={(e) => setEmail(e.target.value)}
                                        />
                                    </Form.Group>
                                    {message && (
                                        <Alert variant={message === 'Profile updated' ? 'primary' : 'danger'} className="mt-3">
                                            {message}
                                        </Alert>
                                    )}
                                    <Button variant="outline-primary" type="submit">
                                        Update Profile
                                    </Button>
                                </Form>
                                <div className="mt-3 d-flex justify-content-between">
                                    <Link to="/logout" className="alert-link">
                                        Logout
                                    </Link>
                                    <Button variant="outline-danger" onClick={handleDelete}>
                                        Delete User
                                    </Button>
                                </div>
                            </Card.Body>
                        </Card>
                    </Col>
                </Row>
            </Container>
        </div>
    );
};

export default UserProfile;
