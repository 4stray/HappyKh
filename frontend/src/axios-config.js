import axios from 'axios';
import store from './store';

const HOST = 'http://127.0.0.1:8000';

export const axiosInstanceAuth = axios.create({
  baseURL: HOST,
  headers: { Authorization: `Token ${store.getters.getToken}` },
});

export const axiosInstance = axios.create({
  baseURL: HOST,
});