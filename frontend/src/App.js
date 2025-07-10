import logo from "./logo.svg";
import "./App.css";
import React, { useEffect, useState } from "react";

function App() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetch("/api/hello")
      .then((res) => res.json())
      .then((data) => setMessage(data.message));
  }, []);

  return (
    <div>
      <h1>{message || "Loading..."}</h1>
      <button class="button is-white">White</button>
      <button class="button is-light">Light</button>
      <button class="button is-dark">Dark</button>
      <button class="button is-black">Black</button>
      <button class="button is-text">Text</button>
      <button class="button is-ghost">Ghost</button>
    </div>
  );
}

export default App;
