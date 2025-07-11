import React, { useState, useEffect, useRef } from 'react';
import TiersForm from './TiersForm';
import config from '../config';

/**
 * Zone principale de l'application : affichage du projet sélectionné, gestion des tiers,
 * anonymisation et désanonymisation.
 * Interface refaite avec deux colonnes verticales selon le design demandé.
 */
const MainPanel = ({ selectedProject, updateProject, projects, setProjects }) => {
  const [inputText, setInputText] = useState('');
  const [anonymizedText, setAnonymizedText] = useState('');
  const [deanonymizedInputText, setDeanonymizedInputText] = useState('');
  const [deanonymizedText, setDeanonymizedText] = useState('');
  const [mapping, setMapping] = useState({});
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState('');
  const [dragActive, setDragActive] = useState(false);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [uploadedFileName, setUploadedFileName] = useState('');
  const [processedFile, setProcessedFile] = useState(null);
  const [fileProgress, setFileProgress] = useState(0);
  const [isFileReady, setIsFileReady] = useState(false);
  
  // États pour la dé-anonymisation
  const [dragActiveDeanon, setDragActiveDeanon] = useState(false);
  const [uploadedFileDeanon, setUploadedFileDeanon] = useState(null);
  const [uploadedFileNameDeanon, setUploadedFileNameDeanon] = useState('');
  const [processedFileDeanon, setProcessedFileDeanon] = useState(null);
  const [fileProgressDeanon, setFileProgressDeanon] = useState(0);
  const [isFileReadyDeanon, setIsFileReadyDeanon] = useState(false);
  
  const fileInputRef = useRef(null);
  const fileInputDenonRef = useRef(null);

  // Réinitialiser les champs lorsque le projet sélectionné change
  useEffect(() => {
    setInputText('');
    setAnonymizedText('');
    setDeanonymizedInputText('');
    setDeanonymizedText('');
    setMapping({});
    setError('');
    setUploadedFile(null);
    setUploadedFileName('');
    setProcessedFile(null);
    setFileProgress(0);
    setIsFileReady(false);
    setUploadedFileDeanon(null);
    setUploadedFileNameDeanon('');
    setProcessedFileDeanon(null);
    setFileProgressDeanon(0);
    setIsFileReadyDeanon(false);
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
      console.log("=== DÉBUT ANONYMISATION TEXTE ===");
      console.log("Texte à anonymiser:", inputText);
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
        const errorText = await response.text();
        console.error("Erreur de réponse:", response.status, errorText);
        throw new Error(`Erreur HTTP: ${response.status} - ${errorText}`);
      }

      const data = await response.json();
      console.log("Réponse d'anonymisation:", data);
      console.log("Texte anonymisé reçu:", data.anonymized_text);
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

  // Fonction pour gérer le glisser-déposer (anonymisation)
  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  // Fonction pour gérer le dépôt de fichier (anonymisation)
  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  // Fonction pour gérer la sélection de fichier via le bouton (anonymisation)
  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  // Fonction pour traiter le fichier (anonymisation)
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
    setFileProgress(0);
    setIsFileReady(false);

    try {
      // Sauvegarder le fichier uploadé
      setUploadedFile(file);
      setUploadedFileName(file.name);
      
      // Simuler une progression
      const progressInterval = setInterval(() => {
        setFileProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return prev;
          }
          return prev + 10;
        });
      }, 200);
      
      // Debugging pour vérifier l'état du fichier
      console.log("Fichier uploadé:", file.name, "Type:", file.type);
      console.log("Extension détectée:", file.name.split('.').pop().toLowerCase());
      
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
      setProcessedFile(file);
      
      // Finaliser la progression
      clearInterval(progressInterval);
      setFileProgress(100);
      setIsFileReady(true);
      
      // Afficher le mapping pour le débogage
      console.log("Mapping reçu après anonymisation de fichier:", data.mapping);
    } catch (err) {
      setError(`Erreur lors du traitement du fichier: ${err.message}`);
      setFileProgress(0);
      setIsFileReady(false);
    } finally {
      setIsProcessing(false);
    }
  };

  // Fonctions pour la dé-anonymisation
  const handleDragDeanon = (e) => {
    e.preventDefault();
    e.stopPropagation();
    
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActiveDeanon(true);
    } else if (e.type === "dragleave") {
      setDragActiveDeanon(false);
    }
  };

  const handleDropDeanon = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActiveDeanon(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileDeanon(e.dataTransfer.files[0]);
    }
  };

  const handleFileChangeDeanon = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFileDeanon(e.target.files[0]);
    }
  };

  const handleFileDeanon = async (file) => {
    if (!selectedProject) {
      setError('Veuillez sélectionner un projet.');
      return;
    }

    const fileType = file.name.split('.').pop().toLowerCase();
    if (fileType !== 'pdf' && fileType !== 'doc' && fileType !== 'docx' && fileType !== 'odt') {
      setError('Format de fichier non supporté. Utilisez PDF, DOCX ou ODT.');
      return;
    }

    setError('');
    setIsProcessing(true);
    setFileProgressDeanon(0);
    setIsFileReadyDeanon(false);

    try {
      setUploadedFileDeanon(file);
      setUploadedFileNameDeanon(file.name);
      
      // Simuler une progression
      const progressInterval = setInterval(() => {
        setFileProgressDeanon(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return prev;
          }
          return prev + 10;
        });
      }, 200);
      
      const formData = new FormData();
      formData.append('file', file);
      formData.append('tiers_json', JSON.stringify(selectedProject.tiers || []));
      formData.append('has_mapping', 'false');

      const response = await fetch(`${config.API_BASE_URL}/deanonymize/file`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`);
      }

      const data = await response.json();
      setDeanonymizedText(data.deanonymized_text);
      setProcessedFileDeanon(file);
      
      clearInterval(progressInterval);
      setFileProgressDeanon(100);
      setIsFileReadyDeanon(true);
    } catch (err) {
      setError(`Erreur lors du traitement du fichier: ${err.message}`);
      setFileProgressDeanon(0);
      setIsFileReadyDeanon(false);
    } finally {
      setIsProcessing(false);
    }
  };

  // Fonction pour déclencher le clic sur l'input de fichier
  const onButtonClick = () => {
    fileInputRef.current.click();
  };

  const onButtonClickDeanon = () => {
    fileInputDenonRef.current.click();
  };

  // Fonction pour télécharger le fichier anonymisé
  const downloadAnonymizedFile = async () => {
    if (!uploadedFile || !selectedProject) {
      setError('Aucun fichier à télécharger.');
      return;
    }

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

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      const contentDisposition = response.headers.get('Content-Disposition');
      let filename = uploadedFileName.replace('.docx', '_ANONYM.docx');
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename=(.+)/);
        if (filenameMatch) {
          filename = filenameMatch[1].replace(/"/g, '');
        }
      }
      a.download = filename;
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
    if (!uploadedFileDeanon || !selectedProject) {
      setError('Aucun fichier à dé-anonymiser.');
      return;
    }

    const fileType = uploadedFileDeanon.name.split('.').pop().toLowerCase();
    if (fileType !== 'docx') {
      setError('Le téléchargement de fichiers dé-anonymisés n\'est disponible que pour les fichiers Word (.docx).');
      return;
    }

    setError('');
    setIsProcessing(true);

    try {
      const formData = new FormData();
      formData.append('file', uploadedFileDeanon);
      formData.append('tiers_json', JSON.stringify(selectedProject.tiers || []));
      formData.append('has_mapping', 'false');

      const response = await fetch(`${config.API_BASE_URL}/deanonymize/file/download`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`);
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      const contentDisposition = response.headers.get('Content-Disposition');
      let filename = uploadedFileNameDeanon.replace('.docx', '_DESANONYM.docx');
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename=(.+)/);
        if (filenameMatch) {
          filename = filenameMatch[1].replace(/"/g, '');
        }
      }
      a.download = filename;
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
    if (!deanonymizedInputText.trim()) {
      setError('Veuillez entrer du texte à dé-anonymiser.');
      return;
    }

    if (!selectedProject) {
      setError('Veuillez sélectionner un projet.');
      return;
    }

    setError('');
    setIsProcessing(true);

    try {
      console.log("=== DÉBUT DÉ-ANONYMISATION TEXTE ===");
      console.log("Texte à dé-anonymiser:", deanonymizedInputText);
      console.log("Tiers du projet:", selectedProject.tiers);
      console.log("Mapping disponible:", mapping);
      console.log("URL utilisée:", `${config.API_BASE_URL}/deanonymize/text/with-tiers`);
      
      const response = await fetch(`${config.API_BASE_URL}/deanonymize/text/with-tiers`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: deanonymizedInputText,
          tiers_json: selectedProject.tiers || [],
          has_mapping: false
        }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error("Erreur de réponse:", response.status, errorText);
        throw new Error(`Erreur HTTP: ${response.status} - ${errorText}`);
      }

      const data = await response.json();
      console.log("Réponse de dé-anonymisation:", data);
      console.log("Texte dé-anonymisé reçu:", data.deanonymized_text);
      setDeanonymizedText(data.deanonymized_text);
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
            Anonymisation et Dé-anonymisation
          </h2>
          <p className="text-sm text-gray-600 mb-4">
            Projet: {selectedProject.nom} • {selectedProject.tiers?.length || 0} tiers configurés
          </p>
          
          <div className="flex flex-col lg:flex-row h-full gap-6">
            {/* Partie des tiers - Maintenant plus petite */}
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
            
            {/* Partie anonymisation - Maintenant plus large avec deux colonnes */}
            <div className="w-full lg:w-2/3 flex flex-col h-full">
              <div className="flex flex-col lg:flex-row h-full gap-4">
                
                {/* Colonne ANONYMISER */}
                <div className="w-full lg:w-1/2 flex flex-col bg-blue-50 rounded-lg p-4 border-2 border-blue-200">
                  <div className="text-center mb-4">
                    <div className="bg-blue-500 text-white rounded-full px-4 py-2 inline-flex items-center">
                      <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                      </svg>
                      ANONYMISER
                    </div>
                  </div>
                  
                  {/* Zone de glisser-déposer pour anonymisation */}
                  <div 
                    className={`border-2 border-dashed rounded-lg p-4 mb-4 text-center cursor-pointer transition-colors duration-200 ${
                      dragActive ? 'border-blue-500 bg-blue-100' : 'border-blue-300 hover:border-blue-400 hover:bg-blue-100'
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
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 mx-auto text-blue-500 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>
                    <p className="text-blue-700 text-sm font-medium">
                      Glissez-déposez votre fichier ici
                    </p>
                    <p className="text-blue-600 text-xs">
                      ou cliquez pour sélectionner
                    </p>
                    <p className="text-blue-500 text-xs mt-1">
                      PDF, DOCX, ODT acceptés
                    </p>
                    {uploadedFileName && (
                      <div className="mt-2 p-2 bg-blue-200 rounded">
                        <p className="text-xs text-blue-800 font-medium">
                          📄 {uploadedFileName}
                        </p>
                      </div>
                    )}
                  </div>
                  
                  {/* Barre de progression */}
                  {isProcessing && fileProgress > 0 && (
                    <div className="mb-4">
                      <div className="bg-blue-200 rounded-full h-2">
                        <div 
                          className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                          style={{ width: `${fileProgress}%` }}
                        ></div>
                      </div>
                      <p className="text-xs text-blue-700 mt-1 text-center">
                        Traitement en cours... {fileProgress}%
                      </p>
                    </div>
                  )}
                  
                  {/* Bouton télécharger */}
                  <button
                    onClick={downloadAnonymizedFile}
                    disabled={!isFileReady || isProcessing}
                    className={`w-full mb-4 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                      isFileReady && !isProcessing
                        ? 'bg-green-600 hover:bg-green-700 text-white shadow-md hover:shadow-lg'
                        : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                    }`}
                  >
                    {isFileReady ? '📥 TÉLÉCHARGER' : 'Télécharger (en attente)'}
                  </button>
                  
                  {/* Titre section texte */}
                  <h4 className="text-sm font-bold text-blue-800 mb-3 text-center uppercase">
                    Anonymiser les documents
                  </h4>
                  
                  {/* Zone de saisie du texte */}
                  <div className="mb-4">
                    <div className="flex justify-between items-center mb-2">
                      <label className="text-sm font-medium text-blue-700">
                        Ou saisissez votre texte directement :
                      </label>
                      <span className="text-xs text-blue-600">
                        {inputText.length} caractères
                      </span>
                    </div>
                    <textarea
                      value={inputText}
                      onChange={(e) => setInputText(e.target.value)}
                      placeholder="HUISSOUD"
                      className="w-full h-24 p-3 border border-blue-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white text-sm"
                    />
                  </div>
                  
                  {/* Bouton anonymiser */}
                  <button
                    onClick={anonymizeText}
                    disabled={isProcessing || !inputText.trim()}
                    className={`w-full mb-4 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                      !isProcessing && inputText.trim()
                        ? 'bg-blue-600 hover:bg-blue-700 text-white shadow-md hover:shadow-lg'
                        : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                    }`}
                  >
                    {isProcessing ? 'Anonymisation...' : 'ANONYMISER'}
                  </button>
                  
                  {/* Zone de réponse */}
                  <div className="flex-1 flex flex-col">
                    <div className="flex justify-between items-center mb-2">
                      <label className="text-sm font-medium text-blue-700">
                        Texte anonymisé :
                      </label>
                      <span className="text-xs text-blue-600">
                        {anonymizedText.length} caractères
                      </span>
                    </div>
                    <div className="flex-1 border-2 border-blue-300 rounded-lg p-3 bg-white min-h-[120px]">
                      <div className="text-sm text-gray-700 whitespace-pre-wrap">
                        {anonymizedText || (
                          <div className="text-center text-gray-400 mt-8">
                            <p>Nom1</p>
                            <p className="text-xs mt-2">Dans cette fenêtre se trouve</p>
                            <p className="text-xs">le texte anonymisé</p>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
                
                {/* Flèches bidirectionnelles */}
                <div className="flex lg:flex-col items-center justify-center py-4 lg:py-0 lg:px-2">
                  <div className="flex lg:flex-col items-center space-x-2 lg:space-x-0 lg:space-y-2">
                    <svg className="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                    </svg>
                    <svg className="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16l-4-4m0 0l4-4m-4 4h18" />
                    </svg>
                  </div>
                </div>
                
                {/* Colonne DÉ-ANONYMISER */}
                <div className="w-full lg:w-1/2 flex flex-col bg-green-50 rounded-lg p-4 border-2 border-green-200">
                  <div className="text-center mb-4">
                    <div className="bg-green-500 text-white rounded-full px-4 py-2 inline-flex items-center">
                      <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 11V7a4 4 0 118 0m-4 8v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2z" />
                      </svg>
                      DÉ-ANONYMISER
                    </div>
                  </div>
                  
                  {/* Zone de glisser-déposer pour dé-anonymisation */}
                  <div 
                    className={`border-2 border-dashed rounded-lg p-4 mb-4 text-center cursor-pointer transition-colors duration-200 ${
                      dragActiveDeanon ? 'border-green-500 bg-green-100' : 'border-green-300 hover:border-green-400 hover:bg-green-100'
                    }`}
                    onDragEnter={handleDragDeanon}
                    onDragOver={handleDragDeanon}
                    onDragLeave={handleDragDeanon}
                    onDrop={handleDropDeanon}
                    onClick={onButtonClickDeanon}
                  >
                    <input 
                      ref={fileInputDenonRef}
                      type="file" 
                      accept=".pdf,.doc,.docx,.odt"
                      onChange={handleFileChangeDeanon}
                      className="hidden" 
                    />
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 mx-auto text-green-500 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>
                    <p className="text-green-700 text-sm font-medium">
                      Glissez-déposez votre fichier ici
                    </p>
                    <p className="text-green-600 text-xs">
                      ou cliquez pour sélectionner
                    </p>
                    <p className="text-green-500 text-xs mt-1">
                      PDF, DOCX, ODT acceptés
                    </p>
                    {uploadedFileNameDeanon && (
                      <div className="mt-2 p-2 bg-green-200 rounded">
                        <p className="text-xs text-green-800 font-medium">
                          📄 {uploadedFileNameDeanon}
                        </p>
                      </div>
                    )}
                  </div>
                  
                  {/* Barre de progression */}
                  {isProcessing && fileProgressDeanon > 0 && (
                    <div className="mb-4">
                      <div className="bg-green-200 rounded-full h-2">
                        <div 
                          className="bg-green-600 h-2 rounded-full transition-all duration-300"
                          style={{ width: `${fileProgressDeanon}%` }}
                        ></div>
                      </div>
                      <p className="text-xs text-green-700 mt-1 text-center">
                        Traitement en cours... {fileProgressDeanon}%
                      </p>
                    </div>
                  )}
                  
                  {/* Bouton télécharger */}
                  <button
                    onClick={downloadDeanonymizedFile}
                    disabled={!isFileReadyDeanon || isProcessing}
                    className={`w-full mb-4 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                      isFileReadyDeanon && !isProcessing
                        ? 'bg-green-600 hover:bg-green-700 text-white shadow-md hover:shadow-lg'
                        : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                    }`}
                  >
                    {isFileReadyDeanon ? '📥 TÉLÉCHARGER' : 'Télécharger (en attente)'}
                  </button>
                  
                  {/* Titre section texte */}
                  <h4 className="text-sm font-bold text-green-800 mb-3 text-center uppercase">
                    Dé-anonymiser les documents
                  </h4>
                  
                  {/* Zone de saisie du texte */}
                  <div className="mb-4">
                    <div className="flex justify-between items-center mb-2">
                      <label className="text-sm font-medium text-green-700">
                        Insérez le texte anonymisé :
                      </label>
                      <span className="text-xs text-green-600">
                        {deanonymizedInputText.length} caractères
                      </span>
                    </div>
                    <textarea
                      value={deanonymizedInputText}
                      onChange={(e) => setDeanonymizedInputText(e.target.value)}
                      placeholder="NOM1"
                      className="w-full h-24 p-3 border border-green-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white text-sm"
                    />
                  </div>
                  
                  {/* Bouton avec flèche */}
                  <div className="flex items-center justify-center mb-4">
                    <div className="flex-1 border-t border-green-300"></div>
                    <button
                      onClick={deanonymizeText}
                      disabled={isProcessing || !deanonymizedInputText.trim()}
                      className={`mx-4 px-6 py-2 rounded-full text-sm font-medium transition-all duration-200 ${
                        !isProcessing && deanonymizedInputText.trim()
                          ? 'bg-green-600 hover:bg-green-700 text-white shadow-md hover:shadow-lg'
                          : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                      }`}
                                         >
                       {isProcessing ? 'Traitement...' : 'DÉ-ANONYMISER'}
                     </button>
                    <div className="flex-1 border-t border-green-300"></div>
                  </div>
                  
                  {/* Zone de réponse */}
                  <div className="flex-1 flex flex-col">
                    <div className="flex justify-between items-center mb-2">
                      <label className="text-sm font-medium text-green-700">
                        Texte dé-anonymisé :
                      </label>
                      <span className="text-xs text-green-600">
                        {deanonymizedText.length} caractères
                      </span>
                    </div>
                    <div className="flex-1 border-2 border-green-300 rounded-lg p-3 bg-white min-h-[120px]">
                      <div className="text-sm text-gray-700 whitespace-pre-wrap">
                        {deanonymizedText || (
                          <div className="text-center text-gray-400 mt-8">
                            <p>HUISSOUD</p>
                            <p className="text-xs mt-2">Dans cette fenêtre</p>
                            <p className="text-xs">se trouve le texte</p>
                            <p className="text-xs">dé-anonymisé</p>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
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