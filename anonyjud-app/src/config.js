// Configuration des URLs selon l'environnement
const config = {
  development: {
    API_BASE_URL: 'http://localhost:8000'
  },
  production: {
    API_BASE_URL: process.env.REACT_APP_API_URL || 'https://anonyjud-backend-production.up.railway.app'
  }
};

const environment = process.env.NODE_ENV || 'production';

export default config[environment]; 