import React, { useState, useRef } from 'react';
import config from '../config';

const AnonymizationPanel = ({ selectedProject, projects, setProjects }) => {
  // États pour l'anonymisation
  const [inputText, setInputText] = useState('');
  const [anonymizedText, setAnonymizedText] = useState('');
  const [mapping, setMapping] = useState({});
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState('');
  const [dragActive, setDragActive] = useState(false);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [processedFile, setProcessedFile] = useState(null);
  const [fileProgress, setFileProgress] = useState(0);
  const [isFileReady, setIsFileReady] = useState(false);
  
  // États pour la dé-anonymisation
  const [dragActiveDeanon, setDragActiveDeanon] = useState(false);
  const [uploadedFileDeanon, setUploadedFileDeanon] = useState(null);
  const [processedFileDeanon, setProcessedFileDeanon] = useState(null);
  const [fileProgressDeanon, setFileProgressDeanon] = useState(0);
  const [isFileReadyDeanon, setIsFileReadyDeanon] = useState(false);
  const [deanonymizedText, setDeanonymizedText] = useState('');
  const [deanonymizationInputText, setDeanonymizationInputText] = useState('');
  
  // États pour les barres de progression de téléchargement
  const [downloadProgress, setDownloadProgress] = useState(0);
  const [isDownloading, setIsDownloading] = useState(false);
  const [downloadProgressDeanon, setDownloadProgressDeanon] = useState(0);
  const [isDownloadingDeanon, setIsDownloadingDeanon] = useState(false);
  
  const fileInputRef = useRef(null);
  const fileInputDenonRef = useRef(null);

  // Fonction pour obtenir l'icône selon le type de fichier
  const getFileIcon = (fileName) => {
    const extension = fileName.split('.').pop().toLowerCase();
    
    switch (extension) {
      case 'pdf':
        return (
          <svg className="w-8 h-8 text-red-500" fill="currentColor" viewBox="0 0 24 24">
            <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z" />
          </svg>
        );
      case 'doc':
      case 'docx':
        return (
          <svg className="w-8 h-8 text-blue-500" fill="currentColor" viewBox="0 0 24 24">
            <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z" />
          </svg>
        );
      case 'odt':
        return (
          <svg className="w-8 h-8 text-orange-500" fill="currentColor" viewBox="0 0 24 24">
            <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z" />
          </svg>
        );
      default:
        return (
          <svg className="w-8 h-8 text-gray-500" fill="currentColor" viewBox="0 0 24 24">
            <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z" />
          </svg>
        );
    }
  };

  // Fonction pour obtenir le type de fichier formaté
  const getFileTypeLabel = (fileName) => {
    const extension = fileName.split('.').pop().toLowerCase();
    
    switch (extension) {
      case 'pdf':
        return 'PDF';
      case 'doc':
      case 'docx':
        return 'Word';
      case 'odt':
        return 'ODT';
      default:
        return extension.toUpperCase();
    }
  };

  // Composant pour afficher le fichier uploadé
  const FileDisplayCard = ({ file, onRemove, color = 'blue', isProcessing = false, progress = 0 }) => {
    if (!file) return null;

    const getColorClasses = (colorName) => {
      if (colorName === 'green') {
        return {
          bg: 'bg-green-50',
          border: 'border-green-200',
          text: 'text-green-700',
          badge: 'bg-green-100 text-green-800',
          progressBg: 'bg-green-200',
          progressBar: 'bg-green-600'
        };
      }
      return {
        bg: 'bg-blue-50',
        border: 'border-blue-200',
        text: 'text-blue-700',
        badge: 'bg-blue-100 text-blue-800',
        progressBg: 'bg-blue-200',
        progressBar: 'bg-blue-600'
      };
    };

    const classes = getColorClasses(color);

    return (
      <div className={`${classes.bg} ${classes.border} border rounded-lg p-4 transition-all duration-200`}>
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3 flex-1 min-w-0">
            {getFileIcon(file.name)}
            <div className="flex-1 min-w-0">
              <p className={`text-sm font-medium ${classes.text} truncate`}>
                {file.name}
              </p>
              <div className="flex items-center space-x-2 mt-1">
                <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${classes.badge}`}>
                  {getFileTypeLabel(file.name)}
                </span>
                <span className="text-xs text-gray-500">
                  {(file.size / 1024).toFixed(1)} KB
                </span>
              </div>
            </div>
          </div>
          
          {!isProcessing && (
            <button
              onClick={onRemove}
              className="ml-2 p-1 hover:bg-red-100 rounded-full transition-colors group"
              title="Supprimer le fichier"
            >
              <svg className="w-5 h-5 text-gray-400 group-hover:text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          )}
        </div>
        
        {isProcessing && (
          <div className="mt-3">
            <div className="flex items-center justify-between mb-2">
              <span className={`text-sm font-medium ${classes.text}`}>Traitement en cours...</span>
              <span className={`text-sm ${classes.text}`}>{progress}%</span>
            </div>
            <div className={`w-full ${classes.progressBg} rounded-full h-2`}>
              <div 
                className={`${classes.progressBar} h-2 rounded-full transition-all duration-300`}
                style={{ width: `${progress}%` }}
              ></div>
            </div>
          </div>
        )}
      </div>
    );
  };

  // Fonction pour supprimer le fichier d'anonymisation
  const removeAnonymizationFile = () => {
    setUploadedFile(null);
    setProcessedFile(null);
    setFileProgress(0);
    setIsFileReady(false);
    setAnonymizedText('');
    setMapping({});
    setError('');
    
    // Réinitialiser l'input file
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  // Fonction pour supprimer le fichier de dé-anonymisation
  const removeDeanonymizationFile = () => {
    setUploadedFileDeanon(null);
    setProcessedFileDeanon(null);
    setFileProgressDeanon(0);
    setIsFileReadyDeanon(false);
    setDeanonymizedText('');
    setError('');
    
    // Réinitialiser l'input file
    if (fileInputDenonRef.current) {
      fileInputDenonRef.current.value = '';
    }
  };

  // Fonction pour vider le texte d'anonymisation
  const clearAnonymizationText = () => {
    setInputText('');
    setAnonymizedText('');
    setMapping({});
  };

  // Fonction pour vider le texte de dé-anonymisation
  const clearDeanonymizationText = () => {
    setDeanonymizationInputText('');
    setDeanonymizedText('');
  };

  if (!selectedProject) {
    return (
      <div className="h-full flex items-center justify-center text-center">
        <div>
          <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
          </svg>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Aucun projet sélectionné
          </h3>
          <p className="text-gray-600">
            Sélectionnez un projet pour commencer l'anonymisation.
          </p>
        </div>
      </div>
    );
  }

  // Fonction pour gérer le glisser-déposer (anonymisation)
  const handleDragEnter = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    const files = e.dataTransfer.files;
    if (files && files[0]) {
      handleFile(files[0]);
    }
  };

  const handleFileInput = (e) => {
    const file = e.target.files[0];
    if (file) {
      handleFile(file);
    }
  };

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
      // NE PAS afficher le texte automatiquement - juste stocker pour le téléchargement
      setAnonymizedText(data.text);
      setMapping(data.mapping);
      setProcessedFile(file);
      
      // Finaliser la progression
      clearInterval(progressInterval);
      setFileProgress(100);
      setIsFileReady(true);
      
    } catch (err) {
      setError(`Erreur lors de l'anonymisation: ${err.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

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
      
    } catch (err) {
      setError(`Erreur lors de l'anonymisation: ${err.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  // Télécharger le fichier anonymisé
  const downloadAnonymizedFile = async () => {
    if (!processedFile) return;

    setIsDownloading(true);
    setDownloadProgress(0);
    setError('');

    try {
      // Simuler une progression de téléchargement
      const progressInterval = setInterval(() => {
        setDownloadProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return prev;
          }
          return prev + 15;
        });
      }, 100);

      const formData = new FormData();
      formData.append('file', processedFile);
      formData.append('tiers_json', JSON.stringify(selectedProject.tiers || []));

      const response = await fetch(`${config.API_BASE_URL}/anonymize/file/download`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`);
      }

      const blob = await response.blob();
      
      // Finaliser la progression
      clearInterval(progressInterval);
      setDownloadProgress(100);
      
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `anonymise_${processedFile.name}`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      
      // Réinitialiser après un délai
      setTimeout(() => {
        setDownloadProgress(0);
        setIsDownloading(false);
      }, 1000);
      
    } catch (err) {
      setError(`Erreur lors du téléchargement: ${err.message}`);
      setIsDownloading(false);
      setDownloadProgress(0);
    }
  };

  // Fonctions pour la dé-anonymisation (similaires mais pour la colonne de droite)
  const handleDragEnterDeanon = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActiveDeanon(true);
  };

  const handleDragLeaveDeanon = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActiveDeanon(false);
  };

  const handleDragOverDeanon = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDropDeanon = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActiveDeanon(false);
    
    const files = e.dataTransfer.files;
    if (files && files[0]) {
      handleFileDeanon(files[0]);
    }
  };

  const handleFileInputDeanon = (e) => {
    const file = e.target.files[0];
    if (file) {
      handleFileDeanon(file);
    }
  };

  const handleFileDeanon = async (file) => {
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
      
      // Utiliser le mapping existant s'il y en a un, sinon envoyer les tiers du projet
      // pour que le backend puisse générer le mapping correct
      if (mapping && Object.keys(mapping).length > 0) {
        formData.append('mapping_json', JSON.stringify(mapping));
        formData.append('has_mapping', 'true');
      } else {
        formData.append('mapping_json', JSON.stringify({}));
        formData.append('tiers_json', JSON.stringify(selectedProject.tiers || []));
        formData.append('has_mapping', 'false');
      }

      const response = await fetch(`${config.API_BASE_URL}/deanonymize/file`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`);
      }

      const data = await response.json();
      setDeanonymizedText(data.text);
      setProcessedFileDeanon(file);
      
      // Si on obtient un nouveau mapping du backend, l'utiliser
      if (data.mapping) {
        setMapping(data.mapping);
      }
      
      clearInterval(progressInterval);
      setFileProgressDeanon(100);
      setIsFileReadyDeanon(true);
      
    } catch (err) {
      setError(`Erreur lors de la dé-anonymisation: ${err.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  // Fonction pour dé-anonymiser le texte
  const deanonymizeText = async () => {
    if (!deanonymizationInputText.trim()) {
      setError('Veuillez entrer du texte anonymisé à dé-anonymiser.');
      return;
    }

    if (!mapping || Object.keys(mapping).length === 0) {
      setError('Aucun mapping disponible pour la dé-anonymisation du texte.');
      return;
    }

    setError('');
    setIsProcessing(true);

    try {
      const response = await fetch(`${config.API_BASE_URL}/deanonymize/text`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          anonymized_text: deanonymizationInputText,
          mapping: mapping
        }),
      });

      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`);
      }

      const data = await response.json();
      setDeanonymizedText(data.deanonymized_text);
      
    } catch (err) {
      setError(`Erreur lors de la dé-anonymisation: ${err.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  // Télécharger le fichier dé-anonymisé
  const downloadDeanonymizedFile = async () => {
    if (!processedFileDeanon) return;

    setIsDownloadingDeanon(true);
    setDownloadProgressDeanon(0);
    setError('');

    try {
      // Simuler une progression de téléchargement
      const progressInterval = setInterval(() => {
        setDownloadProgressDeanon(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return prev;
          }
          return prev + 15;
        });
      }, 100);

      const formData = new FormData();
      formData.append('file', processedFileDeanon);
      formData.append('mapping_json', JSON.stringify(mapping));

      const response = await fetch(`${config.API_BASE_URL}/deanonymize/file/download`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`);
      }

      const blob = await response.blob();
      
      // Finaliser la progression
      clearInterval(progressInterval);
      setDownloadProgressDeanon(100);
      
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `deanonymise_${processedFileDeanon.name}`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      
      // Réinitialiser après un délai
      setTimeout(() => {
        setDownloadProgressDeanon(0);
        setIsDownloadingDeanon(false);
      }, 1000);
      
    } catch (err) {
      setError(`Erreur lors du téléchargement: ${err.message}`);
      setIsDownloadingDeanon(false);
      setDownloadProgressDeanon(0);
    }
  };

  return (
    <div className="h-full bg-gray-50">
      <div className="p-6 border-b bg-white shadow-sm">
        <h2 className="text-xl font-semibold text-gray-900">Anonymisation et Dé-anonymisation</h2>
        <p className="text-gray-600 mt-1">
          Projet: {selectedProject.nom} • {selectedProject.tiers?.length || 0} tiers configurés
        </p>
      </div>
      
      <div className="p-6 h-full overflow-hidden">
        <div className="flex gap-6 h-full">
          {/* COLONNE ANONYMISER (Bleue) */}
          <div className="flex-1 bg-white rounded-lg shadow-sm border border-blue-200 overflow-hidden">
            <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white p-4">
              <h3 className="text-lg font-semibold flex items-center">
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
                ANONYMISER
              </h3>
            </div>
            
            <div className="p-4 space-y-4 h-full overflow-y-auto">
              {/* Zone de glisser-déposer ou affichage du fichier */}
              {uploadedFile ? (
                <FileDisplayCard
                  file={uploadedFile}
                  onRemove={removeAnonymizationFile}
                  color="blue"
                  isProcessing={isProcessing}
                  progress={fileProgress}
                />
              ) : (
                <div
                  className={`border-2 border-dashed rounded-lg p-6 text-center transition-all duration-200 ${
                    dragActive
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-blue-300 hover:border-blue-400 hover:bg-blue-50'
                  }`}
                  onDragEnter={handleDragEnter}
                  onDragLeave={handleDragLeave}
                  onDragOver={handleDragOver}
                  onDrop={handleDrop}
                  onClick={() => fileInputRef.current?.click()}
                >
                  <svg className="mx-auto h-12 w-12 text-blue-400 mb-4" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                    <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                  <p className="text-blue-600 font-medium">Glissez-déposez votre fichier ici</p>
                  <p className="text-blue-500 text-sm mt-1">ou cliquez pour sélectionner</p>
                  <p className="text-blue-400 text-xs mt-2">PDF, DOCX, ODT acceptés</p>
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept=".pdf,.doc,.docx,.odt"
                    onChange={handleFileInput}
                    className="hidden"
                  />
                </div>
              )}

              {/* Barre de progression téléchargement */}
              {isDownloading && (
                <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-green-700">Téléchargement en cours...</span>
                    <span className="text-sm text-green-600">{downloadProgress}%</span>
                  </div>
                  <div className="w-full bg-green-200 rounded-full h-2">
                    <div 
                      className="bg-green-600 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${downloadProgress}%` }}
                    ></div>
                  </div>
                </div>
              )}

              {/* Bouton de téléchargement */}
              <button
                onClick={downloadAnonymizedFile}
                disabled={!isFileReady || isProcessing || isDownloading}
                className={`w-full py-3 px-4 rounded-lg font-medium transition-all duration-200 ${
                  isFileReady && !isProcessing && !isDownloading
                    ? 'bg-green-600 hover:bg-green-700 text-white cursor-pointer'
                    : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                }`}
              >
                {isDownloading ? (
                  <>
                    <svg className="w-5 h-5 inline mr-2 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                    TÉLÉCHARGEMENT...
                  </>
                ) : isFileReady && !isProcessing ? (
                  <>
                    <svg className="w-5 h-5 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    TÉLÉCHARGER
                  </>
                ) : (
                  'TÉLÉCHARGER'
                )}
              </button>

              {/* Zone de texte */}
              <div className="border-t border-blue-200 pt-4">
                <div className="flex justify-between items-center mb-2">
                  <label className="block text-sm font-medium text-blue-700">
                    Ou saisissez votre texte directement :
                  </label>
                  {inputText && (
                    <button
                      onClick={clearAnonymizationText}
                      className="p-1 text-red-500 hover:text-red-700 rounded-full transition-colors"
                      title="Supprimer le texte"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  )}
                </div>
                <textarea
                  id="Text-AREA-Anonimisation"
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  placeholder="Tapez ou collez votre texte ici..."
                  className="w-full h-32 px-3 py-2 border border-blue-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none"
                />
                <div className="flex justify-between items-center mt-2">
                  <span className="text-xs text-blue-600">
                    {inputText.length} caractères
                  </span>
                  <button
                    onClick={anonymizeText}
                    disabled={!inputText.trim() || isProcessing}
                    className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white px-4 py-2 rounded-md transition-colors text-sm"
                  >
                    {isProcessing ? 'Traitement...' : 'Anonymiser'}
                  </button>
                </div>
              </div>

              {/* Résultat de l'anonymisation de texte */}
              {anonymizedText && (
                <div className="border-t border-blue-200 pt-4">
                  <div className="flex justify-between items-center mb-2">
                    <label className="block text-sm font-medium text-blue-700">
                      Texte anonymisé :
                    </label>
                    <button
                      onClick={() => setAnonymizedText('')}
                      className="p-1 text-red-500 hover:text-red-700 rounded-full transition-colors"
                      title="Supprimer le texte anonymisé"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </div>
                  <textarea
                    id="Text-AREA-Anonimisation-result"
                    value={anonymizedText}
                    onChange={(e) => setAnonymizedText(e.target.value)}
                    className="w-full h-32 px-3 py-2 border border-blue-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none bg-blue-50"
                  />
                </div>
              )}
            </div>
          </div>

          {/* COLONNE DÉ-ANONYMISER (Verte) */}
          <div className="flex-1 bg-white rounded-lg shadow-sm border border-green-200 overflow-hidden">
            <div className="bg-gradient-to-r from-green-600 to-green-700 text-white p-4">
              <h3 className="text-lg font-semibold flex items-center">
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 7a2 2 0 012 2m0 0a2 2 0 012 2m-2-2a2 2 0 00-2 2m2-2V5a2 2 0 00-2-2m-2 0H9m0 0v2m0 0V5a2 2 0 012-2m0 0h2" />
                </svg>
                DÉ-ANONYMISER
              </h3>
            </div>
            
            <div className="p-4 space-y-4 h-full overflow-y-auto">
              {/* Zone de glisser-déposer ou affichage du fichier */}
              {uploadedFileDeanon ? (
                <FileDisplayCard
                  file={uploadedFileDeanon}
                  onRemove={removeDeanonymizationFile}
                  color="green"
                  isProcessing={isProcessing}
                  progress={fileProgressDeanon}
                />
              ) : (
                <div
                  className={`border-2 border-dashed rounded-lg p-6 text-center transition-all duration-200 ${
                    dragActiveDeanon
                      ? 'border-green-500 bg-green-50'
                      : 'border-green-300 hover:border-green-400 hover:bg-green-50'
                  }`}
                  onDragEnter={handleDragEnterDeanon}
                  onDragLeave={handleDragLeaveDeanon}
                  onDragOver={handleDragOverDeanon}
                  onDrop={handleDropDeanon}
                  onClick={() => fileInputDenonRef.current?.click()}
                >
                  <svg className="mx-auto h-12 w-12 text-green-400 mb-4" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                    <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                  <p className="text-green-600 font-medium">Glissez-déposez votre fichier ici</p>
                  <p className="text-green-500 text-sm mt-1">ou cliquez pour sélectionner</p>
                  <p className="text-green-400 text-xs mt-2">PDF, DOCX, ODT acceptés</p>
                  <input
                    ref={fileInputDenonRef}
                    type="file"
                    accept=".pdf,.doc,.docx,.odt"
                    onChange={handleFileInputDeanon}
                    className="hidden"
                  />
                </div>
              )}

              {/* Barre de progression téléchargement */}
              {isDownloadingDeanon && (
                <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-green-700">Téléchargement en cours...</span>
                    <span className="text-sm text-green-600">{downloadProgressDeanon}%</span>
                  </div>
                  <div className="w-full bg-green-200 rounded-full h-2">
                    <div 
                      className="bg-green-600 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${downloadProgressDeanon}%` }}
                    ></div>
                  </div>
                </div>
              )}

              {/* Bouton de téléchargement */}
              <button
                onClick={downloadDeanonymizedFile}
                disabled={!isFileReadyDeanon || isProcessing || isDownloadingDeanon}
                className={`w-full py-3 px-4 rounded-lg font-medium transition-all duration-200 ${
                  isFileReadyDeanon && !isProcessing && !isDownloadingDeanon
                    ? 'bg-green-600 hover:bg-green-700 text-white cursor-pointer'
                    : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                }`}
              >
                {isDownloadingDeanon ? (
                  <>
                    <svg className="w-5 h-5 inline mr-2 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                    TÉLÉCHARGEMENT...
                  </>
                ) : isFileReadyDeanon && !isProcessing ? (
                  <>
                    <svg className="w-5 h-5 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    TÉLÉCHARGER
                  </>
                ) : (
                  'TÉLÉCHARGER'
                )}
              </button>

              {/* Zone de texte pour la désanonymisation */}
              <div className="border-t border-green-200 pt-4">
                <div className="flex justify-between items-center mb-2">
                  <label className="block text-sm font-medium text-green-700">
                    Ou utilisez le texte anonymisé :
                  </label>
                  {deanonymizationInputText && (
                    <button
                      onClick={clearDeanonymizationText}
                      className="p-1 text-red-500 hover:text-red-700 rounded-full transition-colors"
                      title="Supprimer le texte"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  )}
                </div>
                <textarea
                  id="Text-AREA-Deanonimisation"
                  value={deanonymizationInputText}
                  onChange={(e) => setDeanonymizationInputText(e.target.value)}
                  placeholder="Collez ici le texte anonymisé à dé-anonymiser..."
                  className="w-full h-32 px-3 py-2 border border-green-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 resize-none"
                />
                <div className="flex justify-between items-center mt-2">
                  <span className="text-xs text-green-600">
                    {deanonymizationInputText.length} caractères
                  </span>
                  <button
                    onClick={deanonymizeText}
                    disabled={!deanonymizationInputText.trim() || isProcessing}
                    className="bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white px-4 py-2 rounded-md transition-colors text-sm"
                  >
                    {isProcessing ? 'Traitement...' : 'Dé-anonymiser'}
                  </button>
                </div>
              </div>

              {/* Résultat de dé-anonymisation */}
              {deanonymizedText && (
                <div className="border-t border-green-200 pt-4">
                  <div className="flex justify-between items-center mb-2">
                    <label className="block text-sm font-medium text-green-700">
                      Texte dé-anonymisé :
                    </label>
                    <button
                      onClick={() => setDeanonymizedText('')}
                      className="p-1 text-red-500 hover:text-red-700 rounded-full transition-colors"
                      title="Supprimer le texte dé-anonymisé"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </div>
                  <textarea
                    id="Text-AREA-Deanonimisation-result"
                    value={deanonymizedText}
                    onChange={(e) => setDeanonymizedText(e.target.value)}
                    className="w-full h-32 px-3 py-2 border border-green-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 resize-none bg-green-50"
                  />
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Messages d'erreur */}
        {error && (
          <div className="mt-4 p-4 bg-red-50 text-red-700 rounded-lg border border-red-200 flex items-start">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 mt-0.5 flex-shrink-0" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            <span>{error}</span>
          </div>
        )}

        {/* Mapping des correspondances */}
        {mapping && Object.keys(mapping).length > 0 && (
          <div className="mt-4 p-4 bg-gray-50 rounded-lg border">
            <h4 className="text-sm font-medium text-gray-700 mb-2">Correspondances détectées :</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs">
              {Object.entries(mapping).map(([key, value]) => (
                <div key={key} className="flex justify-between p-2 bg-white rounded border">
                  <span className="font-mono text-blue-600">{key}</span>
                  <span className="text-gray-600">→</span>
                  <span className="text-gray-800">{value}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AnonymizationPanel; 