import React, { useState } from "react";
import axios from "../api";

const ReceiptUploader = () => {
  const [file, setFile] = useState(null);
  const [classification, setClassification] = useState(null);
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please upload a receipt image.");
      return;
    }

    const formData = new FormData();
    formData.append("receipt_image", file);

    try {
      const response = await axios.post("/classify", formData);
      setClassification(response.data.summary); // Assuming `summary` is returned
      setError("");
    } catch (err) {
      setError("Failed to classify receipt. Please try again.");
    }
  };

  return (
    <div>
      <h2>Upload Receipt</h2>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {classification && (
        <div>
          <h3>Classification Result</h3>
          <ul>
            {Object.keys(classification).map((category) => (
              <li key={category}>
                {category}: ${classification[category].toFixed(2)}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default ReceiptUploader;
