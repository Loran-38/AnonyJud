import React, { useState, useEffect, useRef } from 'react';
import config from '../config';

/**
 * Composant d'anonymisation et de dé-anonymisation avec interface modifiée
 * Zone de saisie en haut et cadre de réponse en dessous pour chaque fonctionnalité
 */
const AnonymizationPanel = ({ selectedProject, updateProject, projects, setProjects }) => {
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
    console.log('[AnonymizationPanel] Projet sélectionné changé:', selectedProject?.nom);
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
    console.log('[AnonymizationPanel] Début anonymisation texte');
    if (!inputText.trim()) {
      setError('Veuillez entrer du texte à anonymiser.');
      console.log('[AnonymizationPanel] Erreur: Texte vide');
      return;
    }

    if (!selectedProject) {
      setError('Veuillez sélectionner un projet.');
      console.log('[AnonymizationPanel] Erreur: Aucun projet sélectionné');
      return;
    }

    setError('');
    setIsProcessing(true);

    try {
      console.log('[AnonymizationPanel] Tiers envoyés pour anonymisation:', selectedProject.tiers);
      console.log('[AnonymizationPanel] URL API:', `${config.API_BASE_URL}/anonymize/text`);
      
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
      console.log('[AnonymizationPanel] Réponse anonymisation:', data);
      setAnonymizedText(data.anonymized_text);
      setMapping(data.mapping);
      
      console.log('[AnonymizationPanel] Mapping reçu:', data.mapping);
    } catch (err) {
      console.error('[AnonymizationPanel] Erreur anonymisation:', err);
      setError(`Erreur lors de l'anonymisation: ${err.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  // Fonction pour dé-anonymiser le texte
  const deanonymizeText = async () => {
    console.log('[AnonymizationPanel] Début dé-anonymisation texte');
    if (!deanonymizedInputText.trim()) {
      setError('Veuillez entrer du texte à dé-anonymiser.');
      console.log('[AnonymizationPanel] Erreur: Texte dé-anonymisation vide');
      return;
    }

    if (!selectedProject) {
      setError('Veuillez sélectionner un projet.');
      console.log('[AnonymizationPanel] Erreur: Aucun projet sélectionné pour dé-anonymisation');
      return;
    }

    setError('');
    setIsProcessing(true);

    try {
      console.log('[AnonymizationPanel] Envoi requête dé-anonymisation avec tiers:', selectedProject.tiers);
      console.log('[AnonymizationPanel] Texte à dé-anonymiser:', deanonymizedInputText);
      
      const response = await fetch(`${config.API_BASE_URL}/deanonymize/text`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          anonymized_text: deanonymizedInputText,
          tiers_json: selectedProject.tiers || [],
          has_mapping: Object.keys(mapping).length > 0,
          mapping: mapping
        }),
      });

      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`);
      }

      const data = await response.json();
      console.log('[AnonymizationPanel] Réponse dé-anonymisation:', data);
      setDeanonymizedText(data.deanonymized_text);
    } catch (err) {
      console.error('[AnonymizationPanel] Erreur dé-anonymisation:', err);
      setError(`Erreur lors de la dé-anonymisation: ${err.message}`);
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
    console.log('[AnonymizationPanel] Traitement fichier anonymisation:', file.name);
    if (!selectedProject) {
      setError('Veuillez sélectionner un projet.');
      console.log('[AnonymizationPanel] Erreur: Aucun projet pour traitement fichier');
      return;
    }

    // Vérifier le type de fichier
    const fileType = file.name.split('.').pop().toLowerCase();
    if (fileType !== 'pdf' && fileType !== 'doc' && fileType !== 'docx' && fileType !== 'odt') {
      setError('Format de fichier non supporté. Utilisez PDF, DOCX ou ODT.');
      console.log('[AnonymizationPanel] Erreur: Format fichier non supporté:', fileType);
      return;
    }

    setError('');
    setIsProcessing(true);
    setFileProgress(0);
    setIsFileReady(false);

    try {
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
      
      console.log('[AnonymizationPanel] Fichier uploadé:', file.name, 'Type:', file.type);
      console.log('[AnonymizationPanel] Tiers envoyés pour anonymisation fichier:', selectedProject.tiers);
      
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
      console.log('[AnonymizationPanel] Réponse anonymisation fichier:', data);
      setAnonymizedText(data.text);
      setMapping(data.mapping);
      setProcessedFile(file);
      
      clearInterval(progressInterval);
      setFileProgress(100);
      setIsFileReady(true);
    } catch (err) {
      console.error('[AnonymizationPanel] Erreur traitement fichier:', err);
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
    console.log('[AnonymizationPanel] Traitement fichier dé-anonymisation:', file.name);
    if (!selectedProject) {
      setError('Veuillez sélectionner un projet.');
      console.log('[AnonymizationPanel] Erreur: Aucun projet pour dé-anonymisation fichier');
      return;
    }

    const fileType = file.name.split('.').pop().toLowerCase();
    if (fileType !== 'pdf' && fileType !== 'doc' && fileType !== 'docx' && fileType !== 'odt') {
      setError('Format de fichier non supporté. Utilisez PDF, DOCX ou ODT.');
      console.log('[AnonymizationPanel] Erreur: Format fichier dé-anonymisation non supporté:', fileType);
      return;
    }

    setError('');
    setIsProcessing(true);
    setFileProgressDeanon(0);
    setIsFileReadyDeanon(false);

    try {
      setUploadedFileDeanon(file);
      setUploadedFileNameDeanon(file.name);
      
      const progressInterval = setInterval(() => {
        setFileProgressDeanon(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return prev;
          }
          return prev + 10;
        });
      }, 200);
      
      console.log('[AnonymizationPanel] Fichier dé-anonymisation uploadé:', file.name);
      console.log('[AnonymizationPanel] Tiers disponibles:', selectedProject.tiers);
      console.log('[AnonymizationPanel] Mapping disponible:', mapping);
      
      const formData = new FormData();
      formData.append('file', file);
      formData.append('tiers_json', JSON.stringify(selectedProject.tiers || []));
      formData.append('has_mapping', Object.keys(mapping).length > 0 ? 'true' : 'false');
      
      if (Object.keys(mapping).length > 0) {
        formData.append('mapping', JSON.stringify(mapping));
      }

      const response = await fetch(`${config.API_BASE_URL}/deanonymize/file`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`);
      }

      const data = await response.json();
      console.log('[AnonymizationPanel] Réponse dé-anonymisation fichier:', data);
      setDeanonymizedText(data.text);
      setProcessedFileDeanon(file);
      
      clearInterval(progressInterval);
      setFileProgressDeanon(100);
      setIsFileReadyDeanon(true);
    } catch (err) {
      console.error('[AnonymizationPanel] Erreur dé-anonymisation fichier:', err);
      setError(`Erreur lors du traitement du fichier: ${err.message}`);
      setFileProgressDeanon(0);
      setIsFileReadyDeanon(false);
    } finally {
      setIsProcessing(false);
    }
  };

  const onButtonClick = () => {
    fileInputRef.current?.click();
  };

  const onButtonClickDeanon = () => {
    fileInputDenonRef.current?.click();
  };

  const downloadAnonymizedFile = async () => {
    if (!processedFile) return;
    
    console.log('[AnonymizationPanel] Téléchargement fichier anonymisé');
    setIsProcessing(true);
    
    try {
      const formData = new FormData();
      formData.append('file', processedFile);
      formData.append('tiers_json', JSON.stringify(selectedProject.tiers || []));

      const response = await fetch(`${config.API_BASE_URL}/anonymize/file`, {
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
      let filename = uploadedFileName.replace(/\.([^.]+)$/, '_ANONYM.$1');
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
      console.log('[AnonymizationPanel] Fichier anonymisé téléchargé:', filename);
    } catch (err) {
      console.error('[AnonymizationPanel] Erreur téléchargement:', err);
      setError(`Erreur lors du téléchargement: ${err.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  const downloadDeanonymizedFile = async () => {
    if (!processedFileDeanon) return;
    
    console.log('[AnonymizationPanel] Téléchargement fichier dé-anonymisé');
    setIsProcessing(true);
    
    try {
      const formData = new FormData();
      formData.append('file', processedFileDeanon);
      formData.append('tiers_json', JSON.stringify(selectedProject.tiers || []));
      formData.append('has_mapping', Object.keys(mapping).length > 0 ? 'true' : 'false');
      
      if (Object.keys(mapping).length > 0) {
        formData.append('mapping', JSON.stringify(mapping));
      }

      const response = await fetch(`${config.API_BASE_URL}/deanonymize/file`, {
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
      let filename = uploadedFileNameDeanon.replace(/\.([^.]+)$/, '_DESANONYM.$1');
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
      console.log('[AnonymizationPanel] Fichier dé-anonymisé téléchargé:', filename);
    } catch (err) {
      console.error('[AnonymizationPanel] Erreur téléchargement dé-anonymisation:', err);
      setError(`Erreur lors du téléchargement: ${err.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="flex flex-col h-full w-full bg-white">
      <div className="flex flex-col lg:flex-row h-full gap-4">
        
        {/* Colonne ANONYMISER */}
        <div className="w-full lg:w-1/2 flex flex-col bg-blue-50 rounded-lg p-4 border-2 border-blue-200">
          <div className="text-center mb-4">
            <h3 className="text-lg font-bold text-blue-800 bg-blue-100 rounded-full px-4 py-2 inline-block">
              🔒 ANONYMISER
            </h3>
          </div>
          
          {/* Zone de glisser-déposer pour anonymisation */}
          <div 
            className={`border-2 border-dashed rounded-lg p-6 mb-4 text-center cursor-pointer transition-colors duration-200 ${
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
            <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 mx-auto text-blue-500 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
            <p className="text-blue-700 text-sm font-medium">
              Glisser-déposer votre fichier ici
            </p>
            <p className="text-blue-600 text-xs">
              ou cliquer pour sélectionner
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
            className={`w-full mb-4 px-4 py-3 rounded-lg text-sm font-medium transition-all duration-200 ${
              isFileReady && !isProcessing
                ? 'bg-green-600 hover:bg-green-700 text-white shadow-md hover:shadow-lg'
                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            }`}
          >
            {isFileReady ? '📥 TÉLÉCHARGER' : 'Télécharger (en attente)'}
          </button>
          
          {/* Titre pour anonymisation texte */}
          <h4 className="text-lg font-semibold text-blue-800 mb-3 text-center border-b border-blue-300 pb-2">
            ANONYMISER LES DOCUMENTS
          </h4>
          
          {/* Zone de saisie pour anonymisation */}
          <div className="mb-4">
            <div className="flex justify-between items-center mb-2">
              <label className="text-sm font-semibold text-blue-800">
                Ou saisissez votre texte directement :
              </label>
              <span className="text-xs text-blue-600">
                {inputText.length} caractères
              </span>
            </div>
            <textarea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="HUISSOUD

DANS CETTE FENÊTRE SE TROUVE LE TEXTE ANONYMISÉ"
              className="w-full h-32 p-3 border border-blue-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white text-sm"
            />
            <button
              onClick={anonymizeText}
              disabled={isProcessing || !inputText.trim()}
              className={`w-full mt-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                !isProcessing && inputText.trim()
                  ? 'bg-blue-600 hover:bg-blue-700 text-white'
                  : 'bg-gray-300 text-gray-500 cursor-not-allowed'
              }`}
            >
              {isProcessing ? '⏳ Traitement...' : '🔒 ANONYMISER'}
            </button>
          </div>
          
          {/* Cadre de réponse pour anonymisation */}
          <div className="flex-1 flex flex-col">
            <div className="flex justify-between items-center mb-2">
              <label className="text-sm font-semibold text-blue-800">
                Texte anonymisé :
              </label>
              <span className="text-xs text-blue-600">
                {anonymizedText.length} caractères
              </span>
            </div>
            <div className="flex-1 p-3 border-2 border-blue-300 rounded-lg bg-blue-50 text-sm overflow-auto">
              {anonymizedText ? (
                <div className="whitespace-pre-wrap text-blue-900 font-mono">
                  {anonymizedText}
                </div>
              ) : (
                <div className="text-blue-500 italic text-center py-8">
                  Le texte anonymisé apparaîtra ici...
                  <br />
                  <span className="text-xs">Utilisez la zone de saisie ci-dessus ou glissez un fichier</span>
                </div>
              )}
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
            <h3 className="text-lg font-bold text-green-800 bg-green-100 rounded-full px-4 py-2 inline-block">
              🔓 DÉ-ANONYMISER
            </h3>
          </div>
          
          {/* Zone de glisser-déposer pour dé-anonymisation */}
          <div 
            className={`border-2 border-dashed rounded-lg p-6 mb-4 text-center cursor-pointer transition-colors duration-200 ${
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
            <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 mx-auto text-green-500 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
            <p className="text-green-700 text-sm font-medium">
              Glisser-déposer votre fichier ici
            </p>
            <p className="text-green-600 text-xs">
              ou cliquer pour sélectionner
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
            className={`w-full mb-4 px-4 py-3 rounded-lg text-sm font-medium transition-all duration-200 ${
              isFileReadyDeanon && !isProcessing
                ? 'bg-green-600 hover:bg-green-700 text-white shadow-md hover:shadow-lg'
                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            }`}
          >
            {isFileReadyDeanon ? '📥 TÉLÉCHARGER' : 'Télécharger (en attente)'}
          </button>
          
          {/* Titre pour dé-anonymisation texte */}
          <h4 className="text-lg font-semibold text-green-800 mb-3 text-center border-b border-green-300 pb-2">
            DÉ-ANONYMISER LES DOCUMENTS
          </h4>
          
          {/* Zone de saisie pour dé-anonymisation */}
          <div className="mb-4">
            <div className="flex justify-between items-center mb-2">
              <label className="text-sm font-semibold text-green-800">
                Insérez le texte anonymisé :
              </label>
              <span className="text-xs text-green-600">
                {deanonymizedInputText.length} caractères
              </span>
            </div>
            <textarea
              value={deanonymizedInputText}
              onChange={(e) => setDeanonymizedInputText(e.target.value)}
              placeholder="NOM1

DANS CETTE FENÊTRE SE TROUVE LE TEXTE DÉ-ANONYMISÉ"
              className="w-full h-32 p-3 border border-green-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white text-sm"
            />
            <button
              onClick={deanonymizeText}
              disabled={isProcessing || !deanonymizedInputText.trim()}
              className={`w-full mt-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                !isProcessing && deanonymizedInputText.trim()
                  ? 'bg-green-600 hover:bg-green-700 text-white'
                  : 'bg-gray-300 text-gray-500 cursor-not-allowed'
              }`}
            >
              {isProcessing ? '⏳ Traitement...' : '🔓 DÉ-ANONYMISER'}
            </button>
          </div>
          
          {/* Cadre de réponse pour dé-anonymisation */}
          <div className="flex-1 flex flex-col">
            <div className="flex justify-between items-center mb-2">
              <label className="text-sm font-semibold text-green-800">
                Texte dé-anonymisé :
              </label>
              <span className="text-xs text-green-600">
                {deanonymizedText.length} caractères
              </span>
            </div>
            <div className="flex-1 p-3 border-2 border-green-300 rounded-lg bg-green-50 text-sm overflow-auto">
              {deanonymizedText ? (
                <div className="whitespace-pre-wrap text-green-900 font-mono">
                  {deanonymizedText}
                </div>
              ) : (
                <div className="text-green-500 italic text-center py-8">
                  Le texte dé-anonymisé apparaîtra ici...
                  <br />
                  <span className="text-xs">Utilisez la zone de saisie ci-dessus ou glissez un fichier</span>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
      
      {/* Affichage des erreurs */}
      {error && (
        <div className="mt-4 p-4 bg-red-50 text-red-700 rounded-lg border border-red-200 flex items-start">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 mt-0.5 flex-shrink-0" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
          <span>{error}</span>
        </div>
      )}
    </div>
  );
};

export default AnonymizationPanel; 