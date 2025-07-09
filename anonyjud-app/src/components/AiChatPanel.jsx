import React, { useState, useRef, useEffect } from 'react';

const AiChatPanel = ({ selectedProject }) => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [selectedFolder, setSelectedFolder] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [history, setHistory] = useState([]);
  const [showHistory, setShowHistory] = useState(false);
  const messagesEndRef = useRef(null);
  const folderInputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  if (!selectedProject) {
    return (
      <div className="h-full flex items-center justify-center text-center">
        <div>
          <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Aucun projet sélectionné
          </h3>
          <p className="text-gray-600">
            Sélectionnez un projet pour utiliser le chat IA.
          </p>
        </div>
      </div>
    );
  }

  const handleFolderSelect = () => {
    // Simuler la sélection d'un dossier (sera remplacé par l'API réelle)
    if (folderInputRef.current) {
      folderInputRef.current.click();
    }
  };

  const handleFolderChange = (event) => {
    const files = event.target.files;
    if (files && files.length > 0) {
      // Obtenir le chemin du dossier à partir du premier fichier
      const firstFile = files[0];
      const folderPath = firstFile.webkitRelativePath.split('/')[0];
      setSelectedFolder(folderPath);
    }
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = {
      id: Date.now(),
      text: inputMessage,
      sender: 'user',
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    // Simuler une réponse de l'IA (sera remplacé par l'API réelle)
    setTimeout(() => {
      const aiResponse = {
        id: Date.now() + 1,
        text: "Je suis une IA en cours de développement. Cette fonctionnalité sera bientôt disponible avec un modèle Mistral ou équivalent. Votre message a été enregistré dans l'historique.",
        sender: 'ai',
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, aiResponse]);
      
      // Ajouter à l'historique
      const historyEntry = {
        id: Date.now() + 2,
        timestamp: new Date().toISOString(),
        project: selectedProject.nom,
        folder: selectedFolder || 'Aucun dossier sélectionné',
        prompt: userMessage.text,
        response: aiResponse.text
      };

      setHistory(prev => [...prev, historyEntry]);
      setIsLoading(false);
    }, 1500);
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSendMessage();
    }
  };

  const exportHistoryToWord = () => {
    // Créer le contenu du document
    const content = history.map(entry => `
DATE: ${new Date(entry.timestamp).toLocaleString('fr-FR')}
PROJET: ${entry.project}
DOSSIER: ${entry.folder}

PROMPT:
${entry.prompt}

RÉPONSE IA:
${entry.response}

${'='.repeat(80)}
`).join('\n');

    const blob = new Blob([content], { type: 'application/msword' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `historique_ia_${new Date().toISOString().split('T')[0]}.doc`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  };

  const exportHistoryToPDF = () => {
    // Simuler l'export PDF (nécessitera une bibliothèque comme jsPDF)
    alert('Export PDF sera implémenté avec jsPDF dans une prochaine version');
  };

  const clearHistory = () => {
    if (window.confirm('Êtes-vous sûr de vouloir effacer tout l\'historique ?')) {
      setHistory([]);
    }
  };

  return (
    <div className="h-full flex">
      {/* Zone principale du chat */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="p-6 border-b bg-gray-50">
          <h2 className="text-xl font-semibold text-gray-900">Chat IA</h2>
          <p className="text-gray-600 mt-1">
            Projet: {selectedProject.nom} • Assistant IA juridique
          </p>
        </div>

        {/* Sélection du dossier */}
        <div className="p-4 border-b bg-white">
          <div className="flex items-center gap-4">
            <button
              onClick={handleFolderSelect}
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md transition-colors flex items-center gap-2"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
              </svg>
              Sélectionner un dossier
            </button>
            {selectedFolder && (
              <span className="text-sm text-gray-600">
                Dossier: <span className="font-medium">{selectedFolder}</span>
              </span>
            )}
          </div>
          <input
            ref={folderInputRef}
            type="file"
            webkitdirectory="true"
            directory="true"
            multiple
            onChange={handleFolderChange}
            className="hidden"
          />
        </div>

        {/* Zone de messages */}
        <div className="flex-1 p-4 overflow-y-auto bg-gray-50">
          {messages.length === 0 ? (
            <div className="text-center text-gray-500 mt-8">
              <svg className="w-12 h-12 mx-auto mb-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
              <p>Commencez une conversation avec l'IA</p>
              <p className="text-sm mt-2">Posez vos questions sur l'analyse juridique</p>
            </div>
          ) : (
            <div className="space-y-4">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                      message.sender === 'user'
                        ? 'bg-blue-600 text-white'
                        : 'bg-white text-gray-800 border'
                    }`}
                  >
                    <p className="text-sm">{message.text}</p>
                    <p className={`text-xs mt-1 ${
                      message.sender === 'user' ? 'text-blue-100' : 'text-gray-500'
                    }`}>
                      {new Date(message.timestamp).toLocaleTimeString('fr-FR')}
                    </p>
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="flex justify-start">
                  <div className="bg-white text-gray-800 border px-4 py-2 rounded-lg">
                    <div className="flex items-center gap-2">
                      <svg className="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      <span className="text-sm">L'IA réfléchit...</span>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        {/* Zone de saisie */}
        <div className="p-4 border-t bg-white">
          <div className="flex gap-2">
            <textarea
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Tapez votre message..."
              rows="2"
              className="flex-1 p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none"
            />
            <button
              onClick={handleSendMessage}
              disabled={!inputMessage.trim() || isLoading}
              className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white px-4 py-2 rounded-md transition-colors flex items-center gap-2"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
              Envoyer
            </button>
          </div>
        </div>
      </div>

      {/* Panneau latéral - Historique */}
      <div className={`${showHistory ? 'w-80' : 'w-12'} border-l bg-white transition-all duration-300`}>
        <div className="p-3 border-b">
          <button
            onClick={() => setShowHistory(!showHistory)}
            className="w-full flex items-center justify-center p-2 hover:bg-gray-100 rounded-md transition-colors"
          >
            <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {showHistory && <span className="ml-2 text-sm font-medium">Historique</span>}
          </button>
        </div>

        {showHistory && (
          <div className="flex flex-col h-full">
            {/* Boutons d'export */}
            <div className="p-3 border-b space-y-2">
              <button
                onClick={exportHistoryToWord}
                disabled={history.length === 0}
                className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white px-3 py-2 rounded-md text-sm transition-colors flex items-center gap-2"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                Export Word
              </button>
              <button
                onClick={exportHistoryToPDF}
                disabled={history.length === 0}
                className="w-full bg-red-600 hover:bg-red-700 disabled:bg-gray-400 text-white px-3 py-2 rounded-md text-sm transition-colors flex items-center gap-2"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                Export PDF
              </button>
              <button
                onClick={clearHistory}
                disabled={history.length === 0}
                className="w-full bg-gray-600 hover:bg-gray-700 disabled:bg-gray-400 text-white px-3 py-2 rounded-md text-sm transition-colors flex items-center gap-2"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
                Effacer
              </button>
            </div>

            {/* Liste de l'historique */}
            <div className="flex-1 overflow-y-auto p-3">
              {history.length === 0 ? (
                <p className="text-sm text-gray-500 text-center mt-4">
                  Aucun historique disponible
                </p>
              ) : (
                <div className="space-y-3">
                  {history.slice().reverse().map((entry) => (
                    <div key={entry.id} className="p-3 bg-gray-50 rounded-lg">
                      <div className="text-xs text-gray-500 mb-2">
                        {new Date(entry.timestamp).toLocaleString('fr-FR')}
                      </div>
                      <div className="text-sm">
                        <div className="font-medium text-gray-900 mb-1">Prompt:</div>
                        <div className="text-gray-700 mb-2 line-clamp-2">{entry.prompt}</div>
                        <div className="font-medium text-gray-900 mb-1">Réponse:</div>
                        <div className="text-gray-700 line-clamp-3">{entry.response}</div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AiChatPanel; 