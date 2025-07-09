import React, { useState } from 'react';
import config from '../config';

const AnonymizationPanel = ({ selectedProject, projects, setProjects }) => {
  const [uploadedFile, setUploadedFile] = useState(null);
  const [anonymizedText, setAnonymizedText] = useState('');
  const [deanonymizedText, setDeanonymizedText] = useState('');
  const [inputText, setInputText] = useState('');
  const [mapping, setMapping] = useState({});
  const [loading, setLoading] = useState(false);
  const [dragOver, setDragOver] = useState(false);

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

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setUploadedFile(file);
      setAnonymizedText('');
      setDeanonymizedText('');
      setInputText('');
      setMapping({});
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      const file = files[0];
      if (file.type === 'text/plain' || file.name.toLowerCase().endsWith('.txt') || file.name.toLowerCase().endsWith('.docx')) {
        setUploadedFile(file);
        setAnonymizedText('');
        setDeanonymizedText('');
        setInputText('');
        setMapping({});
      } else {
        alert('Veuillez sélectionner un fichier .txt ou .docx');
      }
    }
  };

  const anonymizeText = async () => {
    if (!uploadedFile && !inputText.trim()) {
      alert('Veuillez sélectionner un fichier ou saisir du texte');
      return;
    }

    if (!selectedProject.tiers || selectedProject.tiers.length === 0) {
      alert('Veuillez d\'abord configurer les tiers dans l\'onglet "Gestion des tiers"');
      return;
    }

    setLoading(true);
    try {
      if (uploadedFile) {
        // Upload de fichier
        const formData = new FormData();
        formData.append('file', uploadedFile);
        formData.append('tiers_json', JSON.stringify(selectedProject.tiers));

        const response = await fetch(`${config.API_BASE_URL}/anonymize/file`, {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) {
          throw new Error(`Erreur HTTP: ${response.status}`);
        }

        const result = await response.json();
        setAnonymizedText(result.text);
        setMapping(result.mapping);
      } else {
        // Saisie de texte
        const response = await fetch(`${config.API_BASE_URL}/anonymize/text`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            text: inputText,
            tiers: selectedProject.tiers,
          }),
        });

        if (!response.ok) {
          throw new Error(`Erreur HTTP: ${response.status}`);
        }

        const result = await response.json();
        setAnonymizedText(result.anonymized_text);
        setMapping(result.mapping);
      }
      
      setDeanonymizedText('');
    } catch (error) {
      console.error('Erreur lors de l\'anonymisation:', error);
      alert('Erreur lors de l\'anonymisation: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const deanonymizeText = async () => {
    if (!mapping || Object.keys(mapping).length === 0) {
      alert('Aucun mapping disponible. Veuillez d\'abord anonymiser un texte.');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${config.API_BASE_URL}/deanonymize/text`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          anonymized_text: anonymizedText,
          mapping: mapping,
        }),
      });

      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`);
      }

      const result = await response.json();
      setDeanonymizedText(result.deanonymized_text);
    } catch (error) {
      console.error('Erreur lors de la dé-anonymisation:', error);
      alert('Erreur lors de la dé-anonymisation: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const downloadAnonymizedFile = async () => {
    if (!uploadedFile || !selectedProject.tiers || selectedProject.tiers.length === 0) {
      alert('Veuillez d\'abord anonymiser un fichier');
      return;
    }

    try {
      const formData = new FormData();
      formData.append('file', uploadedFile);
      formData.append('tiers_json', JSON.stringify(selectedProject.tiers));

      const response = await fetch(`${config.API_BASE_URL}/anonymize/file/download`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`);
      }

      const blob = await response.blob();
      const contentDisposition = response.headers.get('Content-Disposition');
      let filename = 'document_anonymise.docx';
      
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="(.+)"/);
        if (filenameMatch) {
          filename = filenameMatch[1];
        }
      }

      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Erreur lors du téléchargement:', error);
      alert('Erreur lors du téléchargement: ' + error.message);
    }
  };

  const downloadDeanonymizedFile = async () => {
    if (!mapping || Object.keys(mapping).length === 0) {
      alert('Aucun mapping disponible. Veuillez d\'abord anonymiser un fichier.');
      return;
    }

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

      const blob = await response.blob();
      const contentDisposition = response.headers.get('Content-Disposition');
      let filename = 'document_deanonymise.docx';
      
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="(.+)"/);
        if (filenameMatch) {
          filename = filenameMatch[1];
        }
      }

      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Erreur lors du téléchargement:', error);
      alert('Erreur lors du téléchargement: ' + error.message);
    }
  };

  const isDocxFile = uploadedFile && uploadedFile.name.toLowerCase().endsWith('.docx');

  return (
    <div className="h-full">
      <div className="p-6 border-b bg-gray-50">
        <h2 className="text-xl font-semibold text-gray-900">Anonymisation</h2>
        <p className="text-gray-600 mt-1">
          Projet: {selectedProject.nom} • {selectedProject.tiers?.length || 0} tiers configurés
        </p>
      </div>
      
      <div className="p-6 overflow-y-auto" style={{ height: 'calc(100% - 88px)' }}>
        {/* Zone de glissé-déposé et saisie de texte */}
        <div className="mb-6 space-y-4">
          <h3 className="text-lg font-medium text-gray-900">Source du texte à anonymiser</h3>
          
          {/* Zone de glissé-déposé */}
          <div
            className={`relative border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
              dragOver
                ? 'border-blue-400 bg-blue-50'
                : 'border-gray-300 hover:border-gray-400'
            }`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
          >
            <svg className="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
              <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
            </svg>
            <div className="mt-4">
              <label htmlFor="file-upload" className="cursor-pointer">
                <span className="mt-2 block text-sm font-medium text-gray-900">
                  Glissez-déposez un fichier ici ou cliquez pour sélectionner
                </span>
                <input
                  id="file-upload"
                  type="file"
                  accept=".txt,.docx"
                  onChange={handleFileUpload}
                  className="sr-only"
                />
              </label>
              <p className="mt-1 text-xs text-gray-500">
                Formats acceptés: .txt, .docx
              </p>
            </div>
            {uploadedFile && (
              <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-md">
                <p className="text-sm text-green-800 font-medium">
                  ✓ Fichier sélectionné: {uploadedFile.name}
                </p>
              </div>
            )}
          </div>

          {/* Séparateur OU */}
          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-gray-300"></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-2 bg-white text-gray-500">OU</span>
            </div>
          </div>

          {/* Zone de saisie de texte */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Saisir le texte directement
            </label>
            <textarea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Collez ou tapez votre texte ici..."
              className="w-full h-32 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            />
            {inputText.trim() && (
              <p className="text-sm text-gray-600 mt-1">
                {inputText.length} caractères saisis
              </p>
            )}
          </div>
        </div>

        {/* Boutons d'action */}
        <div className="flex gap-4 mb-6">
          <button
            onClick={anonymizeText}
            disabled={loading || (!uploadedFile && !inputText.trim())}
            className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white px-4 py-2 rounded-md transition-colors flex items-center gap-2"
          >
            {loading ? (
              <>
                <svg className="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Anonymisation...
              </>
            ) : (
              'Anonymiser le texte'
            )}
          </button>

          <button
            onClick={deanonymizeText}
            disabled={loading || !anonymizedText}
            className="bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white px-4 py-2 rounded-md transition-colors"
          >
            Dé-anonymiser le texte
          </button>

          {isDocxFile && (
            <>
              <button
                onClick={downloadAnonymizedFile}
                disabled={loading || !uploadedFile}
                className="bg-purple-600 hover:bg-purple-700 disabled:bg-gray-400 text-white px-4 py-2 rounded-md transition-colors flex items-center gap-2"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                Télécharger fichier anonymisé
              </button>

              <button
                onClick={downloadDeanonymizedFile}
                disabled={loading || !mapping || Object.keys(mapping).length === 0}
                className="bg-orange-600 hover:bg-orange-700 disabled:bg-gray-400 text-white px-4 py-2 rounded-md transition-colors flex items-center gap-2"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                Télécharger fichier dé-anonymisé
              </button>
            </>
          )}
        </div>

        {/* Résultats */}
        <div className="space-y-6">
          {/* Texte anonymisé */}
          {anonymizedText && (
            <div className="bg-white border border-gray-200 rounded-lg shadow-sm">
              <div className="px-4 py-3 bg-blue-50 border-b border-blue-200 rounded-t-lg">
                <h3 className="text-lg font-medium text-blue-900 flex items-center">
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                  </svg>
                  Texte anonymisé
                </h3>
              </div>
              <div className="p-4">
                <textarea
                  value={anonymizedText}
                  onChange={(e) => setAnonymizedText(e.target.value)}
                  className="w-full h-64 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none font-mono text-sm"
                  placeholder="Le texte anonymisé apparaîtra ici..."
                />
              </div>
            </div>
          )}

          {/* Texte dé-anonymisé */}
          {deanonymizedText && (
            <div className="bg-white border border-gray-200 rounded-lg shadow-sm">
              <div className="px-4 py-3 bg-green-50 border-b border-green-200 rounded-t-lg">
                <h3 className="text-lg font-medium text-green-900 flex items-center">
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 7a2 2 0 012 2m0 0a2 2 0 012 2m-2-2a2 2 0 00-2 2m2-2V5a2 2 0 00-2-2m-2 0H9m0 0v2m0 0V5a2 2 0 012-2m0 0h2" />
                  </svg>
                  Texte dé-anonymisé
                </h3>
              </div>
              <div className="p-4">
                <textarea
                  value={deanonymizedText}
                  onChange={(e) => setDeanonymizedText(e.target.value)}
                  className="w-full h-64 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent resize-none font-mono text-sm"
                  placeholder="Le texte dé-anonymisé apparaîtra ici..."
                />
              </div>
            </div>
          )}
        </div>

        {/* Mapping */}
        {Object.keys(mapping).length > 0 && (
          <div className="mt-6">
            <h3 className="text-lg font-medium text-gray-900 mb-3">Correspondances</h3>
            <div className="bg-gray-50 p-4 rounded-lg">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                {Object.entries(mapping).map(([tag, value]) => (
                  <div key={tag} className="flex items-center justify-between p-2 bg-white rounded border">
                    <span className="font-mono text-sm text-blue-600">{tag}</span>
                    <span className="text-sm text-gray-700">{value}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AnonymizationPanel; 