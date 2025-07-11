import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import React, { useEffect, useState } from "react";

export default function HospitalDashboard() {
  const [patients, setPatients] = useState([]);
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [uploadedFile, setFile] = useState(null);

  const OnPatientClick = (value) => {
    setSelectedPatient(value);
    console.log("Clicked User", value);
    console.log(selectedPatient);
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    console.log("Selected file:", e.target.files[0]);
  };

  const handleUpload = () => {
    if (!uploadedFile) {
      alert("No file selected!");
      return;
    }

    const formData = new FormData();
    formData.append("file", uploadedFile);
    formData.append("user_id", selectedPatient.user_id);

    fetch("/api/upload", {
      method: "POST",
      body: formData,
    })
      .then((res) => {
        if (!res.ok) throw new Error("Upload failed");
        return res;
      })
      .then((data) => {
        console.log("Success:", data);
      })
      .catch((err) => {
        console.error("Upload error:", err);
      });
  };

  useEffect(() => {
    const reports_url = "/api/get_patients/";
    fetch(reports_url)
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP error! Status: ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        console.log(data);
        setPatients(data);
      })
      .catch((err) => {
        // Error message
        console.log(err);
      });
  }, []); // Empty dependency array = run only once on mount
  return (
    <div class="columns">
      <div className="column section">
        <nav class="panel">
          <p class="panel-heading">Patients</p>
          <div class="panel-block">
            <p class="control has-icons-left">
              <input class="input" type="text" placeholder="Search" />
              <span class="icon is-left">
                <i class="fas fa-search" aria-hidden="true"></i>
              </span>
            </p>
          </div>
          {patients.map((patient, index) => (
            <a class="panel-block" onClick={() => OnPatientClick(patient)}>
              <span className="panel-icon">
                <i className="fas fa-home" aria-hidden="true"></i>
              </span>
              {patient.patient_info.name}
            </a>
          ))}
        </nav>
      </div>
      <div className="column section">
        <nav className="panel">
          <p className="panel-heading">Patient Info</p>

          <div class="block" style={{ padding: 15 }}>
            <h3>
              {selectedPatient?.patient_info?.name || "Select patient for more"}
            </h3>
            {selectedPatient?.patient_info?.name && (
              <div>
                <p>{selectedPatient?.patient_info?.notes}</p>
                <ul>
                  <li>Age: {selectedPatient?.patient_info?.age}</li>
                  <li>
                    Medical ID: {selectedPatient?.patient_info?.medical_id}
                  </li>
                  {selectedPatient?.patient_info?.conditions.length === 0 ? (
                    <div>
                      <li>Conditions: None</li>
                    </div>
                  ) : (
                    <div>
                      <div>
                        <li>
                          Conditions:
                          <div class="content">
                            <ul>
                              {selectedPatient?.patient_info?.conditions.map(
                                (cond, index) => (
                                  <li>{cond}</li>
                                )
                              )}
                            </ul>
                          </div>
                        </li>
                      </div>
                    </div>
                  )}
                </ul>
                <div class="file has-name is-fullwidth">
                  <label class="file-label">
                    <input
                      class="file-input"
                      type="file"
                      name="resume"
                      onChange={handleFileChange}
                    />
                    <span class="file-cta">
                      <span class="file-icon">
                        <i class="fas fa-upload"></i>
                      </span>
                      <span class="file-label"> Choose a file… </span>
                    </span>
                    <span class="file-name">
                      {uploadedFile?.name || "No file selected"}
                    </span>
                  </label>
                </div>
                <button
                  class="button is-fullwidth is-primary"
                  onClick={handleUpload}
                >
                  Upload new file
                </button>
              </div>
            )}
          </div>
        </nav>
      </div>
    </div>
  );
}
