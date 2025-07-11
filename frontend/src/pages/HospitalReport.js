import {
  BrowserRouter as Router,
  Routes,
  Route,
  Lin,
  useNavigate,
  useParams,
} from "react-router-dom";
import React, { useEffect, useState } from "react";

function ReportItem({ keyName, value }) {
  const handleAccept = () => {
    console.log(`Accepted: ${keyName}`);
    // Add logic to update state or send to backend
  };

  const handleDecline = () => {
    console.log(`Declined: ${keyName}`);
  };

  const handleEdit = () => {
    console.log(`Editing: ${keyName}`);
    // You could open a modal or inline input here
  };

  return (
    <li style={{ borderBottom: "1px solid #dbdbdb", paddingBottom: "1rem", marginBottom: "1rem" }}>
      <strong>{keyName}:</strong> {value}
      <div style={{ marginTop: "0.5rem" }}>
        <button className="button is-small is-success" style={{ marginRight: "0.5rem" }} onClick={handleAccept}>
          Accept
        </button>
        <button className="button is-small is-danger" style={{ marginRight: "0.5rem" }} onClick={handleDecline}>
          Decline
        </button>
        <button className="button is-small is-warning" onClick={handleEdit}>
          Edit
        </button>
      </div>
    </li>
  );
}

function PersonalTakeaway({ value }) {
  const handleAccept = () => {
    console.log("Accepted personal takeaway:", value);
    // You can trigger a status update, toast, or backend call here
  };

  const handleDecline = () => {
    console.log("Declined personal takeaway:", value);
  };

  const handleEdit = () => {
    console.log("Editing personal takeaway:", value);
    // You can open a modal or set up an input field to update the value
  };

  return (
    <div style={{ marginBottom: "1.5rem" }}>
      <strong>Personal Takeaway:</strong> {value}

      <div style={{ marginTop: "0.5rem" }}>
        <button
          className="button is-small is-success"
          style={{ marginRight: "0.5rem" }}
          onClick={handleAccept}
        >
          Accept
        </button>
        <button
          className="button is-small is-danger"
          style={{ marginRight: "0.5rem" }}
          onClick={handleDecline}
        >
          Decline
        </button>
        <button className="button is-small is-warning" onClick={handleEdit}>
          Edit
        </button>
      </div>
    </div>
  );
}

function TaskItem({ taskName, taskData, onAccept, onDecline, onEdit }) {
  return (
    <li style={{ borderBottom: "1px solid #dbdbdb", paddingBottom: "1rem", marginBottom: "1rem" }}>
      <strong>{taskName}</strong>
      <p><strong>Action:</strong> {taskData.action}</p>
      <p><strong>Purpose:</strong> {taskData.purpose}</p>

      <div style={{ marginTop: "0.5rem" }}>
        <button
          className="button is-small is-success"
          style={{ marginRight: "0.5rem" }}
          onClick={() => onAccept(taskName)}
        >
          Accept
        </button>

        <button
          className="button is-small is-danger"
          style={{ marginRight: "0.5rem" }}
          onClick={() => onDecline(taskName)}
        >
          Decline
        </button>

        <button
          className="button is-small is-warning"
          onClick={() => onEdit(taskName)}
        >
          Edit
        </button>
      </div>
    </li>
  );
}


export default function HospitalReport() {
  const { user_id, report_name } = useParams();
  const [report, setReport] = useState(null);
  const [showStackedSections, setShowStackedSections] = useState(false);

  useEffect(() => {
    const report_url = "/api/get_report/" + user_id + "/" + report_name;
    fetch(report_url)
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP error! Status: ${res.status}`);
        }
        console.log("HERE");
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
                  <h3 className="title is-5">Key Details</h3>
                  {report && (
                  <ul>
                    {Object.entries(report[0]["key_details"]).map(([key, value], index) => (
                      <ReportItem key={index} keyName={key} value={value} />
                    ))}
                  </ul>
                  )}
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
                <div 
                  className="box mb-4"
                  style={{ maxHeight: "400px", overflowY: "auto" }}
                >
                  {report && (
                  <PersonalTakeaway value={report[0]["personal_takeaways"]} />
                  )}
                </div>
                <div className="box"
                  style={{ maxHeight: "400px", overflowY: "auto" }}

                >
                  {report && (
                  <ul>
                    {Object.entries(report[1]).map(([taskName, taskData], index) => (
                      <TaskItem
                        key={index}
                        taskName={taskName}
                        taskData={taskData}
                        onAccept={(name) => console.log(`Accepted: ${name}`)}
                        onDecline={(name) => console.log(`Declined: ${name}`)}
                        onEdit={(name) => console.log(`Editing: ${name}`)}
                      />
                    ))}
                  </ul>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  );


  
}
