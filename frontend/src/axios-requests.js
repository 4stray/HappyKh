/* eslint-disable no-param-reassign */
import axios from 'axios';

const HOST = 'http://127.0.0.1:8000';

export const axiosInstance = axios.create({
  baseURL: HOST,
});

axiosInstance.interceptors.request.use(
  (config) => {
    const token = window.$cookies.get('token');
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  error => Promise.reject(error),
);

export function getUserData(id) {
  return axiosInstance.get(`/api/users/${id}`);
}

export function getPlaces(params) {
  return axiosInstance.get('/api/places/', params);
}

export function getPlaceData(id) {
  return axiosInstance.get(`/api/places/${id}`);
}

export function getPlaceRating(id) {
  return axiosInstance.get(`/api/places/rating/${id}`);
}

export function getConfirmation(email, token) {
  return axiosInstance.get(`/api/users/activate/${email}/${token}/`);
}
