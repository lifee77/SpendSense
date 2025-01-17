import React, { useEffect, useState } from "react";
import axios from "../api";
import Loader from "./Loader";

const Dashboard = () => {
  const [summary, setSummary] = useState({});
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get("/dashboard");
        setSummary(response.data);
      } catch (err) {
        setError("Failed to load dashboard data.");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="dashboard">
      <h2>Expense Dashboard</h2>
      {error && <p className="error">{error}</p>}
      {loading && <Loader />}
      {!loading && Object.keys(summary).length > 0 ? (
        <ul>
          {Object.keys(summary).map((category) => (
            <li key={category}>
              {category}: ${summary[category].toFixed(2)}
            </li>
          ))}
        </ul>
      ) : (
        !loading && <p>No expenses recorded yet.</p>
      )}
    </div>
  );
};

export default Dashboard;
