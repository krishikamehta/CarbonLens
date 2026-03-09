import API from "./api";

// calculate footprint
export const calculateFootprint = (data) =>
  API.post("/calculate", data);

// get user history
export const getHistory = (email) =>
  API.get(`/users/${email}/footprints`);

// get analytics
export const getAnalytics = (email) =>
  API.get(`/users/${email}/analytics`);

// get recommendations
export const getRecommendations = (email) =>
  API.get(`/users/${email}/recommendations`);