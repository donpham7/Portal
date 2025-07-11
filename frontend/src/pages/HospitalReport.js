import {
  BrowserRouter as Router,
  Routes,
  Route,
  Lin,
  useNavigate,
} from "react-router-dom";
import React, { useEffect, useState } from "react";

// http://localhost:3000/hospital/report/4/UMNwriteup.pdf



export default function HospitalReport() {
  const [showStackedSections, setShowStackedSections] = useState(false);

  
  return (
    <section className="section">
      <div className="container">
        <div className="columns">
          {/* Left Side: Document */}
          <div className="column section">
            <div className="box">
              <h2 className="title">Document</h2>
              <p>This is your document content. It remains visible at all times.</p>
            </div>
          </div>

          {/* Right Side */}
          <div className="column section">
            {!showStackedSections ? (
              // Scrollable List View
              <div>
                <div
                  className="box"
                  style={{ maxHeight: "600px", overflowY: "auto" }}
                >
                  <h3 className="title is-5">Related Data</h3>
                  <ul>
                    {Array.from({ length: 100 }, (_, i) => (
                      <li key={i}>Item {i + 1}</li>
                    ))}
                  </ul>
                </div>
                <button
                  className="button is-primary"
                  onClick={() => setShowStackedSections(true)}
                >
                  Next
                </button>
              </div>
            ) : (
              // Stacked Sections View
              <div>
                <div className="box mb-4">
                  <p>Top Stacked Section</p>
                </div>
                <div className="box">
                  <p>Bottom Stacked Section</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  );

}
