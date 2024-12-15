import axios from 'axios';

class AuthService {
  constructor() {
    this.isAuthenticated = false;
    this.user = null;
    this.isInitialized = false;
    this.publicPaths = ['/register', '/login', '/auth/register', '/auth/login', '/auth/refresh'];
    this.isRefreshing = false;
    this.failedQueue = [];
    
    // Add axios interceptor for handling 401 responses
    axios.interceptors.response.use(
      (response) => response,
      async (error) => {
        if (error.response?.status === 401) {
          // Don't try to refresh token for public paths
          const isPublicPath = this.publicPaths.some(path => 
            error.config.url.includes(path)
          );
          
          if (isPublicPath) {
            return Promise.reject(error);
          }
          
          // Try to refresh token if available
          try {
            // If already refreshing, queue the request
            if (this.isRefreshing) {
              return new Promise((resolve, reject) => {
                this.failedQueue.push({ resolve, reject });
              })
                .then(token => {
                  error.config.headers['Authorization'] = 'Bearer ' + token;
                  return axios(error.config);
                })
                .catch(err => {
                  return Promise.reject(err);
                });
            }

            this.isRefreshing = true;
            const response = await this.refreshToken();
            this.isRefreshing = false;

            // Process queued requests
            this.failedQueue.forEach(prom => {
              prom.resolve(response.access_token);
            });
            this.failedQueue = [];

            // Retry the original request
            error.config.headers['Authorization'] = 'Bearer ' + response.access_token;
            return axios(error.config);
          } catch (refreshError) {
            this.isAuthenticated = false;
            this.user = null;
            this.isRefreshing = false;
            
            // Reject all queued requests
            this.failedQueue.forEach(prom => {
              prom.reject(refreshError);
            });
            this.failedQueue = [];

            throw error;
          }
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
      // Only try to get current user if we're not on a public path
      const currentPath = window.location.pathname;
      const isPublicPath = this.publicPaths.some(path => 
        currentPath.includes(path)
      );
      
      if (!isPublicPath) {
        await this.getCurrentUser();
      }
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
      const errorMessage = error.response?.data?.detail || ' ❌ Login failed';
      console.error(errorMessage);
      // Rethrow with the error message from the backend
      throw new Error(errorMessage);
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
      // The cookie will be automatically included in the request
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

  async refreshToken() {
    try {
      const response = await axios.post('/api/auth/refresh');
      return response.data;
    } catch (error) {
      console.error(' ❌ Token refresh failed:', error);
      throw error;
    }
  }
}

export default new AuthService();
