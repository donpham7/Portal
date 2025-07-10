import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Home from "./pages/Home";
import About from "./pages/About";

function App() {
  return (
    <Router>
      {/* <nav class="panel">
        <p class="panel-heading">Repositories</p>
        <div class="panel-block">
          <p class="control has-icons-left">
            <input class="input" type="text" placeholder="Search" />
            <span class="icon is-left">
              <i class="fas fa-search" aria-hidden="true"></i>
            </span>
          </p>
        </div>
        <p class="panel-tabs">
          <a class="is-active">All</a>
          <a>Public</a>
          <a>Private</a>
          <a>Sources</a>
          <a>Forks</a>
        </p>
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
          About
        </Link>
        <div class="panel-block">
          <button class="button is-link is-outlined is-fullwidth">
            Reset all filters
          </button>
        </div>
      </nav> */}
      <div className="content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
