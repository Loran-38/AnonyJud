import React, { useState, useEffect, useRef } from 'react';
import TiersForm from './TiersForm';
import config from '../config';

/**
 * Zone principale de l'application : affichage du projet sélectionné, gestion des tiers,
 * anonymisation et désanonymisation.
 */
const MainPanel = ({ selectedProject, updateProject, projects, setProjects }) => {
  const [inputText, setInputText] = useState('');
  const [anonymizedText, setAnonymizedText] = useState('');
  const [mapping, setMapping] = useState({});
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState('');
  const [dragActive, setDragActive] = useState(false);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [uploadedFileName, setUploadedFileName] = useState('');
  const fileInputRef = useRef(null);

  // Réinitialiser les champs lorsque le projet sélectionné change
  useEffect(() => {
    setInputText('');
    setAnonymizedText('');
    setMapping({});
    setError('');
    setUploadedFile(null);
    setUploadedFileName('');
  }, [selectedProject]);

  // Fonction pour anonymiser le texte
  const anonymizeText = async () => {
    if (!inputText.trim()) {
      setError('Veuillez entrer du texte à anonymiser.');
      return;
    }

    if (!selectedProject) {
      setError('Veuillez sélectionner un projet.');
      return;
    }

    setError('');
    setIsProcessing(true);

    try {
      // Afficher les tiers pour le débogage
      console.log("Tiers envoyés pour anonymisation:", selectedProject.tiers);
      console.log("URL utilisée pour l'API:", `${config.API_BASE_URL}/anonymize/text`);
      console.log("Configuration complète:", config);
      
      const response = await fetch(`${config.API_BASE_URL}/anonymize/text`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: inputText,
          tiers: selectedProject.tiers || []
        }),
      });

      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`);
      }

      const data = await response.json();
      setAnonymizedText(data.anonymized_text);
      setMapping(data.mapping);
      
      // Afficher le mapping pour le débogage
      console.log("Mapping reçu après anonymisation:", data.mapping);
    } catch (err) {
      setError(`Erreur lors de l'anonymisation: ${err.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  // Fonction pour gérer le glisser-déposer
  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  // Fonction pour gérer le dépôt de fichier
  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  // Fonction pour gérer la sélection de fichier via le bouton
  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  // Fonction pour traiter le fichier
  const handleFile = async (file) => {
    if (!selectedProject) {
      setError('Veuillez sélectionner un projet.');
      return;
    }

    // Vérifier le type de fichier
    const fileType = file.name.split('.').pop().toLowerCase();
    if (fileType !== 'pdf' && fileType !== 'doc' && fileType !== 'docx' && fileType !== 'odt') {
      setError('Format de fichier non supporté. Utilisez PDF, DOCX ou ODT.');
      return;
    }

    setError('');
    setIsProcessing(true);

    try {
      // Sauvegarder le fichier uploadé pour les téléchargements futurs
      setUploadedFile(file);
      setUploadedFileName(file.name);
      
      // Afficher les tiers pour le débogage
      console.log("Tiers envoyés pour anonymisation de fichier:", selectedProject.tiers);
      
      const formData = new FormData();
      formData.append('file', file);
      formData.append('tiers_json', JSON.stringify(selectedProject.tiers || []));

      const response = await fetch(`${config.API_BASE_URL}/anonymize/file`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`);
      }

      const data = await response.json();
      setAnonymizedText(data.text);
      setMapping(data.mapping);
      
      // Afficher le mapping pour le débogage
      console.log("Mapping reçu après anonymisation de fichier:", data.mapping);
    } catch (err) {
      setError(`Erreur lors du traitement du fichier: ${err.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  // Fonction pour déclencher le clic sur l'input de fichier
  const onButtonClick = () => {
    fileInputRef.current.click();
  };

  // Fonction pour télécharger le fichier anonymisé
  const downloadAnonymizedFile = async () => {
    if (!uploadedFile || !selectedProject) {
      setError('Aucun fichier à télécharger.');
      return;
    }

    // Vérifier que c'est un fichier Word
    const fileType = uploadedFile.name.split('.').pop().toLowerCase();
    if (fileType !== 'docx') {
      setError('Le téléchargement de fichiers anonymisés n\'est disponible que pour les fichiers Word (.docx).');
      return;
    }

    setError('');
    setIsProcessing(true);

    try {
      const formData = new FormData();
      formData.append('file', uploadedFile);
      formData.append('tiers_json', JSON.stringify(selectedProject.tiers || []));

      const response = await fetch(`${config.API_BASE_URL}/anonymize/file/download`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`);
      }

      // Télécharger le fichier
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = uploadedFileName.replace('.docx', '_anonymise.docx');
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError(`Erreur lors du téléchargement: ${err.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  // Fonction pour télécharger le fichier dé-anonymisé
  const downloadDeanonymizedFile = async () => {
    if (!uploadedFile || !mapping || Object.keys(mapping).length === 0) {
      setError('Aucun fichier anonymisé à dé-anonymiser.');
      return;
    }

    // Vérifier que c'est un fichier Word
    const fileType = uploadedFile.name.split('.').pop().toLowerCase();
    if (fileType !== 'docx') {
      setError('Le téléchargement de fichiers dé-anonymisés n\'est disponible que pour les fichiers Word (.docx).');
      return;
    }

    setError('');
    setIsProcessing(true);

    try {
      const formData = new FormData();
      formData.append('file', uploadedFile);
      formData.append('mapping_json', JSON.stringify(mapping));

      const response = await fetch(`${config.API_BASE_URL}/deanonymize/file/download`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`);
      }

      // Télécharger le fichier
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = uploadedFileName.replace('.docx', '_deanonymise.docx');
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError(`Erreur lors du téléchargement: ${err.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  // Fonction pour dé-anonymiser le texte
  const deanonymizeText = async () => {
    if (!anonymizedText.trim()) {
      setError('Pas de texte anonymisé à dé-anonymiser.');
      return;
    }

    // Afficher le mapping pour débogage
    console.log("Mapping utilisé pour la dé-anonymisation:", mapping);

    setError('');
    setIsProcessing(true);

    try {
      const response = await fetch(`${config.API_BASE_URL}/deanonymize/text`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          anonymized_text: anonymizedText,
          mapping: mapping
        }),
      });

      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`);
      }

      const data = await response.json();
      console.log("Réponse de dé-anonymisation:", data);
      setInputText(data.deanonymized_text);
    } catch (err) {
      setError(`Erreur lors de la dé-anonymisation: ${err.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="flex flex-col h-full w-full bg-white p-6 overflow-hidden">
      {selectedProject ? (
        <>
          <h2 className="text-2xl font-bold mb-6 text-gray-800 border-b pb-2">
            Projet: {selectedProject.nom}
          </h2>
          
          <div className="flex flex-col lg:flex-row h-full gap-6">
            {/* Partie des tiers - Maintenant 50% de la largeur */}
            <div className="w-full lg:w-1/2 overflow-auto bg-gray-50 rounded-lg shadow-sm p-4">
              <h3 className="text-lg font-semibold mb-4 text-gray-700">Gestion des tiers</h3>
              <TiersForm 
                projectId={selectedProject.id} 
                tiers={selectedProject.tiers || []} 
                updateProject={updateProject}
                projects={projects}
                setProjects={setProjects}
              />
            </div>
            
            {/* Partie anonymisation - Maintenant 50% de la largeur */}
            <div className="w-full lg:w-1/2 flex flex-col h-full">
              {/* Texte original */}
              <div className="flex flex-col h-1/2 mb-4">
                <div className="flex justify-between items-center mb-3 bg-gray-50 p-3 rounded-t-lg">
                  <h3 className="font-semibold text-gray-700">Texte original</h3>
                  <div className="flex space-x-2">
                    <button
                      onClick={anonymizeText}
                      disabled={isProcessing}
                      className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors duration-150 disabled:opacity-50 flex items-center"
                    >
                      {isProcessing ? (
                        <>
                          <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                          </svg>
                          Traitement...
                        </>
                      ) : (
                        'Anonymiser'
                      )}
                    </button>
                    <button
                      onClick={() => setInputText('')}
                      className="bg-gray-200 hover:bg-gray-300 text-gray-700 px-4 py-2 rounded-md text-sm font-medium transition-colors duration-150"
                    >
                      Effacer
                    </button>
                  </div>
                </div>
                <textarea
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  placeholder="Entrez ici le texte à anonymiser..."
                  className="flex-1 p-4 border border-gray-200 rounded-b-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              
              {/* Zone de glisser-déposer */}
              <div 
                className={`border-2 border-dashed rounded-lg p-6 mb-4 text-center cursor-pointer transition-colors duration-200 ${
                  dragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-blue-400 hover:bg-gray-50'
                }`}
                onDragEnter={handleDrag}
                onDragOver={handleDrag}
                onDragLeave={handleDrag}
                onDrop={handleDrop}
                onClick={onButtonClick}
              >
                <input 
                  ref={fileInputRef}
                  type="file" 
                  accept=".pdf,.doc,.docx,.odt"
                  onChange={handleFileChange}
                  className="hidden" 
                />
                <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 mx-auto text-gray-400 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
                <p className="text-gray-500">
                  Glissez-déposez un fichier PDF, Word ou ODT ici, ou cliquez pour sélectionner un fichier
                </p>
                {uploadedFileName && (
                  <div className="mt-3 p-3 bg-blue-50 rounded-lg">
                    <p className="text-sm text-blue-800 font-medium">
                      📄 {uploadedFileName}
                    </p>
                  </div>
                )}
              </div>

              {/* Section téléchargement de fichiers */}
              {uploadedFile && uploadedFile.name.endsWith('.docx') && (
                <div className="mb-4 p-4 bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg border border-green-200 shadow-sm">
                  <h4 className="text-sm font-semibold text-green-800 mb-3 flex items-center">
                    <svg className="w-5 h-5 mr-2 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    Téléchargement de fichiers Word
                  </h4>
                  <div className="flex flex-col sm:flex-row gap-3">
                    <button
                      onClick={downloadAnonymizedFile}
                      disabled={isProcessing || !selectedProject?.tiers?.length}
                      className="flex-1 bg-blue-600 hover:bg-blue-700 text-white px-4 py-3 rounded-lg text-sm font-medium transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center shadow-sm hover:shadow-md transform hover:scale-105"
                    >
                      <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                      Télécharger fichier anonymisé
                    </button>
                    <button
                      onClick={downloadDeanonymizedFile}
                      disabled={isProcessing || !mapping || Object.keys(mapping).length === 0}
                      className="flex-1 bg-green-600 hover:bg-green-700 text-white px-4 py-3 rounded-lg text-sm font-medium transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center shadow-sm hover:shadow-md transform hover:scale-105"
                    >
                      <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                      Télécharger fichier dé-anonymisé
                    </button>
                  </div>
                  <div className="mt-3 p-3 bg-blue-50 rounded-lg border border-blue-200">
                    <p className="text-xs text-blue-700 font-medium flex items-center">
                      <svg className="w-4 h-4 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      Ces boutons téléchargent le fichier Word original avec les modifications appliquées directement dans le document.
                    </p>
                  </div>
                  {!selectedProject?.tiers?.length && (
                    <div className="mt-2 p-2 bg-yellow-50 rounded-lg border border-yellow-200">
                      <p className="text-xs text-yellow-700 font-medium">
                        ⚠️ Ajoutez des tiers pour activer le téléchargement du fichier anonymisé.
                      </p>
                    </div>
                  )}
                  {(!mapping || Object.keys(mapping).length === 0) && (
                    <div className="mt-2 p-2 bg-orange-50 rounded-lg border border-orange-200">
                      <p className="text-xs text-orange-700 font-medium">
                        ⚠️ Effectuez d'abord une anonymisation pour activer le téléchargement dé-anonymisé.
                      </p>
                    </div>
                  )}
                </div>
              )}
              
              {/* Texte anonymisé */}
              <div className="flex flex-col h-1/2">
                <div className="flex justify-between items-center mb-3 bg-gray-50 p-3 rounded-t-lg">
                  <h3 className="font-semibold text-gray-700">Texte anonymisé</h3>
                  <div className="flex space-x-2">
                    <button
                      onClick={deanonymizeText}
                      disabled={isProcessing || !anonymizedText}
                      className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors duration-150 disabled:opacity-50"
                    >
                      Dé-anonymiser
                    </button>
                    <button
                      onClick={() => {
                        setAnonymizedText('');
                        setMapping({});
                      }}
                      className="bg-gray-200 hover:bg-gray-300 text-gray-700 px-4 py-2 rounded-md text-sm font-medium transition-colors duration-150"
                    >
                      Effacer
                    </button>
                  </div>
                </div>
                <textarea
                  value={anonymizedText}
                  onChange={(e) => setAnonymizedText(e.target.value)}
                  placeholder="Le texte anonymisé apparaîtra ici..."
                  className="flex-1 p-4 border border-gray-200 rounded-b-lg resize-none bg-gray-50 focus:outline-none"
                  readOnly
                />
              </div>
              
              {error && (
                <div className="mt-4 p-4 bg-red-50 text-red-700 rounded-lg border border-red-200 flex items-start">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 mt-0.5 flex-shrink-0" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                  </svg>
                  <span>{error}</span>
                </div>
              )}
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