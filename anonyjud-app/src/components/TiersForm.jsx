import React, { useState, useEffect } from "react";
import { useAuth } from '../contexts/AuthContext';

/**
 * Formulaire pour ajouter et gérer les tiers d'un projet avec champs personnalisés illimités.
 * UX moderne avec animations et interface intuitive.
 */
function TiersForm({ projectId, tiers = [], updateProject, projects, setProjects }) {
  const { userProfile } = useAuth();
  
  // Catégories par défaut
  const defaultCategories = [
    "Demandeur", "Défendeur", "Avocat", "Conseil", "Sapiteur", "Tribunal", "Autres"
  ];
  
  // Combiner les catégories par défaut avec les catégories personnalisées
  const categories = [
    ...defaultCategories,
    ...(userProfile?.customCategories || [])
  ];

  const [form, setForm] = useState({
    nom: "",
    prenom: "",
    adresse_numero: "",
    adresse_voie: "",
    adresse_code_postal: "",
    adresse_ville: "",
    telephone: "",
    portable: "",
    email: "",
    societe: "",
    categorie: "Demandeur",
    customFields: [] // Champs personnalisés illimités
  });

  const [isAddingCustomField, setIsAddingCustomField] = useState(false);
  const [newCustomField, setNewCustomField] = useState({ label: "", value: "" });
  
  // État pour gérer l'affichage du formulaire d'ajout
  const [showAddForm, setShowAddForm] = useState(false);
  
  // État pour gérer quels tiers sont développés dans l'accordéon
  const [expandedTiers, setExpandedTiers] = useState(new Set());

  // Initialiser les numéros des tiers existants s'ils n'en ont pas
  useEffect(() => {
    if (tiers && tiers.length > 0) {
      const needsUpdate = tiers.some(t => !t.numero);
      if (needsUpdate) {
        const tiersWithNumbers = tiers.map((t, idx) => ({
          ...t,
          numero: t.numero || idx + 1
        }));
        
        if (projectId && updateProject) {
          const projectToUpdate = projects.find(p => p.id === projectId);
          if (projectToUpdate) {
            const updatedProject = { ...projectToUpdate, tiers: tiersWithNumbers };
            updateProject(updatedProject);
          }
        }
      }
    }
  }, [tiers, projectId, updateProject, projects]);

  // Fonction pour obtenir les couleurs des catégories avec plus de contraste
  const getCategoryColor = (categorie) => {
    const colors = {
      "Demandeur": "bg-blue-100 text-blue-900 border border-blue-300",
      "Défendeur": "bg-red-100 text-red-900 border border-red-300",
      "Avocat": "bg-purple-100 text-purple-900 border border-purple-300",
      "Conseil": "bg-green-100 text-green-900 border border-green-300",
      "Sapiteur": "bg-orange-100 text-orange-900 border border-orange-300",
      "Tribunal": "bg-gray-100 text-gray-900 border border-gray-400",
      "Autres": "bg-yellow-100 text-yellow-900 border border-yellow-300"
    };
    return colors[categorie] || "bg-gray-100 text-gray-900 border border-gray-300";
  };

  // Fonction pour basculer l'état développé/réduit d'un tiers
  const toggleTierExpansion = (index) => {
    const newExpanded = new Set(expandedTiers);
    if (newExpanded.has(index)) {
      newExpanded.delete(index);
    } else {
      newExpanded.add(index);
    }
    setExpandedTiers(newExpanded);
  };

  const handleChange = e => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // Gestion des champs personnalisés
  const addCustomField = () => {
    if (!newCustomField.label.trim()) return;
    
    const updatedCustomFields = [...form.customFields, { ...newCustomField, id: Date.now() }];
    setForm({ ...form, customFields: updatedCustomFields });
    setNewCustomField({ label: "", value: "" });
    setIsAddingCustomField(false);
  };

  const updateCustomField = (id, field, value) => {
    const updatedCustomFields = form.customFields.map(cf => 
      cf.id === id ? { ...cf, [field]: value } : cf
    );
    setForm({ ...form, customFields: updatedCustomFields });
  };

  const removeCustomField = (id) => {
    const updatedCustomFields = form.customFields.filter(cf => cf.id !== id);
    setForm({ ...form, customFields: updatedCustomFields });
  };

  const handleAdd = () => {
    if (!form.nom && !form.prenom && form.customFields.length === 0) return;
    
    // Calculer le prochain numéro disponible
    const existingNumbers = tiers.map(t => t.numero || 0);
    const nextNumber = existingNumbers.length > 0 ? Math.max(...existingNumbers) + 1 : 1;
    
    const nouveauTiers = { ...form, numero: nextNumber };
    const updatedTiers = [...tiers, nouveauTiers];
    
    // Si nous sommes dans le contexte d'un projet existant
    if (projectId && updateProject) {
      const projectToUpdate = projects.find(p => p.id === projectId);
      if (projectToUpdate) {
        const updatedProject = { ...projectToUpdate, tiers: updatedTiers };
        updateProject(updatedProject);
      }
    } else if (setProjects) {
      // Si nous sommes dans le contexte de création d'un nouveau projet
      setProjects([...projects, { tiers: updatedTiers }]);
    }
    
    // Réinitialiser le formulaire et fermer le formulaire d'ajout
    setForm({ 
      nom: "", 
      prenom: "", 
      adresse_numero: "",
      adresse_voie: "",
      adresse_code_postal: "",
      adresse_ville: "",
      telephone: "", 
      portable: "", 
      email: "", 
      societe: "", 
      categorie: "Demandeur",
      customFields: []
    });
    setShowAddForm(false);
    setIsAddingCustomField(false);
  };

  const handleDelete = idx => {
    if (window.confirm("Êtes-vous sûr de vouloir supprimer ce tiers ?")) {
    const updatedTiers = tiers.filter((_, i) => i !== idx);
    
    if (projectId && updateProject) {
      const projectToUpdate = projects.find(p => p.id === projectId);
      if (projectToUpdate) {
        const updatedProject = { ...projectToUpdate, tiers: updatedTiers };
        updateProject(updatedProject);
      }
      }
      
      // Retirer le tiers de la liste des tiers développés et réajuster les indices
      const newExpanded = new Set(expandedTiers);
      newExpanded.delete(idx);
      // Réajuster les indices pour les tiers suivants
      const adjustedExpanded = new Set();
      newExpanded.forEach(i => {
        if (i < idx) {
          adjustedExpanded.add(i);
        } else if (i > idx) {
          adjustedExpanded.add(i - 1);
        }
      });
      setExpandedTiers(adjustedExpanded);
    }
  };

  const handleEditField = (idx, field, value) => {
    const updatedTiers = tiers.map((t, i) => {
      if (i === idx) {
        // S'assurer que le tiers a un numéro fixe
        const tiersWithNumber = t.numero ? t : { ...t, numero: idx + 1 };
        return { ...tiersWithNumber, [field]: value };
      }
      return t;
    });
    
    if (projectId && updateProject) {
      const projectToUpdate = projects.find(p => p.id === projectId);
      if (projectToUpdate) {
        const updatedProject = { ...projectToUpdate, tiers: updatedTiers };
        updateProject(updatedProject);
      }
    }
  };

  const handleEditCustomField = (tiersIdx, fieldId, fieldKey, value) => {
    const updatedTiers = tiers.map((t, i) => {
      if (i === tiersIdx) {
        const updatedCustomFields = (t.customFields || []).map(cf => 
          cf.id === fieldId ? { ...cf, [fieldKey]: value } : cf
        );
        return { ...t, customFields: updatedCustomFields };
      }
      return t;
    });
    
    if (projectId && updateProject) {
      const projectToUpdate = projects.find(p => p.id === projectId);
      if (projectToUpdate) {
        const updatedProject = { ...projectToUpdate, tiers: updatedTiers };
        updateProject(updatedProject);
      }
    }
  };

  const addCustomFieldToTiers = (tiersIdx) => {
    const updatedTiers = tiers.map((t, i) => {
      if (i === tiersIdx) {
        const newField = { id: Date.now(), label: "Nouveau champ", value: "" };
        const updatedCustomFields = [...(t.customFields || []), newField];
        return { ...t, customFields: updatedCustomFields };
      }
      return t;
    });
    
    if (projectId && updateProject) {
      const projectToUpdate = projects.find(p => p.id === projectId);
      if (projectToUpdate) {
        const updatedProject = { ...projectToUpdate, tiers: updatedTiers };
        updateProject(updatedProject);
      }
    }
  };

  const removeCustomFieldFromTiers = (tiersIdx, fieldId) => {
    const updatedTiers = tiers.map((t, i) => {
      if (i === tiersIdx) {
        const updatedCustomFields = (t.customFields || []).filter(cf => cf.id !== fieldId);
        return { ...t, customFields: updatedCustomFields };
      }
      return t;
    });
    
    if (projectId && updateProject) {
      const projectToUpdate = projects.find(p => p.id === projectId);
      if (projectToUpdate) {
        const updatedProject = { ...projectToUpdate, tiers: updatedTiers };
        updateProject(updatedProject);
      }
    }
  };

  return (
    <div className="space-y-6">
      {/* Liste des tiers avec bouton d'ajout */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <div className="flex items-center justify-between p-6 border-b border-gray-200 bg-gradient-to-r from-blue-50 to-indigo-50">
          <h4 className="text-lg font-semibold text-gray-800 flex items-center">
            <svg className="w-5 h-5 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
            Liste des tiers
          </h4>
          <div className="flex items-center space-x-4">
            <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium">
              {tiers.length} tiers
            </span>
            <button
              onClick={() => setShowAddForm(true)}
              className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-150 flex items-center space-x-2 shadow-sm hover:shadow-md"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              <span>Ajouter un tiers</span>
            </button>
          </div>
        </div>

        {tiers.length === 0 ? (
          <div className="p-12 text-center">
            <svg className="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
            <h3 className="text-lg font-medium text-gray-700 mb-2">Aucun tiers ajouté</h3>
            <p className="text-gray-500">Commencez par ajouter votre premier tiers en cliquant sur le bouton "Ajouter un tiers".</p>
          </div>
        ) : (
          <div className="divide-y divide-gray-300">
            {tiers.map((t, idx) => (
              <div key={idx} className="transition-all duration-200">
                {/* Vue compacte - toujours visible */}
                <div 
                  className={`p-5 hover:bg-blue-50 cursor-pointer flex items-center justify-between transition-all duration-200 ${
                    idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'
                  } ${expandedTiers.has(idx) ? 'border-l-4 border-blue-500' : ''}`}
                  onClick={() => toggleTierExpansion(idx)}
                >
                  <div className="flex items-center space-x-4">
                    <div className="w-9 h-9 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-full flex items-center justify-center font-bold text-sm shadow-sm">
                      {t.numero || idx + 1}
                    </div>
                    <div className="flex items-center space-x-4">
                      <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold ${
                        getCategoryColor(t.categorie)
                      }`}>
                        {t.categorie}
                      </span>
                      <div className="flex items-center space-x-2">
                        {t.nom && <span className="font-semibold text-gray-900 text-sm">{t.nom}</span>}
                        {t.prenom && <span className="text-gray-700 text-sm">{t.prenom}</span>}
                        {!t.nom && !t.prenom && t.societe && <span className="font-semibold text-gray-900 text-sm">{t.societe}</span>}
                        {!t.nom && !t.prenom && !t.societe && <span className="text-gray-500 italic text-sm">Tiers sans nom</span>}
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center space-x-3">
                    {/* Indicateur de champs personnalisés */}
                    {t.customFields && t.customFields.length > 0 && (
                      <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800 border border-emerald-200">
                        {t.customFields.length} champ{t.customFields.length > 1 ? 's' : ''}
                      </span>
                    )}
                    {/* Bouton de suppression */}
                    <button 
                      onClick={(e) => {
                        e.stopPropagation();
                        handleDelete(idx);
                      }}
                      className="text-red-600 hover:text-red-800 hover:bg-red-100 p-2 rounded-lg transition-all duration-200 border border-transparent hover:border-red-200"
                      title="Supprimer ce tiers"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                    {/* Icône d'expansion/réduction */}
                    <svg 
                      className={`w-5 h-5 text-gray-600 transition-transform duration-200 ${expandedTiers.has(idx) ? 'rotate-180' : ''}`}
                      fill="none" 
                      stroke="currentColor" 
                      viewBox="0 0 24 24"
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                  </div>
                </div>

                {/* Vue détaillée - révélée au clic */}
                {expandedTiers.has(idx) && (
                  <div className="px-6 pb-6 bg-gradient-to-r from-blue-50 to-indigo-50 border-t border-blue-200 animate-fade-in">
                    <div className="pt-4 space-y-6">
                      {/* Sélecteur de catégorie */}
                      <div className="bg-white p-4 rounded-lg shadow-sm border border-blue-200">
                        <label className="block text-sm font-semibold text-blue-900 mb-2 flex items-center">
                          <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                          </svg>
                          Catégorie
                        </label>
                        <select 
                          value={t.categorie} 
                          onChange={e => handleEditField(idx, "categorie", e.target.value)} 
                          className="w-full border-2 border-blue-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white font-medium text-gray-900 shadow-sm"
                        >
                          {categories.map(cat => <option key={cat} value={cat}>{cat}</option>)}
                        </select>
                      </div>

                      {/* Informations personnelles */}
                      <div className="bg-white p-4 rounded-lg shadow-sm border border-green-200">
                        <h5 className="text-sm font-semibold text-green-900 mb-3 flex items-center">
                          <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                          </svg>
                          Informations personnelles
                        </h5>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                          <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Nom</label>
                            <input 
                              value={t.nom || ""} 
                              onChange={e => handleEditField(idx, "nom", e.target.value)} 
                              placeholder="Nom de famille"
                              className="w-full border-2 border-green-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 bg-white shadow-sm font-medium" 
                            />
                          </div>
                          <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Prénom</label>
                            <input 
                              value={t.prenom || ""} 
                              onChange={e => handleEditField(idx, "prenom", e.target.value)} 
                              placeholder="Prénom"
                              className="w-full border-2 border-green-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 bg-white shadow-sm font-medium" 
                            />
                          </div>
                          <div className="md:col-span-2 lg:col-span-1">
                            <label className="block text-sm font-medium text-gray-700 mb-2">Société</label>
                            <input 
                              value={t.societe || ""} 
                              onChange={e => handleEditField(idx, "societe", e.target.value)} 
                              placeholder="Nom de la société"
                              className="w-full border-2 border-green-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 bg-white shadow-sm font-medium" 
                            />
                          </div>
                        </div>
                      </div>

                      {/* Adresse */}
                      <div className="bg-white p-4 rounded-lg shadow-sm border border-purple-200">
                        <h5 className="text-sm font-semibold text-purple-900 mb-3 flex items-center">
                          <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                          </svg>
                          Adresse
                        </h5>
                        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                          <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">N°</label>
                            <input 
                              value={t.adresse_numero || ""} 
                              onChange={e => handleEditField(idx, "adresse_numero", e.target.value)} 
                              placeholder="123"
                              className="w-full border-2 border-purple-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 bg-white shadow-sm font-medium" 
                            />
                          </div>
                          <div className="md:col-span-2">
                            <label className="block text-sm font-medium text-gray-700 mb-2">Voie</label>
                            <input 
                              value={t.adresse_voie || ""} 
                              onChange={e => handleEditField(idx, "adresse_voie", e.target.value)} 
                              placeholder="Rue, avenue, boulevard..."
                              className="w-full border-2 border-purple-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 bg-white shadow-sm font-medium" 
                            />
                          </div>
                          <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Code postal</label>
                            <input 
                              value={t.adresse_code_postal || ""} 
                              onChange={e => handleEditField(idx, "adresse_code_postal", e.target.value)} 
                              placeholder="75000"
                              className="w-full border-2 border-purple-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 bg-white shadow-sm font-medium" 
                            />
                          </div>
                          <div className="md:col-span-2">
                            <label className="block text-sm font-medium text-gray-700 mb-2">Ville</label>
                            <input 
                              value={t.adresse_ville || ""} 
                              onChange={e => handleEditField(idx, "adresse_ville", e.target.value)} 
                              placeholder="Ville"
                              className="w-full border-2 border-purple-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 bg-white shadow-sm font-medium" 
                            />
                          </div>
                        </div>
                      </div>

                      {/* Contact */}
                      <div className="bg-white p-4 rounded-lg shadow-sm border border-orange-200">
                        <h5 className="text-sm font-semibold text-orange-900 mb-3 flex items-center">
                          <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                          </svg>
                          Contact
                        </h5>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                          <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Téléphone</label>
                            <input 
                              value={t.telephone || ""} 
                              onChange={e => handleEditField(idx, "telephone", e.target.value)} 
                              placeholder="01 23 45 67 89"
                              className="w-full border-2 border-orange-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500 bg-white shadow-sm font-medium" 
                            />
                          </div>
                          <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Portable</label>
                            <input 
                              value={t.portable || ""} 
                              onChange={e => handleEditField(idx, "portable", e.target.value)} 
                              placeholder="06 12 34 56 78"
                              className="w-full border-2 border-orange-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500 bg-white shadow-sm font-medium" 
                            />
                          </div>
                          <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
                            <input 
                              value={t.email || ""} 
                              onChange={e => handleEditField(idx, "email", e.target.value)} 
                              placeholder="adresse@email.com"
                              className="w-full border-2 border-orange-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500 bg-white shadow-sm font-medium" 
                            />
                          </div>
                        </div>
                      </div>

                      {/* Champs personnalisés du tiers */}
                      {(t.customFields && t.customFields.length > 0) && (
                        <div className="border-t pt-4">
                          <div className="flex items-center justify-between mb-3">
                            <h6 className="text-sm font-semibold text-gray-700 flex items-center">
                              <svg className="w-4 h-4 mr-1 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4" />
                              </svg>
                              Champs personnalisés
                            </h6>
                          </div>
                          <div className="space-y-2">
                            {t.customFields.map((field) => (
                              <div key={field.id} className="flex items-center space-x-2 p-3 bg-blue-50 rounded-lg">
                                <input 
                                  type="text"
                                  value={field.label || ""}
                                  onChange={(e) => handleEditCustomField(idx, field.id, 'label', e.target.value)}
                                  placeholder="Nom du champ"
                                  className="flex-1 border border-blue-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white text-sm"
                                />
                                <input 
                                  type="text"
                                  value={field.value || ""}
                                  onChange={(e) => handleEditCustomField(idx, field.id, 'value', e.target.value)}
                                  placeholder="Valeur"
                                  className="flex-1 border border-blue-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white text-sm"
                                />
                                <button 
                                  onClick={() => removeCustomFieldFromTiers(idx, field.id)}
                                  className="text-red-500 hover:text-red-700 hover:bg-red-100 p-1 rounded transition-all duration-200"
                                  title="Supprimer ce champ"
                                >
                                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                                  </svg>
                                </button>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Bouton pour ajouter un champ personnalisé à ce tiers */}
                      <div className="mt-4 pt-4 border-t">
                        <button
                          onClick={() => addCustomFieldToTiers(idx)}
                          className="text-blue-600 hover:text-blue-700 hover:bg-blue-50 px-3 py-2 rounded-lg transition-all duration-200 flex items-center space-x-2 text-sm font-medium"
                        >
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                          </svg>
                          <span>Ajouter un champ personnalisé</span>
                        </button>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Popup d'ajout de tiers */}
      {showAddForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            {/* Header du popup */}
            <div className="sticky top-0 bg-gradient-to-r from-blue-600 to-indigo-600 text-white p-6 rounded-t-2xl">
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="text-xl font-bold flex items-center">
                    <svg className="w-6 h-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                    </svg>
                    Ajouter un nouveau tiers
                  </h4>
                  <p className="text-blue-100 mt-1">Remplissez au moins un champ pour créer un tiers</p>
                </div>
                <button
                  onClick={() => {
                    setShowAddForm(false);
                    setIsAddingCustomField(false);
                    setNewCustomField({ label: "", value: "" });
                  }}
                  className="text-blue-100 hover:text-white hover:bg-blue-700 p-2 rounded-lg transition-colors"
                  title="Fermer le formulaire"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>

            {/* Contenu du popup */}
            <div className="p-6 space-y-6">
              {/* Catégorie */}
              <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
                <label className="block text-sm font-semibold text-blue-900 mb-2 flex items-center">
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                  </svg>
                  Catégorie
                </label>
          <select 
            name="categorie" 
            value={form.categorie} 
            onChange={handleChange} 
                  className="w-full border-2 border-blue-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white font-medium text-gray-900 shadow-sm"
          >
                  {categories.map(cat => <option key={cat} value={cat}>{cat}</option>)}
          </select>
              </div>

              {/* Informations personnelles */}
              <div className="bg-green-50 p-4 rounded-lg border border-green-200">
                <h5 className="text-sm font-semibold text-green-900 mb-3 flex items-center">
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                  Informations personnelles
                </h5>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Nom</label>
          <input 
            name="nom" 
            value={form.nom} 
            onChange={handleChange} 
                      placeholder="Nom de famille" 
                      className="w-full border-2 border-green-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 bg-white shadow-sm font-medium" 
          />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Prénom</label>
          <input 
            name="prenom" 
            value={form.prenom} 
            onChange={handleChange} 
            placeholder="Prénom" 
                      className="w-full border-2 border-green-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 bg-white shadow-sm font-medium" 
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Société</label>
          <input 
            name="societe" 
            value={form.societe} 
            onChange={handleChange} 
                      placeholder="Nom de la société" 
                      className="w-full border-2 border-green-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 bg-white shadow-sm font-medium" 
              />
            </div>
          </div>
      </div>
      
              {/* Adresse */}
              <div className="bg-purple-50 p-4 rounded-lg border border-purple-200">
                <h5 className="text-sm font-semibold text-purple-900 mb-3 flex items-center">
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                      </svg>
                  Adresse
                </h5>
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">N°</label>
                    <input 
                      name="adresse_numero" 
                      value={form.adresse_numero} 
                      onChange={handleChange} 
                      placeholder="123" 
                      className="w-full border-2 border-purple-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 bg-white shadow-sm font-medium" 
                    />
                  </div>
                  <div className="md:col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-2">Voie</label>
                    <input 
                      name="adresse_voie" 
                      value={form.adresse_voie} 
                      onChange={handleChange} 
                      placeholder="Rue, avenue, boulevard..." 
                      className="w-full border-2 border-purple-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 bg-white shadow-sm font-medium" 
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Code postal</label>
                    <input 
                      name="adresse_code_postal" 
                      value={form.adresse_code_postal} 
                      onChange={handleChange} 
                      placeholder="75000" 
                      className="w-full border-2 border-purple-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 bg-white shadow-sm font-medium" 
                    />
                  </div>
                  <div className="md:col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-2">Ville</label>
                    <input 
                      name="adresse_ville" 
                      value={form.adresse_ville} 
                      onChange={handleChange} 
                      placeholder="Ville" 
                      className="w-full border-2 border-purple-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 bg-white shadow-sm font-medium" 
                    />
                  </div>
                </div>
              </div>

              {/* Contact */}
              <div className="bg-orange-50 p-4 rounded-lg border border-orange-200">
                <h5 className="text-sm font-semibold text-orange-900 mb-3 flex items-center">
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                  </svg>
                  Contact
                </h5>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Téléphone</label>
                    <input 
                      name="telephone" 
                      value={form.telephone} 
                      onChange={handleChange} 
                      placeholder="01 23 45 67 89" 
                      className="w-full border-2 border-orange-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500 bg-white shadow-sm font-medium" 
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Portable</label>
                    <input 
                      name="portable" 
                      value={form.portable} 
                      onChange={handleChange} 
                      placeholder="06 12 34 56 78" 
                      className="w-full border-2 border-orange-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500 bg-white shadow-sm font-medium" 
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
                    <input 
                      name="email" 
                      type="email"
                      value={form.email} 
                      onChange={handleChange} 
                      placeholder="exemple@email.com" 
                      className="w-full border-2 border-orange-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500 bg-white shadow-sm font-medium" 
                    />
                  </div>
                </div>
                            </div>
              
              {/* Section Champs Personnalisés */}
              <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
            <div className="flex items-center justify-between mb-4">
              <h5 className="text-md font-semibold text-gray-800 flex items-center">
                <svg className="w-5 h-5 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4" />
                </svg>
                Champs personnalisés
              </h5>
              <span className="text-sm text-gray-500">
                {form.customFields.length} champ{form.customFields.length > 1 ? 's' : ''}
              </span>
            </div>

            {/* Liste des champs personnalisés existants */}
            <div className="space-y-3 mb-4">
              {form.customFields.map((field, index) => (
                <div key={field.id} className="flex items-center space-x-3 p-4 bg-blue-50 rounded-lg border border-blue-200 animate-fade-in">
                  <div className="flex-1 grid grid-cols-1 md:grid-cols-2 gap-3">
                    <input 
                      type="text"
                      value={field.label}
                      onChange={(e) => updateCustomField(field.id, 'label', e.target.value)}
                      placeholder="Nom du champ (ex: N° dossier)"
                      className="border border-blue-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white"
                    />
                    <input 
                      type="text"
                      value={field.value}
                      onChange={(e) => updateCustomField(field.id, 'value', e.target.value)}
                      placeholder="Valeur à anonymiser"
                      className="border border-blue-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white"
                    />
                  </div>
                    <button 
                    onClick={() => removeCustomField(field.id)}
                    className="text-red-500 hover:text-red-700 hover:bg-red-100 p-2 rounded-lg transition-all duration-200"
                    title="Supprimer ce champ"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                </div>
              ))}
            </div>

            {/* Zone d'ajout de nouveau champ personnalisé */}
            {isAddingCustomField ? (
              <div className="p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border-2 border-blue-200 animate-fade-in">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-3">
                  <input
                    type="text"
                    value={newCustomField.label}
                    onChange={(e) => setNewCustomField({...newCustomField, label: e.target.value})}
                    placeholder="Nom du champ (ex: N° SIRET, Référence...)"
                    className="border border-blue-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white"
                    autoFocus
                  />
                  <input 
                    type="text"
                    value={newCustomField.value}
                    onChange={(e) => setNewCustomField({...newCustomField, value: e.target.value})}
                    placeholder="Valeur à anonymiser" 
                    className="border border-blue-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white"
                  />
                </div>
                <div className="flex justify-end space-x-2">
                  <button
                    onClick={() => {
                      setIsAddingCustomField(false);
                      setNewCustomField({ label: "", value: "" });
                    }}
                    className="px-4 py-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-all duration-200"
                  >
                    Annuler
                  </button>
                  <button
                    onClick={addCustomField}
                    disabled={!newCustomField.label.trim()}
                    className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white rounded-lg transition-all duration-200 flex items-center space-x-2"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                    </svg>
                    <span>Ajouter</span>
                  </button>
                </div>
              </div>
            ) : (
              <button
                onClick={() => setIsAddingCustomField(true)}
                className="w-full p-4 border-2 border-dashed border-blue-300 hover:border-blue-400 rounded-lg text-blue-600 hover:text-blue-700 hover:bg-blue-50 transition-all duration-200 flex items-center justify-center space-x-2 group"
              >
                <svg className="w-5 h-5 group-hover:scale-110 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
                <span className="font-medium">Ajouter un champ personnalisé</span>
              </button>
            )}
          </div>

              {/* Bouton d'ajout du tiers */}
              <div className="bg-white p-4 rounded-lg border border-gray-200 sticky bottom-0">
                <button 
                  type="button" 
                  className="w-full bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-white font-semibold py-4 px-6 rounded-lg transition-all duration-200 flex items-center justify-center space-x-2 shadow-lg hover:shadow-xl transform hover:scale-105"
                  onClick={handleAdd}
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                  <span>Ajouter ce tiers au projet</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      <style jsx>{`
        @keyframes fade-in {
          from {
            opacity: 0;
            transform: translateY(-10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        .animate-fade-in {
          animation: fade-in 0.3s ease-out;
        }
      `}</style>
    </div>
  );
}

export default TiersForm; 