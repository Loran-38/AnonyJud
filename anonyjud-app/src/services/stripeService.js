// Service pour l'intégration future de Stripe
// Ce fichier prépare l'infrastructure pour les paiements

// Configuration des plans avec leurs prix Stripe (à configurer plus tard)
export const STRIPE_PLANS = {
  FREE: {
    priceId: null, // Pas de prix Stripe pour le plan gratuit
    name: 'Gratuit',
    maxProjects: 1,
    price: 0
  },
  STANDARD: {
    priceId: 'price_XXXXXXXX', // À remplacer par l'ID réel de Stripe
    name: 'Standard',
    maxProjects: 15,
    price: 19.99
  },
  PREMIUM: {
    priceId: 'price_XXXXXXXX', // À remplacer par l'ID réel de Stripe
    name: 'Premium',
    maxProjects: -1, // Illimité
    price: 49.99
  }
};

// Fonction pour créer une session de checkout Stripe
export const createCheckoutSession = async (planId, userId) => {
  try {
    // Cette fonction sera implémentée quand Stripe sera configuré
    // Elle devra appeler votre backend pour créer une session Stripe
    
    const response = await fetch(`${process.env.REACT_APP_API_URL}/create-checkout-session`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        planId,
        userId,
        successUrl: `${window.location.origin}/dashboard?payment=success`,
        cancelUrl: `${window.location.origin}/pricing?payment=cancelled`
      })
    });

    if (!response.ok) {
      throw new Error('Erreur lors de la création de la session de paiement');
    }

    const { sessionId } = await response.json();
    
    // Rediriger vers Stripe Checkout
    // const stripe = await loadStripe(process.env.REACT_APP_STRIPE_PUBLISHABLE_KEY);
    // await stripe.redirectToCheckout({ sessionId });
    
    return sessionId;
  } catch (error) {
    console.error('Erreur Stripe:', error);
    throw error;
  }
};

// Fonction pour gérer le portail client Stripe (gestion des abonnements)
export const createCustomerPortalSession = async (customerId) => {
  try {
    // Cette fonction sera implémentée quand Stripe sera configuré
    const response = await fetch(`${process.env.REACT_APP_API_URL}/create-portal-session`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        customerId,
        returnUrl: `${window.location.origin}/dashboard`
      })
    });

    if (!response.ok) {
      throw new Error('Erreur lors de la création de la session portail');
    }

    const { url } = await response.json();
    window.location.href = url;
  } catch (error) {
    console.error('Erreur portail Stripe:', error);
    throw error;
  }
};

// Fonction pour vérifier le statut d'un paiement
export const checkPaymentStatus = async (sessionId) => {
  try {
    const response = await fetch(`${process.env.REACT_APP_API_URL}/check-payment-status/${sessionId}`);
    
    if (!response.ok) {
      throw new Error('Erreur lors de la vérification du paiement');
    }

    return await response.json();
  } catch (error) {
    console.error('Erreur vérification paiement:', error);
    throw error;
  }
};

// Fonctions utilitaires pour l'affichage des prix
export const formatPrice = (price) => {
  return new Intl.NumberFormat('fr-FR', {
    style: 'currency',
    currency: 'EUR'
  }).format(price);
};

export const getPlanByPriceId = (priceId) => {
  return Object.values(STRIPE_PLANS).find(plan => plan.priceId === priceId);
};

// Instructions pour l'implémentation future de Stripe :
/*
1. Installer Stripe : npm install @stripe/stripe-js
2. Configurer les variables d'environnement :
   - REACT_APP_STRIPE_PUBLISHABLE_KEY
3. Créer les produits et prix dans le dashboard Stripe
4. Implémenter les endpoints backend :
   - POST /create-checkout-session
   - POST /create-portal-session
   - GET /check-payment-status/:sessionId
   - Webhook pour gérer les événements Stripe
5. Mettre à jour les priceId dans STRIPE_PLANS
6. Décommenter et adapter le code loadStripe
*/ 