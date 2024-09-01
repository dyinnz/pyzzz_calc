import axios from "axios";

const instance = axios.create({
  baseURL: "http://127.0.0.1:5704",
  headers: {},
});

export default instance;
