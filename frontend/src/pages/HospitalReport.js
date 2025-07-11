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
    <div class="columns">
      <div class="column">
        <p>User ID: {user_id}</p>
      </div>
      <div class="column">
        <p>Report ID: {report_name}</p>
      </div>
    </div>
  );
}
