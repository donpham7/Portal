import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Home from "./pages/Home";
import Patient from "./pages/Patient";
import Hospital from "./pages/Hospital";

function App() {
  return (
    <Router>
      <div className="content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/patient" element={<Patient />} />
          <Route path="/hospital" element={<Hospital />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
