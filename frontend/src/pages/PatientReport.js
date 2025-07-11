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
    <li
      style={{
        borderBottom: "1px solid #dbdbdb",
        paddingBottom: "1rem",
        marginBottom: "1rem",
      }}
    >
      <strong>{keyName}:</strong> {value}
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
    </div>
  );
}

function TaskItem({ taskName, taskData, onAccept, onDecline, onEdit }) {
  return (
    <li
      style={{
        borderBottom: "1px solid #dbdbdb",
        paddingBottom: "1rem",
        marginBottom: "1rem",
      }}
    >
      <strong>{taskName}</strong>
      <p>
        <strong>Action:</strong> {taskData.action}
      </p>
      <p>
        <strong>Purpose:</strong> {taskData.purpose}
      </p>
    </li>
  );
}

export default function PatientReport() {
  const { user_id, report_name } = useParams();
  const [report, setReport] = useState(null);
  const [showStackedSections, setShowStackedSections] = useState(false);
  const navigate = useNavigate();

  const [images, setImages] = useState([]);
  const [currPageIdx, setPageIdx] = useState(1);
  const [currBboxes, setCurrBboxes] = useState([]);
  const [scaledBbox, setScaledBbox] = useState([]);
  const dpi = 150;
  const scale = dpi / 72;

  const nextPage = () => {
    if (currPageIdx + 1 > images.length) {
      setPageIdx(1);
      getBboxAtPage(1);
    } else {
      setPageIdx(currPageIdx + 1);
      getBboxAtPage(currPageIdx + 1);
    }
  };
  const prevPage = () => {
    if (currPageIdx - 1 == 0) {
      setPageIdx(images.length);
      getBboxAtPage(images.length);
    } else {
      setPageIdx(currPageIdx - 1);
      getBboxAtPage(currPageIdx - 1);
    }
  };

  const getBboxAtPage = (pageIdx) => {};
  useEffect(() => {
    const report_url = "/api/get_report/" + user_id + "/" + report_name;
    const image_url = "/api/get_report_images/" + user_id + "/" + report_name;
    fetch(report_url)
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP error! Status: ${res.status}`);
        }
        console.log("HERE");
        return res.json();
      })
      .then((data) => {
        setReport(data);
      })
      .catch((err) => {
        // Error message
        console.log(err);
      });

    fetch(image_url)
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP error! Status: ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        setImages(data);
      })
      .catch((err) => {
        // Error message
        console.log(err);
      });
  }, []); // Empty dependency array = run only once on mount

  useEffect(() => {
    if (report) {
      getBboxAtPage(1);
    }
  }, [report]);
  return (
    <section className="section">
      <div className="container">
        <div className="columns">
          {/* Left Side: Document */}
          <div class="column">
            <div>
              <img
                src={`/api/serve_image/${user_id}/${report_name}/page_${currPageIdx}.png`}
              />
            </div>
            <div class="buttons">
              <button class="button is-link " onClick={prevPage}>
                Previous Page
              </button>
              <button class="button is-primary" onClick={nextPage}>
                Next Page
              </button>
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
                      {Object.entries(report[0]["key_details"]).map(
                        ([key, value], index) => (
                          <ReportItem key={index} keyName={key} value={value} />
                        )
                      )}
                    </ul>
                  )}
                </div>
                <button
                  className="button is-primary is-fullwidth"
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
                <div
                  className="box"
                  style={{ maxHeight: "400px", overflowY: "auto" }}
                >
                  {report && (
                    <ul>
                      {Object.entries(report[1]).map(
                        ([taskName, taskData], index) => (
                          <TaskItem
                            key={index}
                            taskName={taskName}
                            taskData={taskData}
                            onAccept={(name) =>
                              console.log(`Accepted: ${name}`)
                            }
                            onDecline={(name) =>
                              console.log(`Declined: ${name}`)
                            }
                            onEdit={(name) => console.log(`Editing: ${name}`)}
                          />
                        )
                      )}
                    </ul>
                  )}
                </div>
              </div>
            )}
            <button
              class="button is-primary is-fullwidth"
              style={{ marginTop: 15 }}
              onClick={() => navigate("/patient")}
            >
              Go home
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}
