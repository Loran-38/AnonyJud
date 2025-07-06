import React, { useState, useEffect } from "react";

/**
 * Formulaire pour ajouter et gérer les tiers d'un projet (demandeur, défendeur, etc.).
 * C'est un composant "contrôlé" : il reçoit les tiers et notifie le parent de tout changement.
 */
function TiersForm({ projectId, tiers = [], updateProject, projects, setProjects }) {
  const [form, setForm] = useState({
    nom: "",
    prenom: "",
    adresse: "",
    telephone: "",
    portable: "",
    email: "",
    societe: "",
    categorie: "Demandeur",
    champPerso: "",
    labelChampPerso: "Champ personnalisé"
  });

  const categories = [
    "Demandeur", "Défendeur", "Avocat", "Conseil", "Sapiteur", "Tribunal", "Autres"
  ];

  const handleChange = e => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleAdd = () => {
    if (!form.nom && !form.prenom && !form.champPerso) return;
    
    const nouveauTiers = { ...form };
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
    
    // Réinitialiser le formulaire
    setForm({ 
      nom: "", 
      prenom: "", 
      adresse: "", 
      telephone: "", 
      portable: "", 
      email: "", 
      societe: "", 
      categorie: form.categorie,
      champPerso: "",
      labelChampPerso: form.labelChampPerso
    });
  };

  const handleDelete = idx => {
    const updatedTiers = tiers.filter((_, i) => i !== idx);
    
    if (projectId && updateProject) {
      const projectToUpdate = projects.find(p => p.id === projectId);
      if (projectToUpdate) {
        const updatedProject = { ...projectToUpdate, tiers: updatedTiers };
        updateProject(updatedProject);
      }
    }
  };

  const handleEditField = (idx, field, value) => {
    const updatedTiers = tiers.map((t, i) => i === idx ? { ...t, [field]: value } : t);
    
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
      {/* Formulaire d'ajout de tiers */}
      <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
        <h4 className="text-md font-medium text-gray-700 mb-3">Ajouter un nouveau tiers</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-3">
          <select 
            name="categorie" 
            value={form.categorie} 
            onChange={handleChange} 
            className="border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            {categories.map(cat => <option key={cat}>{cat}</option>)}
          </select>
          <input 
            name="nom" 
            value={form.nom} 
            onChange={handleChange} 
            placeholder="Nom" 
            className="border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" 
          />
          <input 
            name="prenom" 
            value={form.prenom} 
            onChange={handleChange} 
            placeholder="Prénom" 
            className="border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" 
          />
          <input 
            name="adresse" 
            value={form.adresse} 
            onChange={handleChange} 
            placeholder="Adresse complète" 
            className="border border-gray-300 rounded-md px-3 py-2 md:col-span-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" 
          />
          <input 
            name="telephone" 
            value={form.telephone} 
            onChange={handleChange} 
            placeholder="Téléphone fixe" 
            className="border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" 
          />
          <input 
            name="portable" 
            value={form.portable} 
            onChange={handleChange} 
            placeholder="Portable" 
            className="border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" 
          />
          <input 
            name="email" 
            value={form.email} 
            onChange={handleChange} 
            placeholder="Email" 
            className="border border-gray-300 rounded-md px-3 py-2 md:col-span-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" 
          />
          <input 
            name="societe" 
            value={form.societe} 
            onChange={handleChange} 
            placeholder="Société" 
            className="border border-gray-300 rounded-md px-3 py-2 md:col-span-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" 
          />
          
          {/* Champ personnalisé */}
          <div className="md:col-span-2 grid grid-cols-1 md:grid-cols-2 gap-3 p-3 bg-blue-50 rounded-md border border-blue-100">
            <div className="flex flex-col">
              <label className="text-sm font-medium text-blue-700 mb-1">Nom du champ personnalisé</label>
              <input 
                name="labelChampPerso" 
                value={form.labelChampPerso} 
                onChange={handleChange} 
                placeholder="Ex: Numéro de dossier, SIRET..." 
                className="border border-blue-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" 
              />
            </div>
            <div className="flex flex-col">
              <label className="text-sm font-medium text-blue-700 mb-1">Valeur à anonymiser</label>
              <input 
                name="champPerso" 
                value={form.champPerso} 
                onChange={handleChange} 
                placeholder="Valeur à anonymiser" 
                className="border border-blue-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" 
              />
            </div>
          </div>
        </div>
        <button 
          type="button" 
          className="w-full bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-4 rounded-md transition-colors duration-150 flex items-center justify-center"
          onClick={handleAdd}
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clipRule="evenodd" />
          </svg>
          Ajouter ce tiers
        </button>
      </div>
      
      {/* Tableau des tiers */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        <h4 className="text-md font-medium text-gray-700 p-4 border-b">Liste des tiers ({tiers.length})</h4>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-gray-100 text-left">
                <th className="p-3 w-12 text-gray-600">#</th>
                <th className="p-3 text-gray-600">Catégorie</th>
                <th className="p-3 text-gray-600">Nom</th>
                <th className="p-3 text-gray-600">Prénom</th>
                <th className="p-3 text-gray-600">Adresse</th>
                <th className="p-3 text-gray-600">Tél</th>
                <th className="p-3 text-gray-600">Portable</th>
                <th className="p-3 text-gray-600">Email</th>
                <th className="p-3 text-gray-600">Société</th>
                <th className="p-3 text-gray-600 bg-blue-50">Champ perso.</th>
                <th className="p-3 text-gray-600 bg-blue-50">Valeur</th>
                <th className="p-3 w-20 text-gray-600"></th>
              </tr>
            </thead>
            <tbody>
              {tiers.length === 0 && (
                <tr>
                  <td colSpan={12} className="italic text-gray-400 p-4 text-center">
                    <div className="flex flex-col items-center py-6">
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 text-gray-300 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                      </svg>
                      Aucun tiers ajouté
                    </div>
                  </td>
                </tr>
              )}
              {tiers.map((t, idx) => (
                <tr key={idx} className={`border-t ${idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'} hover:bg-blue-50 transition-colors duration-150`}>
                  <td className="p-2 text-center font-semibold text-gray-700">{idx + 1}</td>
                  <td className="p-2">
                    <select 
                      value={t.categorie} 
                      onChange={e => handleEditField(idx, "categorie", e.target.value)} 
                      className="border border-gray-300 rounded-md px-2 py-1 w-full focus:outline-none focus:ring-1 focus:ring-blue-500"
                    >
                      {categories.map(cat => <option key={cat}>{cat}</option>)}
                    </select>
                  </td>
                  <td className="p-2">
                    <input 
                      value={t.nom} 
                      onChange={e => handleEditField(idx, "nom", e.target.value)} 
                      className="border border-gray-300 rounded-md px-2 py-1 w-full focus:outline-none focus:ring-1 focus:ring-blue-500" 
                    />
                  </td>
                  <td className="p-2">
                    <input 
                      value={t.prenom} 
                      onChange={e => handleEditField(idx, "prenom", e.target.value)} 
                      className="border border-gray-300 rounded-md px-2 py-1 w-full focus:outline-none focus:ring-1 focus:ring-blue-500" 
                    />
                  </td>
                  <td className="p-2">
                    <input 
                      value={t.adresse} 
                      onChange={e => handleEditField(idx, "adresse", e.target.value)} 
                      className="border border-gray-300 rounded-md px-2 py-1 w-full focus:outline-none focus:ring-1 focus:ring-blue-500" 
                    />
                  </td>
                  <td className="p-2">
                    <input 
                      value={t.telephone} 
                      onChange={e => handleEditField(idx, "telephone", e.target.value)} 
                      className="border border-gray-300 rounded-md px-2 py-1 w-full focus:outline-none focus:ring-1 focus:ring-blue-500" 
                    />
                  </td>
                  <td className="p-2">
                    <input 
                      value={t.portable} 
                      onChange={e => handleEditField(idx, "portable", e.target.value)} 
                      className="border border-gray-300 rounded-md px-2 py-1 w-full focus:outline-none focus:ring-1 focus:ring-blue-500" 
                    />
                  </td>
                  <td className="p-2">
                    <input 
                      value={t.email} 
                      onChange={e => handleEditField(idx, "email", e.target.value)} 
                      className="border border-gray-300 rounded-md px-2 py-1 w-full focus:outline-none focus:ring-1 focus:ring-blue-500" 
                    />
                  </td>
                  <td className="p-2">
                    <input 
                      value={t.societe} 
                      onChange={e => handleEditField(idx, "societe", e.target.value)} 
                      className="border border-gray-300 rounded-md px-2 py-1 w-full focus:outline-none focus:ring-1 focus:ring-blue-500" 
                    />
                  </td>
                  <td className="p-2 bg-blue-50">
                    <input 
                      value={t.labelChampPerso || "Champ personnalisé"} 
                      onChange={e => handleEditField(idx, "labelChampPerso", e.target.value)} 
                      className="border border-blue-300 rounded-md px-2 py-1 w-full focus:outline-none focus:ring-1 focus:ring-blue-500 bg-white" 
                    />
                  </td>
                  <td className="p-2 bg-blue-50">
                    <input 
                      value={t.champPerso || ""} 
                      onChange={e => handleEditField(idx, "champPerso", e.target.value)} 
                      className="border border-blue-300 rounded-md px-2 py-1 w-full focus:outline-none focus:ring-1 focus:ring-blue-500 bg-white" 
                    />
                  </td>
                  <td className="p-2 text-center">
                    <button 
                      onClick={() => handleDelete(idx)} 
                      className="text-red-600 hover:text-red-800 hover:bg-red-100 p-1 rounded-full transition-colors duration-150"
                      title="Supprimer"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                      </svg>
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default TiersForm; 