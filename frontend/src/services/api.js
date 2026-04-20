import axios from "axios";

const API = axios.create({
  baseURL: "http://0.0.0.0:9000"
});

export const runPlugins = (data) => API.post("/run", data);
export const getStatus = (jobId) => API.get(`/status/${jobId}`);
export const getResults = (jobId) => API.get(`/results/${jobId}`);
export const getPluginsList = (data) => API.post("/plugin-list", data);
export const getTimeline = (data) => API.post("/timeline", data);
