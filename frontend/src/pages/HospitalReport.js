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
    <div class="columns">
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
      <div class="column">
        <p>Report ID: {report_name}</p>
      </div>
    </div>
  );
}
