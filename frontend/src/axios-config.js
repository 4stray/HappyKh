import axios from 'axios';
import store from './store';

export const axiosInstance = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  headers: {'Authorization': `Token ${store.getters.getToken}`},
});