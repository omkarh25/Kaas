import axios from 'axios';

const API_URL = 'http://localhost:8000';

export async function login(username: string, password: string) {
  try {
    const response = await axios.post(`${API_URL}/token`, new URLSearchParams({
      username,
      password,
    }), {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    const { access_token } = response.data;
    localStorage.setItem('token', access_token);
    return true;
  } catch (error) {
    console.error('Login error:', error);
    return false;
  }
}

export function logout() {
  localStorage.removeItem('token');
}

export function getToken() {
  return localStorage.getItem('token');
}

export function isAuthenticated() {
  return !!getToken();
}

export const axiosAuth = axios.create({
  baseURL: API_URL,
});

axiosAuth.interceptors.request.use(
  (config) => {
    const token = getToken();
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);