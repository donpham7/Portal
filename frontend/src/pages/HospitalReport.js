import {
  BrowserRouter as Router,
  Routes,
  Route,
  Lin,
  useNavigate,
  useParams,
} from "react-router-dom";
import React, { useEffect, useState } from "react";

export default function HospitalReport() {
  const { user_id, report_name } = useParams();
  const [report, setReport] = useState(null);
  console.log();
  useEffect(() => {
    const report_url = "/api/get_report/" + user_id + "/" + report_name;
    fetch(report_url)
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP error! Status: ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        console.log(data);
        setReport(data);
      })
      .catch((err) => {
        // Error message
        console.log(err);
      });
  }, []); // Empty dependency array = run only once on mount
  return (
    <section className="section">
      <div className="container">
        <div className="columns">
          {/* Left Side: Document */}
          <div className="column section">
            <div className="box">
              <h2 className="title">Document</h2>
              <p>This is your document content. It remains visible at all times.</p>
              <p>User ID: {user_id}</p>
              <p>Report ID: {report_name}</p>


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
