import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { updatePassword, updateEmail, reauthenticateWithCredential, EmailAuthProvider, updateProfile } from 'firebase/auth';
import { doc, updateDoc } from 'firebase/firestore';
import { db } from '../firebase/config';

const AccountPage = () => {
  const { currentUser, userProfile, logout, PLANS } = useAuth();
  const [activeTab, setActiveTab] = useState('profile');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });

  // États pour les formulaires
  const [profileForm, setProfileForm] = useState({
    displayName: currentUser?.displayName || '',
    email: currentUser?.email || ''
  });

  const [passwordForm, setPasswordForm] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  });

  const showMessage = (type, text) => {
    setMessage({ type, text });
    setTimeout(() => setMessage({ type: '', text: '' }), 5000);
  };

  const handleProfileUpdate = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      // Mettre à jour le profil Firebase Auth
      if (profileForm.displayName !== currentUser.displayName) {
        await updateProfile(currentUser, { displayName: profileForm.displayName });
      }

      // Mettre à jour le profil Firestore
      const userRef = doc(db, 'users', currentUser.uid);
      await updateDoc(userRef, {
        displayName: profileForm.displayName,
        updatedAt: new Date().toISOString()
      });

      showMessage('success', 'Profil mis à jour avec succès');
    } catch (error) {
      console.error('Erreur mise à jour profil:', error);
      showMessage('error', 'Erreur lors de la mise à jour du profil');
    } finally {
      setLoading(false);
    }
  };

  const handlePasswordChange = async (e) => {
    e.preventDefault();
    setLoading(true);

    if (passwordForm.newPassword !== passwordForm.confirmPassword) {
      showMessage('error', 'Les mots de passe ne correspondent pas');
      setLoading(false);
      return;
    }

    if (passwordForm.newPassword.length < 6) {
      showMessage('error', 'Le mot de passe doit contenir au moins 6 caractères');
      setLoading(false);
      return;
    }

    try {
      // Ré-authentifier l'utilisateur
      const credential = EmailAuthProvider.credential(
        currentUser.email,
        passwordForm.currentPassword
      );
      await reauthenticateWithCredential(currentUser, credential);

      // Changer le mot de passe
      await updatePassword(currentUser, passwordForm.newPassword);

      setPasswordForm({ currentPassword: '', newPassword: '', confirmPassword: '' });
      showMessage('success', 'Mot de passe modifié avec succès');
    } catch (error) {
      console.error('Erreur changement mot de passe:', error);
      if (error.code === 'auth/wrong-password') {
        showMessage('error', 'Mot de passe actuel incorrect');
      } else {
        showMessage('error', 'Erreur lors du changement de mot de passe');
      }
    } finally {
      setLoading(false);
    }
  };

  const tabs = [
    { id: 'profile', name: 'Profil', icon: 'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z' },
    { id: 'security', name: 'Sécurité', icon: 'M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z' },
    { id: 'subscription', name: 'Abonnement', icon: 'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1' },
    { id: 'billing', name: 'Facturation', icon: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z' },
    { id: 'settings', name: 'Paramètres', icon: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z' }
  ];

  const mockInvoices = [
    { id: 'inv_001', date: '2024-01-15', amount: 19.99, status: 'paid', plan: 'Standard' },
    { id: 'inv_002', date: '2023-12-15', amount: 19.99, status: 'paid', plan: 'Standard' },
    { id: 'inv_003', date: '2023-11-15', amount: 19.99, status: 'paid', plan: 'Standard' }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center space-x-4">
            <div className="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center">
              <span className="text-white font-bold text-lg">
                {(currentUser?.displayName || 'U').charAt(0).toUpperCase()}
              </span>
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Mon Compte</h1>
              <p className="text-gray-600">{currentUser?.email}</p>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Navigation latérale */}
          <div className="lg:w-64">
            <nav className="bg-white rounded-lg shadow-sm p-4">
              <ul className="space-y-2">
                {tabs.map((tab) => (
                  <li key={tab.id}>
                    <button
                      onClick={() => setActiveTab(tab.id)}
                      className={`w-full flex items-center px-3 py-2 text-left rounded-lg transition-colors ${
                        activeTab === tab.id
                          ? 'bg-blue-50 text-blue-600 border-r-2 border-blue-600'
                          : 'text-gray-700 hover:bg-gray-50'
                      }`}
                    >
                      <svg className="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={tab.icon} />
                      </svg>
                      {tab.name}
                    </button>
                  </li>
                ))}
              </ul>
            </nav>
          </div>

          {/* Contenu principal */}
          <div className="flex-1">
            {/* Messages */}
            {message.text && (
              <div className={`mb-6 p-4 rounded-lg ${
                message.type === 'success' ? 'bg-green-50 text-green-800 border border-green-200' : 'bg-red-50 text-red-800 border border-red-200'
              }`}>
                {message.text}
              </div>
            )}

            {/* Onglet Profil */}
            {activeTab === 'profile' && (
              <div className="bg-white rounded-lg shadow-sm p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-6">Informations personnelles</h2>
                
                <form onSubmit={handleProfileUpdate} className="space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Nom complet
                      </label>
                      <input
                        type="text"
                        value={profileForm.displayName}
                        onChange={(e) => setProfileForm({...profileForm, displayName: e.target.value})}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Email
                      </label>
                      <input
                        type="email"
                        value={profileForm.email}
                        disabled
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg bg-gray-50 text-gray-500"
                      />
                      <p className="text-xs text-gray-500 mt-1">L'email ne peut pas être modifié</p>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Date d'inscription
                      </label>
                      <input
                        type="text"
                        value={userProfile?.createdAt ? new Date(userProfile.createdAt).toLocaleDateString('fr-FR') : 'N/A'}
                        disabled
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg bg-gray-50 text-gray-500"
                      />
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Plan actuel
                      </label>
                      <input
                        type="text"
                        value={PLANS[userProfile?.plan]?.name || 'Gratuit'}
                        disabled
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg bg-gray-50 text-gray-500"
                      />
                    </div>
                  </div>

                  <div className="flex justify-end">
                    <button
                      type="submit"
                      disabled={loading}
                      className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-medium transition-colors disabled:opacity-50"
                    >
                      {loading ? 'Enregistrement...' : 'Enregistrer les modifications'}
                    </button>
                  </div>
                </form>
              </div>
            )}

            {/* Onglet Sécurité */}
            {activeTab === 'security' && (
              <div className="bg-white rounded-lg shadow-sm p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-6">Sécurité du compte</h2>
                
                <form onSubmit={handlePasswordChange} className="space-y-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Mot de passe actuel
                    </label>
                    <input
                      type="password"
                      value={passwordForm.currentPassword}
                      onChange={(e) => setPasswordForm({...passwordForm, currentPassword: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required
                    />
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Nouveau mot de passe
                      </label>
                      <input
                        type="password"
                        value={passwordForm.newPassword}
                        onChange={(e) => setPasswordForm({...passwordForm, newPassword: e.target.value})}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                        required
                      />
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Confirmer le nouveau mot de passe
                      </label>
                      <input
                        type="password"
                        value={passwordForm.confirmPassword}
                        onChange={(e) => setPasswordForm({...passwordForm, confirmPassword: e.target.value})}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                        required
                      />
                    </div>
                  </div>

                  <div className="bg-blue-50 p-4 rounded-lg">
                    <h3 className="text-sm font-medium text-blue-900 mb-2">Conseils pour un mot de passe sécurisé :</h3>
                    <ul className="text-sm text-blue-700 space-y-1">
                      <li>• Au moins 8 caractères</li>
                      <li>• Mélange de lettres majuscules et minuscules</li>
                      <li>• Au moins un chiffre et un caractère spécial</li>
                      <li>• Évitez les informations personnelles</li>
                    </ul>
                  </div>

                  <div className="flex justify-end">
                    <button
                      type="submit"
                      disabled={loading}
                      className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-medium transition-colors disabled:opacity-50"
                    >
                      {loading ? 'Modification...' : 'Modifier le mot de passe'}
                    </button>
                  </div>
                </form>
              </div>
            )}

            {/* Onglet Abonnement */}
            {activeTab === 'subscription' && (
              <div className="space-y-6">
                {/* Plan actuel */}
                <div className="bg-white rounded-lg shadow-sm p-6">
                  <h2 className="text-xl font-semibold text-gray-900 mb-6">Plan d'abonnement actuel</h2>
                  
                  <div className="flex items-center justify-between p-4 bg-blue-50 rounded-lg border border-blue-200">
                    <div>
                      <h3 className="text-lg font-semibold text-blue-900">
                        Plan {PLANS[userProfile?.plan]?.name || 'Gratuit'}
                      </h3>
                      <p className="text-blue-700">
                        {PLANS[userProfile?.plan]?.maxProjects === -1 
                          ? 'Projets illimités' 
                          : `${PLANS[userProfile?.plan]?.maxProjects} projet(s) maximum`
                        }
                      </p>
                    </div>
                    <div className="text-right">
                      <div className="text-2xl font-bold text-blue-900">
                        {PLANS[userProfile?.plan]?.price === 0 ? 'Gratuit' : `${PLANS[userProfile?.plan]?.price}€/mois`}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Tous les plans */}
                <div className="bg-white rounded-lg shadow-sm p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Changer de plan</h3>
                  
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {Object.entries(PLANS).map(([key, plan]) => (
                      <div key={key} className={`border rounded-lg p-4 ${
                        userProfile?.plan === key ? 'border-blue-500 bg-blue-50' : 'border-gray-200'
                      }`}>
                        <h4 className="text-lg font-semibold text-gray-900 mb-2">{plan.name}</h4>
                        <div className="text-2xl font-bold text-gray-900 mb-4">
                          {plan.price === 0 ? 'Gratuit' : `${plan.price}€/mois`}
                        </div>
                        <ul className="text-sm text-gray-600 space-y-2 mb-4">
                          <li>• {plan.maxProjects === -1 ? 'Projets illimités' : `${plan.maxProjects} projet(s)`}</li>
                          <li>• Anonymisation complète</li>
                          <li>• Support par email</li>
                          {key !== 'FREE' && <li>• Historique des projets</li>}
                          {key === 'PREMIUM' && <li>• Support prioritaire 24/7</li>}
                          {key === 'PREMIUM' && <li>• API d'intégration</li>}
                        </ul>
                        
                        {userProfile?.plan === key ? (
                          <button className="w-full bg-blue-100 text-blue-600 px-4 py-2 rounded-lg font-medium" disabled>
                            Plan actuel
                          </button>
                        ) : (
                          <button className="w-full bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium transition-colors">
                            {plan.price === 0 ? 'Rétrograder' : 'Mettre à niveau'}
                          </button>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* Onglet Facturation */}
            {activeTab === 'billing' && (
              <div className="space-y-6">
                {/* Méthode de paiement */}
                <div className="bg-white rounded-lg shadow-sm p-6">
                  <h2 className="text-xl font-semibold text-gray-900 mb-6">Méthode de paiement</h2>
                  
                  <div className="border border-gray-200 rounded-lg p-4 mb-4">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <div className="w-10 h-6 bg-blue-600 rounded flex items-center justify-center">
                          <span className="text-white text-xs font-bold">VISA</span>
                        </div>
                        <div>
                          <p className="font-medium text-gray-900">•••• •••• •••• 4242</p>
                          <p className="text-sm text-gray-500">Expire 12/2025</p>
                        </div>
                      </div>
                      <button className="text-blue-600 hover:text-blue-700 font-medium">
                        Modifier
                      </button>
                    </div>
                  </div>
                  
                  <button className="bg-gray-100 hover:bg-gray-200 text-gray-800 px-4 py-2 rounded-lg font-medium transition-colors">
                    + Ajouter une méthode de paiement
                  </button>
                </div>

                {/* Historique des factures */}
                <div className="bg-white rounded-lg shadow-sm p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Historique des factures</h3>
                  
                  <div className="overflow-x-auto">
                    <table className="w-full">
                      <thead>
                        <tr className="border-b border-gray-200">
                          <th className="text-left py-3 px-4 font-medium text-gray-900">Facture</th>
                          <th className="text-left py-3 px-4 font-medium text-gray-900">Date</th>
                          <th className="text-left py-3 px-4 font-medium text-gray-900">Plan</th>
                          <th className="text-left py-3 px-4 font-medium text-gray-900">Montant</th>
                          <th className="text-left py-3 px-4 font-medium text-gray-900">Statut</th>
                          <th className="text-left py-3 px-4 font-medium text-gray-900">Actions</th>
                        </tr>
                      </thead>
                      <tbody>
                        {mockInvoices.map((invoice) => (
                          <tr key={invoice.id} className="border-b border-gray-100">
                            <td className="py-3 px-4 text-gray-900">{invoice.id}</td>
                            <td className="py-3 px-4 text-gray-600">
                              {new Date(invoice.date).toLocaleDateString('fr-FR')}
                            </td>
                            <td className="py-3 px-4 text-gray-600">{invoice.plan}</td>
                            <td className="py-3 px-4 text-gray-900 font-medium">{invoice.amount}€</td>
                            <td className="py-3 px-4">
                              <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                                invoice.status === 'paid' 
                                  ? 'bg-green-100 text-green-800' 
                                  : 'bg-red-100 text-red-800'
                              }`}>
                                {invoice.status === 'paid' ? 'Payée' : 'Impayée'}
                              </span>
                            </td>
                            <td className="py-3 px-4">
                              <button className="text-blue-600 hover:text-blue-700 font-medium">
                                Télécharger
                              </button>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            )}

            {/* Onglet Paramètres */}
            {activeTab === 'settings' && (
              <div className="bg-white rounded-lg shadow-sm p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-6">Paramètres du compte</h2>
                
                <div className="space-y-6">
                  {/* Notifications */}
                  <div>
                    <h3 className="text-lg font-medium text-gray-900 mb-4">Notifications</h3>
                    <div className="space-y-3">
                      <label className="flex items-center">
                        <input type="checkbox" className="rounded border-gray-300 text-blue-600 focus:ring-blue-500" defaultChecked />
                        <span className="ml-3 text-gray-700">Notifications par email</span>
                      </label>
                      <label className="flex items-center">
                        <input type="checkbox" className="rounded border-gray-300 text-blue-600 focus:ring-blue-500" defaultChecked />
                        <span className="ml-3 text-gray-700">Mises à jour produit</span>
                      </label>
                      <label className="flex items-center">
                        <input type="checkbox" className="rounded border-gray-300 text-blue-600 focus:ring-blue-500" />
                        <span className="ml-3 text-gray-700">Newsletter marketing</span>
                      </label>
                    </div>
                  </div>

                  {/* Zone de danger */}
                  <div className="border-t pt-6">
                    <h3 className="text-lg font-medium text-red-600 mb-4">Zone de danger</h3>
                    <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                      <h4 className="text-red-800 font-medium mb-2">Supprimer le compte</h4>
                      <p className="text-red-700 text-sm mb-4">
                        Cette action est irréversible. Toutes vos données seront définitivement supprimées.
                      </p>
                      <button className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg font-medium transition-colors">
                        Supprimer mon compte
                      </button>
                    </div>
                  </div>

                  <div className="flex justify-end">
                    <button
                      onClick={logout}
                      className="bg-gray-600 hover:bg-gray-700 text-white px-6 py-2 rounded-lg font-medium transition-colors"
                    >
                      Se déconnecter
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AccountPage; 