import React, { createContext, useContext, useState, useEffect } from 'react';
import { 
  createUserWithEmailAndPassword, 
  signInWithEmailAndPassword, 
  signOut, 
  onAuthStateChanged,
  updateProfile
} from 'firebase/auth';
import { doc, setDoc, getDoc } from 'firebase/firestore';
import { auth, db } from '../firebase/config';

const AuthContext = createContext();

export function useAuth() {
  return useContext(AuthContext);
}

export function AuthProvider({ children }) {
  const [currentUser, setCurrentUser] = useState(null);
  const [userProfile, setUserProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Plans d'abonnement
  const PLANS = {
    FREE: { name: 'Gratuit', maxProjects: 1, price: 0 },
    STANDARD: { name: 'Standard', maxProjects: 15, price: 19.99 },
    PREMIUM: { name: 'Premium', maxProjects: -1, price: 49.99 } // -1 = illimité
  };

  async function signup(email, password, displayName) {
    try {
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      const user = userCredential.user;
      
      // Mettre à jour le profil avec le nom d'affichage
      await updateProfile(user, { displayName });
      
      // Créer le profil utilisateur dans Firestore
      await setDoc(doc(db, 'users', user.uid), {
        email: user.email,
        displayName: displayName,
        plan: 'FREE',
        createdAt: new Date().toISOString(),
        projectsCount: 0
      });
      
      return userCredential;
    } catch (error) {
      console.error('Erreur lors de l\'inscription:', error);
      throw error;
    }
  }

  async function login(email, password) {
    try {
      return await signInWithEmailAndPassword(auth, email, password);
    } catch (error) {
      console.error('Erreur lors de la connexion:', error);
      throw error;
    }
  }

  async function logout() {
    try {
      return await signOut(auth);
    } catch (error) {
      console.error('Erreur lors de la déconnexion:', error);
      throw error;
    }
  }

  async function loadUserProfile(user) {
    if (!user) {
      setUserProfile(null);
      return;
    }

    try {
      const docRef = doc(db, 'users', user.uid);
      const docSnap = await getDoc(docRef);
      
      if (docSnap.exists()) {
        setUserProfile(docSnap.data());
      } else {
        // Créer le profil s'il n'existe pas
        const profile = {
          email: user.email,
          displayName: user.displayName || 'Utilisateur',
          plan: 'FREE',
          createdAt: new Date().toISOString(),
          projectsCount: 0
        };
        await setDoc(docRef, profile);
        setUserProfile(profile);
      }
    } catch (error) {
      console.error('Erreur lors du chargement du profil:', error);
      setError(error.message);
    }
  }

  async function updateUserPlan(plan) {
    if (!currentUser) return;
    
    try {
      const docRef = doc(db, 'users', currentUser.uid);
      await setDoc(docRef, { plan }, { merge: true });
      setUserProfile(prev => ({ ...prev, plan }));
    } catch (error) {
      console.error('Erreur lors de la mise à jour du plan:', error);
      setError(error.message);
    }
  }

  function canCreateProject() {
    if (!userProfile) return false;
    const plan = PLANS[userProfile.plan];
    return plan.maxProjects === -1 || userProfile.projectsCount < plan.maxProjects;
  }

  useEffect(() => {
    console.log('AuthProvider: Initialisation...');
    
    // Timeout de sécurité
    const timeout = setTimeout(() => {
      console.log('AuthProvider: Timeout atteint, arrêt du loading');
      setLoading(false);
      setError('Timeout de connexion Firebase');
    }, 10000); // 10 secondes

    const unsubscribe = onAuthStateChanged(auth, async (user) => {
      try {
        console.log('AuthProvider: État d\'authentification changé:', user ? 'connecté' : 'déconnecté');
        clearTimeout(timeout);
        setCurrentUser(user);
        await loadUserProfile(user);
        setLoading(false);
      } catch (error) {
        console.error('AuthProvider: Erreur lors du changement d\'état:', error);
        clearTimeout(timeout);
        setError(error.message);
        setLoading(false);
      }
    }, (error) => {
      console.error('AuthProvider: Erreur onAuthStateChanged:', error);
      clearTimeout(timeout);
      setError(error.message);
      setLoading(false);
    });

    return () => {
      clearTimeout(timeout);
      unsubscribe();
    };
  }, []);

  const value = {
    currentUser,
    userProfile,
    signup,
    login,
    logout,
    updateUserPlan,
    canCreateProject,
    PLANS,
    error
  };

  // Afficher l'erreur si Firebase ne fonctionne pas
  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-red-50">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-red-600 mb-4">Erreur de configuration Firebase</h1>
          <p className="text-red-500 mb-4">{error}</p>
          <p className="text-sm text-gray-600">Vérifiez les variables d'environnement Firebase</p>
        </div>
      </div>
    );
  }

  return (
    <AuthContext.Provider value={value}>
      {!loading ? children : (
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Chargement...</p>
          </div>
        </div>
      )}
    </AuthContext.Provider>
  );
} 