import React, { useState, useEffect } from "react";
import Sidebar from "./components/Sidebar";
import MainPanel from "./components/MainPanel";
import './index.css';

/**
 * Composant principal de l'application AnonyJud.
 * Gère l'état global de l'application : projets, projet sélectionné.
 */
function App() {
  // État pour stocker les projets
  const [projects, setProjects] = useState([]);
  
  // État pour le projet actuellement sélectionné
  const [selectedProject, setSelectedProject] = useState(null);

  // Charger les projets depuis le localStorage au démarrage
  useEffect(() => {
    const savedProjects = localStorage.getItem('anonyjud_projects');
    if (savedProjects) {
      try {
        const parsedProjects = JSON.parse(savedProjects);
        setProjects(parsedProjects);
      } catch (e) {
        console.error("Erreur lors du chargement des projets:", e);
      }
    }
  }, []);

  // Sauvegarder les projets dans le localStorage à chaque modification
  useEffect(() => {
    localStorage.setItem('anonyjud_projects', JSON.stringify(projects));
  }, [projects]);

  // Fonction pour mettre à jour un projet
  const updateProject = (updatedProject) => {
    const updatedProjects = projects.map(p => 
      p.id === updatedProject.id ? updatedProject : p
    );
    setProjects(updatedProjects);
    setSelectedProject(updatedProject);
  };

  return (
    <div className="flex h-screen bg-gray-100 overflow-hidden">
      <Sidebar 
        projects={projects} 
        selectedProject={selectedProject} 
        setSelectedProject={setSelectedProject} 
        setProjects={setProjects} 
      />
      <main className="flex-1 overflow-auto">
        <MainPanel 
          selectedProject={selectedProject} 
          updateProject={updateProject} 
          projects={projects}
          setProjects={setProjects}
        />
      </main>
    </div>
  );
}

export default App; 