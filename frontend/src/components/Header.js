import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';

const Header = () => {
    const [showMenu, setShowMenu] = useState(false);

    return (
        <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
            <Link className="navbar-brand" to="/UserProfile">EmoCare</Link>
            <button className="navbar-toggler" type="button" onClick={() => setShowMenu(!showMenu)}>
                <span className="navbar-toggler-icon"></span>
            </button>

            <div className={`collapse navbar-collapse ${showMenu ? 'show' : ''}`}>
                <ul className="navbar-nav ml-auto">
                    <li className="nav-item">
                        <Link className="nav-link" to="/UserProfile">UserProfile</Link>
                    </li>
                </ul>
            </div>
        </nav>
    );
};

export default Header;
