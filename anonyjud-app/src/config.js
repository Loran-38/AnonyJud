// Configuration des URLs selon l'environnement
const config = {
  development: {
    API_BASE_URL: 'http://localhost:8000'
  },
  production: {
    API_BASE_URL: process.env.REACT_APP_API_URL || 'https://anonyjud-backend-production.up.railway.app'
  }
};

// Forcer l'utilisation de l'URL Railway en production
const isLocalhost = window.location.hostname === 'localhost';
const environment = isLocalhost ? 'development' : 'production';

const currentConfig = config[environment];

export const API_BASE_URL = currentConfig.API_BASE_URL;
export default currentConfig; 