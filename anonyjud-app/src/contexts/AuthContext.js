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

  // Plans d'abonnement
  const PLANS = {
    FREE: { name: 'Gratuit', maxProjects: 1, price: 0 },
    STANDARD: { name: 'Standard', maxProjects: 15, price: 19.99 },
    PREMIUM: { name: 'Premium', maxProjects: -1, price: 49.99 } // -1 = illimité
  };

  async function signup(email, password, displayName) {
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
  }

  async function login(email, password) {
    return signInWithEmailAndPassword(auth, email, password);
  }

  async function logout() {
    return signOut(auth);
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
    }
  }

  function canCreateProject() {
    if (!userProfile) return false;
    const plan = PLANS[userProfile.plan];
    return plan.maxProjects === -1 || userProfile.projectsCount < plan.maxProjects;
  }

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (user) => {
      setCurrentUser(user);
      await loadUserProfile(user);
      setLoading(false);
    });

    return unsubscribe;
  }, []);

  const value = {
    currentUser,
    userProfile,
    signup,
    login,
    logout,
    updateUserPlan,
    canCreateProject,
    PLANS
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
} 