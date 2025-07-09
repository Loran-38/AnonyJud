import React, { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { collection, query, where, getDocs, addDoc, updateDoc, deleteDoc, doc } from 'firebase/firestore';
import { db } from '../firebase/config';
import Sidebar from '../components/Sidebar';
import TiersManagement from '../components/TiersManagement';
import AnonymizationPanel from '../components/AnonymizationPanel';
import AiChatPanel from '../components/AiChatPanel';

const DashboardPage = () => {
  const { currentUser, userProfile, canCreateProject, PLANS } = useAuth();
  const [projects, setProjects] = useState([]);
  const [selectedProject, setSelectedProject] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('tiers');

  // Fonction pour charger les projets depuis Firebase
  const loadProjects = useCallback(async () => {
    if (!currentUser) return;
    
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
  }, [currentUser, selectedProject]);

  // Charger les projets au montage du composant
  useEffect(() => {
    loadProjects();
  }, [loadProjects]);

  const createProject = async (projectData) => {
    console.log('createProject appelé avec:', projectData);
    console.log('currentUser:', currentUser);
    console.log('userProfile:', userProfile);
    console.log('canCreateProject():', canCreateProject(projects.length));
    
    if (!canCreateProject(projects.length)) {
      alert(`Vous avez atteint la limite de votre plan ${PLANS[userProfile.plan]?.name}. Passez à un plan supérieur pour créer plus de projets.`);
      return;
    }

    // Test de connexion Firebase
    try {
      console.log('Test de connexion Firebase...');
      const testQuery = query(collection(db, 'projects'), where('userId', '==', currentUser.uid));
      const testSnapshot = await getDocs(testQuery);
      console.log('Connexion Firebase OK, nombre de projets existants:', testSnapshot.size);
    } catch (testError) {
      console.error('Erreur de connexion Firebase:', testError);
      alert(`Erreur de connexion Firebase: ${testError.message}`);
      return;
    }

    try {
      const newProject = {
        ...projectData,
        userId: currentUser.uid,
        createdAt: new Date().toISOString(),
        tiers: projectData.tiers || []
      };

      console.log('Données du projet à créer:', newProject);
      console.log('Collection de destination:', collection(db, 'projects'));
      
      const docRef = await addDoc(collection(db, 'projects'), newProject);
      console.log('Projet créé avec ID:', docRef.id);
      
      const projectWithId = { id: docRef.id, ...newProject };
      
      setProjects(prev => {
        const updatedProjects = [...prev, projectWithId];
        console.log('Projets mis à jour:', updatedProjects);
        return updatedProjects;
      });
      setSelectedProject(projectWithId);
      
      console.log('Projet créé avec succès');
      alert('Projet créé avec succès !');
      
    } catch (error) {
      console.error('Erreur lors de la création du projet:', error);
      console.error('Code d\'erreur:', error.code);
      console.error('Message d\'erreur:', error.message);
      console.error('Détails complets:', error);
      
      if (error.code === 'permission-denied') {
        alert('Erreur de permissions Firebase. Vérifiez les règles de sécurité Firestore.');
      } else if (error.code === 'unavailable') {
        alert('Service Firebase indisponible. Vérifiez votre connexion internet.');
      } else {
        alert(`Erreur lors de la création du projet: ${error.message}`);
      }
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

  const tabs = [
    {
      id: 'tiers',
      name: 'Gestion des tiers',
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
      )
    },
    {
      id: 'anonymizer',
      name: 'Anonymiser',
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
        </svg>
      )
    },
    {
      id: 'ai-chat',
      name: 'Chat IA',
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
        </svg>
      )
    }
  ];

  const renderActiveTab = () => {
    switch (activeTab) {
      case 'tiers':
        return (
          <TiersManagement 
            selectedProject={selectedProject}
            updateProject={updateProject}
            projects={projects}
            setProjects={setProjects}
          />
        );
      case 'anonymizer':
        return (
          <AnonymizationPanel 
            selectedProject={selectedProject}
            projects={projects}
            setProjects={setProjects}
          />
        );
      case 'ai-chat':
        return (
          <AiChatPanel 
            selectedProject={selectedProject}
          />
        );
      default:
        return null;
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
        <div className="w-full px-4 py-4">
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
      <div className="w-full px-4 py-6">
        <div className="flex h-[calc(100vh-200px)] gap-6">
          {/* Sidebar */}
          <div className="w-80 bg-white rounded-lg shadow-sm overflow-hidden">
            <Sidebar
              projects={projects}
              selectedProject={selectedProject}
              setSelectedProject={setSelectedProject}
              createProject={createProject}
              deleteProject={deleteProject}
              canCreateProject={() => canCreateProject(projects.length)}
              userPlan={userProfile?.plan || 'FREE'}
              maxProjects={PLANS[userProfile?.plan || 'FREE']?.maxProjects}
            />
          </div>

          {/* Main Panel avec onglets */}
          <div className="flex-1 bg-white rounded-lg shadow-sm overflow-hidden">
            {selectedProject ? (
              <div className="h-full flex flex-col">
                {/* Onglets */}
                <div className="flex border-b bg-gray-50">
                  {tabs.map((tab) => (
                    <button
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id)}
                      className={`flex items-center gap-2 px-6 py-4 text-sm font-medium transition-colors ${
                        activeTab === tab.id
                          ? 'text-blue-600 border-b-2 border-blue-600 bg-white'
                          : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                      }`}
                    >
                      {tab.icon}
                      {tab.name}
                    </button>
                  ))}
                </div>

                {/* Contenu de l'onglet actif */}
                <div className="flex-1 overflow-hidden">
                  {renderActiveTab()}
                </div>
              </div>
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
                    Créez un nouveau projet ou sélectionnez un projet existant pour commencer.
                  </p>
                  {canCreateProject(projects.length) && (
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