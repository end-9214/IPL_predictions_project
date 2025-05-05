import React, { useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import "./Navbar.css";

function Navbar() {
  const [menuOpen, setMenuOpen] = useState(false);
  const location = useLocation();
  
  // Close mobile menu when route changes
  useEffect(() => {
    setMenuOpen(false);
  }, [location.pathname]);
  
  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
  };
  
  // Function to check if a link is active
  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <nav className="navbar">
      <Link to="/" className="navbar-logo">
        <span>🏏</span> IPL Predictions
      </Link>
      
      <button 
        className="mobile-menu-button" 
        onClick={toggleMenu}
        aria-label="Toggle navigation menu"
      >
        {menuOpen ? "✕" : "☰"}
      </button>
      
      <ul className={`navbar-links ${menuOpen ? 'open' : ''}`}>
        <li>
          <Link 
            to="/" 
            className={`navbar-link ${isActive('/') ? 'active' : ''}`}
          >
            Upload Matches
          </Link>
        </li>
        <li>
          <Link 
            to="/current-predictions" 
            className={`navbar-link ${isActive('/current-predictions') ? 'active' : ''}`}
          >
            Current Predictions
          </Link>
        </li>
        <li>
          <Link 
            to="/manual-date-predictions" 
            className={`navbar-link ${isActive('/manual-date-predictions') ? 'active' : ''}`}
          >
            Date Predictions
          </Link>
        </li>
        <li>
          <Link 
            to="/train-model" 
            className={`navbar-link ${isActive('/train-model') ? 'active' : ''}`}
          >
            Train Model
          </Link>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;