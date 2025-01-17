import React from "react";
import ReceiptUploader from "./components/ReceiptUploader";
import Dashboard from "./components/Dashboard";
import "./App.css";

const App = () => {
  return (
    <div className="App">
      <h1>Receipt Classifier</h1>
      <ReceiptUploader />
      <Dashboard />
    </div>
  );
};

export default App;
