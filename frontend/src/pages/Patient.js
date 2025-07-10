import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Patient from "./Patient";
import React, { useEffect, useState } from "react";

export default function About() {
  const [reports, setReports] = useState(null);

  useEffect(() => {
    // Replace with your URL
    const url = "/api/hello";
    fetch(url)
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP error! Status: ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        console.log(data);
        setReports(data.message);
      })
      .catch((err) => {
        // Error message
        console.log(err);
      });
  }, []); // Empty dependency array = run only once on mount
  return (
    <div className="section">
      <nav className="panel">
        <p className="panel-heading">Navigation</p>

        <div className="panel-block">
          <p className="control has-icons-left">
            <input className="input" type="text" placeholder="Search" />
            <span className="icon is-left">
              <i className="fas fa-search" aria-hidden="true"></i>
            </span>
          </p>
        </div>

        <Link to="/" className="panel-block">
          <span className="panel-icon">
            <i className="fas fa-home" aria-hidden="true"></i>
          </span>
          Home
        </Link>

        <Link to="/about" className="panel-block">
          <span className="panel-icon">
            <i className="fas fa-info-circle" aria-hidden="true"></i>
          </span>
          {reports}
        </Link>

        <label className="panel-block">
          <input type="checkbox" />
          remember me
        </label>

        <div className="panel-block">
          <button className="button is-link is-outlined is-fullwidth">
            Reset all filters
          </button>
        </div>
      </nav>

      <div className="content">
        <Routes>
          <Route path="/about" element={<About />} />
        </Routes>
      </div>
    </div>
  );
}
