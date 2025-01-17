import axios from "axios";

const instance = axios.create({
  baseURL: "http://localhost:5000", // Update with your deployed backend URL
  headers: {
    "Content-Type": "multipart/form-data",
  },
});

export default instance;
