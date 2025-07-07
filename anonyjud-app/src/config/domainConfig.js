// Configuration des domaines pour AnonyJud
// Permet de basculer facilement vers un domaine personnalisé plus tard

const DOMAIN_CONFIG = {
  // Domaine actuel (Railway)
  current: {
    primary: 'https://anonyjud-app-production.up.railway.app',
    name: 'AnonyJud App',
    isCustomDomain: false
  },
  
  // Domaine futur (à configurer quand vous l'achèterez)
  future: {
    primary: 'https://anonyjud.com', // Exemple de domaine futur
    name: 'AnonyJud',
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
  support: 'mailto:support@anonyjud.com' // Email de support
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
  console.log('1. Acheter et configurer le domaine');
  console.log('2. Ajouter le domaine dans Firebase Console');
  console.log('3. Mettre à jour REACT_APP_CUSTOM_DOMAIN=true');
  console.log('4. Redéployer l\'application');
};

// Domaines suggérés pour l'avenir
export const SUGGESTED_DOMAINS = [
  'anonyjud.com',
  'anonyjud.fr',
  'anony-jud.com',
  'anonymisation-juridique.com'
];

export default {
  APP_DOMAIN,
  EMAIL_URLS,
  FIREBASE_AUTH_CONFIG,
  switchToCustomDomain,
  SUGGESTED_DOMAINS
}; 