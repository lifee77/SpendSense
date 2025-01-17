import React, { useEffect, useState } from "react";
import axios from "../api";

const Dashboard = () => {
  const [summary, setSummary] = useState({});
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get("/dashboard");
        setSummary(response.data);
      } catch (err) {
        setError("Failed to load dashboard data.");
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      <h2>Expense Dashboard</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {Object.keys(summary).length > 0 ? (
        <ul>
          {Object.keys(summary).map((category) => (
            <li key={category}>
              {category}: ${summary[category].toFixed(2)}
            </li>
          ))}
        </ul>
      ) : (
        <p>No expenses recorded yet.</p>
      )}
    </div>
  );
};

export default Dashboard;
