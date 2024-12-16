import axios from 'axios';

class AuthService {
  constructor() {
    this.isAuthenticated = false;
    this.user = null;
    this.isInitialized = false;
    
    // Add axios interceptor for handling 401 responses
    axios.interceptors.response.use(
      (response) => response,
      async (error) => {
        if (error.response?.status === 401) {
          this.isAuthenticated = false;
          this.user = null;
        }
        return Promise.reject(error);
      }
    );

    // Configure axios to include credentials
    axios.defaults.withCredentials = true;
  }

  async initialize() {
    if (this.isInitialized) {
      return;
    }

    try {
      await this.getCurrentUser();
    } catch (error) {
      // Silently handle initialization error
      this.isAuthenticated = false;
      this.user = null;
    } finally {
      this.isInitialized = true;
    }
  }

  async login(username, password, mfaCode = null) {
    try {
      const response = await axios.post('/api/auth/login', {
        username,
        password,
        mfa_code: mfaCode
      });
      
      this.isAuthenticated = true;
      this.user = response.data.user;
      
      return response.data;
    } catch (error) {
      console.error(' ❌ Login failed:', error);
      throw error;
    }
  }

  async register(userData) {
    try {
      console.log('🔑 Registering user:', userData);
      const response = await axios.post('/api/auth/register', userData);
      return response.data;
    } catch (error) {
      console.error(' ❌ Registration failed:', error);
      throw error;
    }
  }

  async logout() {
    try {
      await axios.post('/api/auth/logout');
      this.isAuthenticated = false;
      this.user = null;
    } catch (error) {
      console.error(' ❌ Logout failed:', error);
      throw error;
    }
  }

  async getCurrentUser() {
    try {
      const response = await axios.get('/api/auth/me');
      this.user = response.data.user;
      this.isAuthenticated = true;
      return this.user;
    } catch (error) {
      this.isAuthenticated = false;
      this.user = null;
      throw error;
    }
  }
}

export default new AuthService();
