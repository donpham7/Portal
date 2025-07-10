import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Home from "./pages/Home";
import Patient from "./pages/Patient";

function App() {
  return (
    <Router>
      <div className="content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/patient" element={<Patient />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
