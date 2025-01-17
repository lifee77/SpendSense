import React, { useState } from "react";
import axios from "../api";

const ReceiptUploader = () => {
  const [file, setFile] = useState(null);
  const [classification, setClassification] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setError("");
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please upload a receipt image.");
      return;
    }

    const formData = new FormData();
    formData.append("receipt_image", file);

    try {
      setLoading(true);
      setError("");
      const response = await axios.post("/classify", formData);

      if (response.data.error) {
        setError(response.data.error);
      } else {
        setClassification(response.data.summary); // Assuming `summary` is returned.
      }
    } catch (err) {
      setError("Failed to classify receipt. Please try again.");
      console.error("Error during upload:", err.response || err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="receipt-uploader">
      <h2>Upload Your Receipt</h2>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Uploading..." : "Upload"}
      </button>
      {error && <p className="error">{error}</p>}
      {loading && <p>Processing your receipt...</p>}
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
