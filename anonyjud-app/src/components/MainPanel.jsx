import React, { useState, useEffect, useRef } from 'react';
import TiersForm from './TiersForm';
import AnonymizationPanel from './AnonymizationPanel';
import config from '../config';

/**
 * Zone principale de l'application : affichage du projet sélectionné, gestion des tiers,
 * anonymisation et désanonymisation.
 * Interface refaite avec deux colonnes verticales selon le design demandé.
 */
const MainPanel = ({ selectedProject, updateProject, projects, setProjects }) => {
  return (
    <div className="flex flex-col h-full w-full bg-white p-6 overflow-hidden">
      {selectedProject ? (
        <>
          <h2 className="text-2xl font-bold mb-6 text-gray-800 border-b pb-2">
            Projet: {selectedProject.nom} • {selectedProject.tiers?.length || 0} tiers configurés
          </h2>
          
          <div className="flex flex-col lg:flex-row h-full gap-6">
            {/* Partie des tiers - Maintenant 30% de la largeur */}
            <div className="w-full lg:w-1/3 overflow-auto bg-gray-50 rounded-lg shadow-sm p-4">
              <h3 className="text-lg font-semibold mb-4 text-gray-700">Gestion des tiers</h3>
              <TiersForm 
                projectId={selectedProject.id} 
                tiers={selectedProject.tiers || []} 
                updateProject={updateProject}
                projects={projects}
                setProjects={setProjects}
              />
            </div>
            
            {/* Partie anonymisation - Maintenant 70% de la largeur */}
            <div className="w-full lg:w-2/3 flex flex-col h-full">
              <AnonymizationPanel 
                selectedProject={selectedProject}
                updateProject={updateProject}
                projects={projects}
                setProjects={setProjects}
              />
            </div>
          </div>
        </>
      ) : (
        <div className="flex flex-col items-center justify-center h-full bg-gray-50 rounded-lg p-10">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-16 w-16 text-gray-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <p className="text-gray-500 text-lg">Veuillez sélectionner ou créer un projet dans la barre latérale.</p>
          <p className="text-gray-400 mt-2">Vous pourrez ensuite gérer les tiers et anonymiser vos documents.</p>
        </div>
      )}
    </div>
  );
};

export default MainPanel; 