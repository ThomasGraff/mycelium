import axios from 'axios';

class AuthService {
  constructor() {
    this.isAuthenticated = false;
    this.user = null;
  }

  async login() {
    // Redirect to backend login endpoint
    window.location.href = '/api/auth/login';
  }

  async logout() {
    try {
      await axios.get('/api/auth/logout');
      this.isAuthenticated = false;
      this.user = null;
    } catch (error) {
      console.error('❌ Logout failed:', error);
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
