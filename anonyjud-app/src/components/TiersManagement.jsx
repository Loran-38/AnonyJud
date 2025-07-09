import React from 'react';
import TiersForm from './TiersForm';

const TiersManagement = ({ selectedProject, updateProject }) => {
  if (!selectedProject) {
    return (
      <div className="h-full flex items-center justify-center text-center">
        <div>
          <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Aucun projet sélectionné
          </h3>
          <p className="text-gray-600">
            Sélectionnez un projet pour gérer les tiers.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full">
      <div className="p-6 border-b bg-gray-50">
        <h2 className="text-xl font-semibold text-gray-900">Gestion des tiers</h2>
        <p className="text-gray-600 mt-1">
          Projet: {selectedProject.nom}
        </p>
      </div>
      
      <div className="p-6 overflow-y-auto" style={{ height: 'calc(100% - 88px)' }}>
        <TiersForm 
          selectedProject={selectedProject}
          updateProject={updateProject}
        />
      </div>
    </div>
  );
};

export default TiersManagement; 