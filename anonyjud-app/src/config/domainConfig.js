// Configuration des domaines pour Anonym-IA
// Permet de basculer facilement vers un domaine personnalisé plus tard

const DOMAIN_CONFIG = {
  // Domaine actuel (Railway)
  current: {
    primary: 'https://anonyjud-app-production.up.railway.app',
    name: 'Anonym-IA App',
    isCustomDomain: false
  },
  
  // Domaine personnalisé (anonym-ia.com)
  future: {
    primary: 'https://www.anonym-ia.com',
    name: 'Anonym-IA',
    isCustomDomain: true
  }
};

// Variables d'environnement pour faciliter le changement
const getAppDomain = () => {
  // Si vous définissez REACT_APP_CUSTOM_DOMAIN=true, utilisera le domaine personnalisé
  const useCustomDomain = process.env.REACT_APP_CUSTOM_DOMAIN === 'true';
  
  return useCustomDomain ? DOMAIN_CONFIG.future : DOMAIN_CONFIG.current;
};

// Configuration actuelle
export const APP_DOMAIN = getAppDomain();

// URLs pour les emails et liens
export const EMAIL_URLS = {
  home: `${APP_DOMAIN.primary}`,
  login: `${APP_DOMAIN.primary}/login`,
  pricing: `${APP_DOMAIN.primary}/pricing`,
  dashboard: `${APP_DOMAIN.primary}/dashboard`,
  account: `${APP_DOMAIN.primary}/account`,
  support: 'mailto:contact@anonym-ia.com' // Email de support
};

// Configuration Firebase Auth
export const FIREBASE_AUTH_CONFIG = {
  // URL de redirection après réinitialisation
  passwordResetRedirectUrl: EMAIL_URLS.login,
  
  // Domaine autorisé pour Firebase
  authorizedDomain: APP_DOMAIN.primary.replace('https://', ''),
  
  // Configuration pour les emails
  emailActionSettings: {
    url: EMAIL_URLS.login,
    handleCodeInApp: false
  }
};

// Fonction pour mettre à jour facilement vers un domaine personnalisé
export const switchToCustomDomain = (newDomain) => {
  console.log(`🔄 Migration vers domaine personnalisé : ${newDomain}`);
  console.log('📋 Étapes à suivre :');
  console.log('1. Configurer les DNS OVH');
  console.log('2. Ajouter le domaine dans Railway');
  console.log('3. Ajouter le domaine dans Firebase Console');
  console.log('4. Mettre à jour REACT_APP_CUSTOM_DOMAIN=true');
  console.log('5. Redéployer l\'application');
};

// Domaine actuel configuré
export const CURRENT_DOMAIN = 'www.anonym-ia.com';

export default {
  APP_DOMAIN,
  EMAIL_URLS,
  FIREBASE_AUTH_CONFIG,
  switchToCustomDomain,
  CURRENT_DOMAIN
}; 