import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { collection, query, where, getDocs, addDoc, updateDoc, deleteDoc, doc } from 'firebase/firestore';
import { db } from '../firebase/config';
import Sidebar from '../components/Sidebar';
import MainPanel from '../components/MainPanel';

const DashboardPage = () => {
  const { currentUser, userProfile, canCreateProject, PLANS } = useAuth();
  const [projects, setProjects] = useState([]);
  const [selectedProject, setSelectedProject] = useState(null);
  const [loading, setLoading] = useState(true);

  // Charger les projets depuis Firebase
  useEffect(() => {
    if (currentUser) {
      loadProjects();
    }
  }, [currentUser]);

  const loadProjects = async () => {
    try {
      const projectsRef = collection(db, 'projects');
      const q = query(projectsRef, where('userId', '==', currentUser.uid));
      const querySnapshot = await getDocs(q);
      
      const projectsData = [];
      querySnapshot.forEach((doc) => {
        projectsData.push({
          id: doc.id,
          ...doc.data()
        });
      });
      
      setProjects(projectsData);
      
      // Sélectionner le premier projet s'il y en a un
      if (projectsData.length > 0 && !selectedProject) {
        setSelectedProject(projectsData[0]);
      }
    } catch (error) {
      console.error('Erreur lors du chargement des projets:', error);
    } finally {
      setLoading(false);
    }
  };

  const createProject = async (projectData) => {
    if (!canCreateProject()) {
      alert(`Vous avez atteint la limite de votre plan ${PLANS[userProfile.plan]?.name}. Passez à un plan supérieur pour créer plus de projets.`);
      return;
    }

    try {
      const newProject = {
        ...projectData,
        userId: currentUser.uid,
        createdAt: new Date().toISOString(),
        tiers: []
      };

      const docRef = await addDoc(collection(db, 'projects'), newProject);
      const projectWithId = { id: docRef.id, ...newProject };
      
      setProjects(prev => [...prev, projectWithId]);
      setSelectedProject(projectWithId);
      
      // Mettre à jour le compteur de projets dans le profil utilisateur
      // TODO: Implémenter la mise à jour du compteur
      
    } catch (error) {
      console.error('Erreur lors de la création du projet:', error);
    }
  };

  const updateProject = async (updatedProject) => {
    try {
      const projectRef = doc(db, 'projects', updatedProject.id);
      const { id, ...projectData } = updatedProject;
      
      await updateDoc(projectRef, projectData);
      
      setProjects(prev => 
        prev.map(p => p.id === updatedProject.id ? updatedProject : p)
      );
      
      if (selectedProject && selectedProject.id === updatedProject.id) {
        setSelectedProject(updatedProject);
      }
    } catch (error) {
      console.error('Erreur lors de la mise à jour du projet:', error);
    }
  };

  const deleteProject = async (projectId) => {
    try {
      await deleteDoc(doc(db, 'projects', projectId));
      
      setProjects(prev => prev.filter(p => p.id !== projectId));
      
      if (selectedProject && selectedProject.id === projectId) {
        setSelectedProject(null);
      }
    } catch (error) {
      console.error('Erreur lors de la suppression du projet:', error);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <svg className="animate-spin -ml-1 mr-3 h-8 w-8 text-blue-600 mx-auto" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <p className="text-gray-600 mt-2">Chargement de vos projets...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header Dashboard */}
      <div className="bg-white shadow-sm border-b">
        <div className="container mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
              <p className="text-gray-600">
                Bienvenue, {currentUser?.displayName || 'Utilisateur'}
              </p>
            </div>
            
            {userProfile && (
              <div className="text-right">
                <p className="text-sm font-medium text-gray-900">
                  Plan {PLANS[userProfile.plan]?.name || 'Gratuit'}
                </p>
                <p className="text-sm text-gray-600">
                  {projects.length} / {PLANS[userProfile.plan]?.maxProjects === -1 ? '∞' : PLANS[userProfile.plan]?.maxProjects} projets
                </p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-6">
        <div className="flex h-[calc(100vh-200px)] gap-6">
          {/* Sidebar */}
          <div className="w-80 bg-white rounded-lg shadow-sm overflow-hidden">
            <Sidebar
              projects={projects}
              selectedProject={selectedProject}
              setSelectedProject={setSelectedProject}
              createProject={createProject}
              deleteProject={deleteProject}
              canCreateProject={canCreateProject}
              userPlan={userProfile?.plan || 'FREE'}
              maxProjects={PLANS[userProfile?.plan || 'FREE']?.maxProjects}
            />
          </div>

          {/* Main Panel */}
          <div className="flex-1 bg-white rounded-lg shadow-sm overflow-hidden">
            {selectedProject ? (
              <MainPanel
                selectedProject={selectedProject}
                updateProject={updateProject}
                projects={projects}
                setProjects={setProjects}
              />
            ) : (
              <div className="h-full flex items-center justify-center text-center">
                <div>
                  <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  <h3 className="text-lg font-medium text-gray-900 mb-2">
                    Aucun projet sélectionné
                  </h3>
                  <p className="text-gray-600 mb-4">
                    Créez un nouveau projet ou sélectionnez un projet existant pour commencer l'anonymisation.
                  </p>
                  {canCreateProject() && (
                    <button
                      onClick={() => {
                        const projectName = prompt('Nom du projet:');
                        if (projectName) {
                          createProject({ nom: projectName });
                        }
                      }}
                      className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md transition-colors"
                    >
                      Créer un projet
                    </button>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage; 