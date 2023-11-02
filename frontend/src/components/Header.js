import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Navbar, Nav, Container } from 'react-bootstrap';

const Header = () => {
    const [expanded, setExpanded] = useState(false);

    const toggleMenu = () => {
        setExpanded(!expanded);
    };

    return (
        <Navbar expand="lg" bg="dark" variant="dark" expanded={expanded}>
            <Container>
                <Navbar.Brand as={Link} to="/UserProfile">EmoCare</Navbar.Brand>
                <Navbar.Toggle aria-controls="responsive-navbar-nav" onClick={toggleMenu} />
                <Navbar.Collapse id="responsive-navbar-nav">
                    <Nav className="ml-auto">
                        <Nav.Link as={Link} to="/UserProfile" onClick={() => setExpanded(false)}>
                            UserProfile
                        </Nav.Link>
                        <Nav.Link as={Link} to="/statistics" onClick={() => setExpanded(false)}>
                            Statistics
                        </Nav.Link>
                    </Nav>
                </Navbar.Collapse>
            </Container>
        </Navbar>
    );
};

export default Header;
