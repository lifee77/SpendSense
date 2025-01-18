import React from "react";
import ReceiptUploader from "./components/ReceiptUploader";
import Dashboard from "./components/Dashboard";
import "./App.css";

const App = () => {
  return (
    <div className="App">
      <header>
        <h1>Receipt Classifier</h1>
      </header>
      <main>
        <ReceiptUploader />
        <Dashboard />
      </main>
      <footer>
        <p>&copy; 2025 SpendSense</p>
      </footer>
    </div>
  );
};

export default App;