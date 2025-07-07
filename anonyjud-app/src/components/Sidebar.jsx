import React, { useState } from "react";

/**
 * Sidebar affichant la liste des projets et permettant d'en créer ou supprimer.
 */
function Sidebar({ projects, selectedProject, setSelectedProject, createProject, deleteProject, canCreateProject, userPlan, maxProjects }) {
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showConfirmDelete, setShowConfirmDelete] = useState(null); // Stocke l'objet projet à supprimer

  // États locaux pour le formulaire de la modale de création
  const [nomProjet, setNomProjet] = useState("");

  // Fonction pour créer un nouveau projet
  const handleCreateProject = () => {
    if (!nomProjet.trim()) return;
    
    const newProject = {
      nom: nomProjet.trim(),
      tiers: [],
    };
    
    console.log('Création du projet:', newProject);
    createProject(newProject);
    
    setShowCreateModal(false);
    setNomProjet("");
  };
  
  // Fonction pour supprimer un projet
  const handleDeleteProject = (projectToDelete) => {
    if (!projectToDelete) return;
    
    deleteProject(projectToDelete.id);
    setShowConfirmDelete(null);
  };

  return (
    <>
      <aside className="w-full h-full bg-gray-800 text-white flex flex-col shadow-lg">
        <div className="p-4 border-b border-gray-700">
          <h2 className="text-xl font-bold flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" />
            </svg>
            AnonyJud
          </h2>
          <p className="text-sm text-gray-400 mt-1">Anonymisation de documents</p>
        </div>
        
        <div className="p-4">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-md font-semibold text-gray-300">Projets</h3>
            <span className="bg-blue-600 text-xs rounded-full px-2 py-1">
              {projects.length}{maxProjects !== -1 ? `/${maxProjects}` : ''}
            </span>
          </div>
          
          {userPlan && (
            <div className="mb-4 p-2 bg-gray-700 bg-opacity-50 rounded text-xs">
              <p className="text-gray-400">Plan: <span className="text-white font-medium">{userPlan}</span></p>
              {maxProjects !== -1 && (
                <p className="text-gray-400">
                  Limite: {projects.length}/{maxProjects} projets
                </p>
              )}
            </div>
          )}
          
          <div className="flex-1 overflow-y-auto space-y-1 mb-4 max-h-[calc(100vh-220px)]">
            {projects.length === 0 && (
              <div className="text-gray-500 italic text-sm bg-gray-700 bg-opacity-30 p-3 rounded text-center">
                Aucun projet
              </div>
            )}
            
            {projects.map((p) => (
              <div 
                key={p.id} 
                className={`py-2 px-3 flex items-center justify-between rounded cursor-pointer transition-colors duration-150 ${
                  selectedProject?.id === p.id 
                    ? "bg-blue-600 text-white" 
                    : "text-gray-300 hover:bg-gray-700"
                }`}
                title={p.nom}
                onClick={() => setSelectedProject(p)}
              >
                <div className="flex items-center truncate">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  <span className="truncate font-medium flex-1">{p.nom}</span>
                </div>
                <button 
                  className={`ml-2 text-gray-400 hover:text-red-400 p-1 rounded-full hover:bg-red-900 hover:bg-opacity-30 flex-shrink-0 ${
                    selectedProject?.id === p.id ? "text-white hover:text-red-200" : ""
                  }`} 
                  title="Supprimer le projet" 
                  onClick={(e) => {
                    e.stopPropagation();
                    setShowConfirmDelete(p);
                  }}
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            ))}
          </div>
          
          <button
            className={`w-full py-2 px-4 rounded transition-colors duration-150 flex items-center justify-center ${
              canCreateProject() 
                ? "bg-blue-600 hover:bg-blue-700 text-white" 
                : "bg-gray-600 text-gray-400 cursor-not-allowed"
            }`}
            onClick={() => {
              if (canCreateProject()) {
                setNomProjet('');
                setShowCreateModal(true);
              }
            }}
            disabled={!canCreateProject()}
            title={canCreateProject() ? "Créer un nouveau projet" : "Limite de projets atteinte"}
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clipRule="evenodd" />
            </svg>
            Nouveau projet
          </button>
        </div>
        
        <div className="mt-auto border-t border-gray-700 p-4">
          <div className="text-xs text-gray-500 text-center">
            AnonyJud v1.0.0
          </div>
        </div>
      </aside>

      {/* Modale de création de projet */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg shadow-xl w-full max-w-5xl max-h-[90vh] overflow-auto">
            <div className="flex justify-between items-center mb-6 border-b pb-3">
              <h3 className="text-xl font-bold text-gray-800">Créer un nouveau projet</h3>
              <button 
                onClick={() => setShowCreateModal(false)}
                className="text-gray-500 hover:text-gray-700 transition-colors duration-150"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            <div className="mb-6">
              <label htmlFor="project-name" className="block text-sm font-medium text-gray-700 mb-1">
                Nom du projet
              </label>
              <input
                id="project-name"
                className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Nom du projet (ex: Maison Martin - Lyon)"
                value={nomProjet}
                onChange={e => setNomProjet(e.target.value)}
              />
            </div>
            
            <div className="mb-6">
              <h4 className="text-md font-medium text-gray-700 mb-3">Ajouter des tiers au projet (optionnel)</h4>
              <div className="bg-gray-50 p-4 rounded-lg">
                <p className="text-sm text-gray-600 mb-3">
                  Vous pourrez ajouter des tiers après la création du projet.
                </p>
                <div className="text-xs text-gray-500">
                  Les tiers permettent de personnaliser l'anonymisation pour chaque personne impliquée dans le dossier.
                </div>
              </div>
            </div>
            
            <div className="flex justify-end gap-3 border-t pt-4">
              <button 
                className="bg-gray-200 hover:bg-gray-300 text-gray-700 px-4 py-2 rounded-md transition-colors duration-150"
                onClick={() => setShowCreateModal(false)}
              >
                Annuler
              </button>
              <button 
                className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md transition-colors duration-150 disabled:opacity-50"
                onClick={handleCreateProject}
                disabled={!nomProjet.trim()}
              >
                Créer le projet
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Modale de confirmation de suppression */}
      {showConfirmDelete !== null && (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg shadow-xl w-full max-w-md">
            <div className="mb-5">
              <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100 mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              </div>
              <h3 className="text-lg font-medium text-center text-gray-900 mb-2">Confirmer la suppression</h3>
              <p className="text-gray-500 text-center">
                Voulez-vous vraiment supprimer le projet <span className="font-semibold text-gray-700">{showConfirmDelete.nom}</span> ? Cette action est irréversible.
              </p>
            </div>
            <div className="flex justify-end gap-3">
              <button 
                className="bg-gray-200 hover:bg-gray-300 text-gray-700 px-4 py-2 rounded-md transition-colors duration-150"
                onClick={() => setShowConfirmDelete(null)}
              >
                Annuler
              </button>
              <button 
                className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md transition-colors duration-150"
                onClick={() => handleDeleteProject(showConfirmDelete)}
              >
                Supprimer
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default Sidebar; 