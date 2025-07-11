import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import React, { useEffect, useState } from "react";

export default function PatientDashboard() {
  const [reports, setReports] = useState([]);
  const [tasks, setTasks] = useState([]);
  var patientId = 1;
  useEffect(() => {
    // Replace with your URL
    const reports_url = "/api/get_reports/" + patientId;
    const tasks_url = "/api/get_tasks/" + patientId;
    fetch(reports_url)
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP error! Status: ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        console.log("reports", data);
        setReports(data);
      })
      .catch((err) => {
        // Error message
        console.log(err);
      });

    fetch(tasks_url)
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP error! Status: ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        setTasks(data);
      })
      .catch((err) => {
        // Error message
        console.log(err);
      });
  }, []); // Empty dependency array = run only once on mount
  return (
    <div class="columns">
      <div className="column section">
        <nav className="panel">
          <p className="panel-heading">Reports</p>

          <div className="panel-block">
            <p className="control has-icons-left">
              <span className="icon is-left">
                <i className="fas fa-search" aria-hidden="true"></i>
              </span>
            </p>
          </div>
          {reports.map((report, index) => (
            <Link
              to={`report/${patientId}/${report.filename}`}
              className="panel-block"
            >
              <span className="panel-icon">
                <i className="fas fa-home" aria-hidden="true"></i>
              </span>
              {report.data[0].filename}
            </Link>
          ))}
        </nav>
      </div>
      <div className="column section">
        <nav className="panel">
          <p className="panel-heading">Tasks</p>

          <div className="panel-block">
            <p className="control has-icons-left">
              <span className="icon is-left">
                <i className="fas fa-search" aria-hidden="true"></i>
              </span>
            </p>
          </div>
          {tasks.map((task, index) => (
            <a class="panel-block">
              <span className="panel-icon">
                <i className="fas fa-home" aria-hidden="true"></i>
              </span>
              {task}
            </a>
          ))}
        </nav>
      </div>
    </div>
  );
}
