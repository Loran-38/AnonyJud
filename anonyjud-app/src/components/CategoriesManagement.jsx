import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { doc, updateDoc } from 'firebase/firestore';
import { db } from '../firebase/config';

const CategoriesManagement = () => {
  const { currentUser, userProfile, setUserProfile } = useAuth();
  const [categories, setCategories] = useState([]);
  const [newCategory, setNewCategory] = useState('');
  const [editingCategory, setEditingCategory] = useState(null);
  const [editingValue, setEditingValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  // Catégories par défaut
  const defaultCategories = [
    "Demandeur", "Défendeur", "Avocat", "Conseil", "Sapiteur", "Tribunal", "Autres"
  ];

  // Charger les catégories depuis le profil utilisateur
  useEffect(() => {
    if (userProfile) {
      const userCategories = userProfile.customCategories || [];
      // Combiner les catégories par défaut avec les catégories personnalisées
      const allCategories = [...defaultCategories, ...userCategories];
      setCategories(allCategories);
    } else {
      setCategories(defaultCategories);
    }
  }, [userProfile]);

  // Fonction pour obtenir les couleurs des catégories
  const getCategoryColor = (index) => {
    const colors = [
      "bg-blue-100 text-blue-900 border border-blue-300",
      "bg-red-100 text-red-900 border border-red-300",
      "bg-purple-100 text-purple-900 border border-purple-300",
      "bg-green-100 text-green-900 border border-green-300",
      "bg-orange-100 text-orange-900 border border-orange-300",
      "bg-gray-100 text-gray-900 border border-gray-400",
      "bg-yellow-100 text-yellow-900 border border-yellow-300",
      "bg-pink-100 text-pink-900 border border-pink-300",
      "bg-indigo-100 text-indigo-900 border border-indigo-300",
      "bg-teal-100 text-teal-900 border border-teal-300"
    ];
    return colors[index % colors.length];
  };

  // Sauvegarder les catégories personnalisées dans Firebase
  const saveCategories = async (newCustomCategories) => {
    if (!currentUser) return;

    setIsLoading(true);
    setError('');

    try {
      const userRef = doc(db, 'users', currentUser.uid);
      await updateDoc(userRef, {
        customCategories: newCustomCategories
      });

      // Mettre à jour le profil local
      setUserProfile(prev => ({
        ...prev,
        customCategories: newCustomCategories
      }));

    } catch (err) {
      setError('Erreur lors de la sauvegarde des catégories.');
      console.error('Erreur:', err);
    } finally {
      setIsLoading(false);
    }
  };

  // Ajouter une nouvelle catégorie
  const addCategory = async () => {
    if (!newCategory.trim()) {
      setError('Veuillez entrer un nom de catégorie.');
      return;
    }

    if (categories.includes(newCategory.trim())) {
      setError('Cette catégorie existe déjà.');
      return;
    }

    const currentCustomCategories = userProfile?.customCategories || [];
    const updatedCustomCategories = [...currentCustomCategories, newCategory.trim()];
    
    await saveCategories(updatedCustomCategories);
    setNewCategory('');
  };

  // Modifier une catégorie personnalisée
  const editCategory = async (oldCategory, newCategoryName) => {
    if (!newCategoryName.trim()) {
      setError('Veuillez entrer un nom de catégorie.');
      return;
    }

    if (categories.includes(newCategoryName.trim()) && newCategoryName.trim() !== oldCategory) {
      setError('Cette catégorie existe déjà.');
      return;
    }

    const currentCustomCategories = userProfile?.customCategories || [];
    const updatedCustomCategories = currentCustomCategories.map(cat => 
      cat === oldCategory ? newCategoryName.trim() : cat
    );
    
    await saveCategories(updatedCustomCategories);
    setEditingCategory(null);
    setEditingValue('');
  };

  // Supprimer une catégorie personnalisée
  const deleteCategory = async (categoryToDelete) => {
    if (defaultCategories.includes(categoryToDelete)) {
      setError('Impossible de supprimer une catégorie par défaut.');
      return;
    }

    if (window.confirm(`Êtes-vous sûr de vouloir supprimer la catégorie "${categoryToDelete}" ?`)) {
      const currentCustomCategories = userProfile?.customCategories || [];
      const updatedCustomCategories = currentCustomCategories.filter(cat => cat !== categoryToDelete);
      
      await saveCategories(updatedCustomCategories);
    }
  };

  // Démarrer l'édition d'une catégorie
  const startEditing = (category) => {
    if (defaultCategories.includes(category)) {
      setError('Impossible de modifier une catégorie par défaut.');
      return;
    }
    setEditingCategory(category);
    setEditingValue(category);
  };

  return (
    <div className="h-full bg-gradient-to-br from-gray-50 to-purple-50">
      <div className="p-6 border-b bg-gray-50">
        <h2 className="text-xl font-semibold text-gray-900 flex items-center">
          <svg className="w-6 h-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
          </svg>
          Gestion des catégories
        </h2>
        <p className="text-gray-600 mt-1">
          Personnalisez les catégories de tiers pour vos projets
        </p>
      </div>

      <div className="p-6 overflow-y-auto" style={{ height: 'calc(100% - 120px)' }}>
        {/* Formulaire d'ajout */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
            <svg className="w-5 h-5 mr-2 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            Ajouter une nouvelle catégorie
          </h3>
          
          <div className="flex gap-3">
            <input
              type="text"
              value={newCategory}
              onChange={(e) => setNewCategory(e.target.value)}
              placeholder="Nom de la nouvelle catégorie..."
              className="flex-1 border-2 border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
              onKeyPress={(e) => e.key === 'Enter' && addCategory()}
            />
            <button
              onClick={addCategory}
              disabled={isLoading || !newCategory.trim()}
              className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-lg font-medium transition-colors duration-150 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
            >
              {isLoading ? (
                <svg className="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              ) : (
                'Ajouter'
              )}
            </button>
          </div>
        </div>

        {/* Liste des catégories */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <div className="p-6 border-b border-gray-200 bg-gradient-to-r from-purple-50 to-indigo-50">
            <h3 className="text-lg font-semibold text-gray-800 flex items-center">
              <svg className="w-5 h-5 mr-2 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
              </svg>
              Toutes les catégories ({categories.length})
            </h3>
          </div>

          <div className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {categories.map((category, index) => {
                const isDefault = defaultCategories.includes(category);
                const isCustom = !isDefault;

                return (
                  <div
                    key={category}
                    className={`p-4 rounded-lg border-2 transition-all duration-200 ${getCategoryColor(index)}`}
                  >
                    {editingCategory === category ? (
                      <div className="space-y-2">
                        <input
                          type="text"
                          value={editingValue}
                          onChange={(e) => setEditingValue(e.target.value)}
                          className="w-full px-2 py-1 border border-gray-300 rounded text-sm"
                          onKeyPress={(e) => {
                            if (e.key === 'Enter') editCategory(category, editingValue);
                            if (e.key === 'Escape') {
                              setEditingCategory(null);
                              setEditingValue('');
                            }
                          }}
                          autoFocus
                        />
                        <div className="flex gap-1">
                          <button
                            onClick={() => editCategory(category, editingValue)}
                            className="px-2 py-1 bg-green-500 text-white text-xs rounded hover:bg-green-600"
                          >
                            ✓
                          </button>
                          <button
                            onClick={() => {
                              setEditingCategory(null);
                              setEditingValue('');
                            }}
                            className="px-2 py-1 bg-gray-500 text-white text-xs rounded hover:bg-gray-600"
                          >
                            ✕
                          </button>
                        </div>
                      </div>
                    ) : (
                      <div className="flex items-center justify-between">
                        <div className="flex-1">
                          <span className="font-medium">{category}</span>
                          {isDefault && (
                            <span className="ml-2 text-xs bg-gray-200 text-gray-600 px-2 py-1 rounded">
                              Par défaut
                            </span>
                          )}
                        </div>
                        {isCustom && (
                          <div className="flex gap-1 ml-2">
                            <button
                              onClick={() => startEditing(category)}
                              className="p-1 text-gray-500 hover:text-blue-600 transition-colors"
                              title="Modifier"
                            >
                              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                              </svg>
                            </button>
                            <button
                              onClick={() => deleteCategory(category)}
                              className="p-1 text-gray-500 hover:text-red-600 transition-colors"
                              title="Supprimer"
                            >
                              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                              </svg>
                            </button>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>

            {categories.length === defaultCategories.length && (
              <div className="text-center py-8 text-gray-500">
                <svg className="w-12 h-12 mx-auto mb-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                </svg>
                <p>Aucune catégorie personnalisée.</p>
                <p className="text-sm">Ajoutez vos propres catégories ci-dessus.</p>
              </div>
            )}
          </div>
        </div>

        {/* Messages d'erreur */}
        {error && (
          <div className="mt-4 p-4 bg-red-50 text-red-700 rounded-lg border border-red-200 flex items-start">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 mt-0.5 flex-shrink-0" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            <span>{error}</span>
          </div>
        )}

        {/* Informations */}
        <div className="mt-6 p-4 bg-blue-50 text-blue-700 rounded-lg border border-blue-200">
          <h4 className="font-medium mb-2 flex items-center">
            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Informations
          </h4>
          <ul className="text-sm space-y-1">
            <li>• Les catégories par défaut ne peuvent pas être modifiées ou supprimées</li>
            <li>• Vos catégories personnalisées sont sauvegardées dans votre compte</li>
            <li>• Ces catégories seront disponibles dans tous vos projets</li>
            <li>• Vous pouvez modifier ou supprimer vos catégories personnalisées à tout moment</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default CategoriesManagement; 