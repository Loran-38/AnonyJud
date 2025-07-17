import React, { useState } from 'react';

const ResourcesPage = () => {
  const [openFaqItem, setOpenFaqItem] = useState(null);

  const toggleFaqItem = (index) => {
    setOpenFaqItem(openFaqItem === index ? null : index);
  };

  const faqData = [
    {
      question: "Qu'est-ce qu'Anonym-IA ?",
      answer: "Anonym-IA est une solution d'anonymisation de documents juridiques propulsée par l'intelligence artificielle. Elle permet de remplacer automatiquement les données personnelles (noms, adresses, etc.) par des identifiants anonymes tout en préservant la structure et le sens du document."
    },
    {
      question: "Comment garantissez-vous la conformité RGPD ?",
      answer: "Notre solution respecte strictement le RGPD en appliquant les principes de minimisation des données, de pseudonymisation et d'anonymisation. Aucune donnée personnelle n'est stockée de manière permanente, et tous les traitements sont documentés pour assurer la traçabilité."
    },
    {
      question: "Quels formats de documents sont supportés ?",
      answer: "Anonym-IA supporte les formats PDF, DOCX (Word) et ODT (LibreOffice/OpenOffice). La solution préserve la mise en forme originale du document lors de l'anonymisation."
    },
    {
      question: "Puis-je dé-anonymiser un document ?",
      answer: "Oui, Anonym-IA permet la dé-anonymisation sécurisée. Vous pouvez récupérer les données originales en utilisant la clé de dé-anonymisation fournie lors du processus initial. Cette fonctionnalité est essentielle pour les cabinets d'avocats qui doivent pouvoir revenir au document original."
    },
    {
      question: "Vos serveurs sont-ils sécurisés ?",
      answer: "Absolument. Nos serveurs utilisent le chiffrement TLS/SSL, sont hébergés en Europe avec des certifications de sécurité strictes. Aucune donnée personnelle n'est conservée après traitement, et nous appliquons le principe de 'privacy by design'."
    },
    {
      question: "Comment fonctionne votre IA ?",
      answer: "Notre IA utilise des algorithmes de traitement du langage naturel (NLP) spécialement entraînés pour reconnaître les entités nommées dans les documents juridiques français. Elle identifie automatiquement les noms, prénoms, adresses, et autres données sensibles avec une précision élevée."
    }
  ];

  const useCases = [
    {
      title: "Formation des équipes juridiques",
      description: "Utilisez des cas réels anonymisés pour former vos collaborateurs sans exposer de données clients.",
      icon: "🎓"
    },
    {
      title: "Consultation d'IA externe",
      description: "Soumettez vos documents anonymisés à des IA comme ChatGPT pour obtenir des analyses sans risque.",
      icon: "🤖"
    },
    {
      title: "Recherche et études juridiques",
      description: "Créez des corpus de documents pour des études statistiques ou de la recherche académique.",
      icon: "📊"
    },
    {
      title: "Archivage et conformité",
      description: "Archivez vos dossiers en respectant les obligations de conservation tout en protégeant les données.",
      icon: "📁"
    },
    {
      title: "Collaboration inter-cabinets",
      description: "Partagez des documents avec des confrères ou experts externes en toute sécurité.",
      icon: "🤝"
    },
    {
      title: "Documentation et procédures",
      description: "Créez des modèles et exemples pour vos procédures internes basés sur des cas réels.",
      icon: "📋"
    }
  ];

  const guides = [
    {
      title: "Guide RGPD pour avocats",
      description: "Comprendre vos obligations en matière de protection des données personnelles",
      format: "PDF",
      size: "2.3 MB"
    },
    {
      title: "IA Act - Impact sur le secteur juridique",
      description: "Analyse de la nouvelle réglementation européenne sur l'intelligence artificielle",
      format: "PDF",
      size: "1.8 MB"
    },
    {
      title: "Checklist d'anonymisation",
      description: "Liste de vérification pour garantir une anonymisation complète",
      format: "PDF",
      size: "0.5 MB"
    },
    {
      title: "Modèles de clauses RGPD",
      description: "Clauses types pour vos contrats et mentions légales",
      format: "DOCX",
      size: "0.8 MB"
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-12">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">Ressources</h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Tout ce que vous devez savoir sur l'anonymisation de documents juridiques, 
              la conformité RGPD et l'utilisation sécurisée de l'IA
            </p>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-12">
        {/* Navigation interne */}
        <div className="mb-12">
          <nav className="flex space-x-8 justify-center">
            <a href="#faq" className="text-blue-600 hover:text-blue-800 font-medium transition-colors">FAQ</a>
            <a href="#comment-ca-marche" className="text-blue-600 hover:text-blue-800 font-medium transition-colors">Comment ça marche</a>
            <a href="#cadre-reglementaire" className="text-blue-600 hover:text-blue-800 font-medium transition-colors">Cadre réglementaire</a>
            <a href="#cas-usage" className="text-blue-600 hover:text-blue-800 font-medium transition-colors">Cas d'usage</a>
            <a href="#guides" className="text-blue-600 hover:text-blue-800 font-medium transition-colors">Guides</a>
          </nav>
        </div>

        {/* FAQ Section */}
        <section id="faq" className="mb-16">
          <div className="bg-white rounded-xl shadow-sm p-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">
              Questions Fréquemment Posées
            </h2>
            <div className="space-y-4">
              {faqData.map((item, index) => (
                <div key={index} className="border border-gray-200 rounded-lg">
                  <button
                    className="w-full px-6 py-4 text-left flex justify-between items-center hover:bg-gray-50 transition-colors"
                    onClick={() => toggleFaqItem(index)}
                  >
                    <span className="font-medium text-gray-900">{item.question}</span>
                    <svg
                      className={`w-5 h-5 text-gray-500 transform transition-transform ${
                        openFaqItem === index ? 'rotate-180' : ''
                      }`}
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                  </button>
                  {openFaqItem === index && (
                    <div className="px-6 pb-4">
                      <p className="text-gray-700 leading-relaxed">{item.answer}</p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Comment fonctionne Anonym-IA */}
        <section id="comment-ca-marche" className="mb-16">
          <div className="bg-white rounded-xl shadow-sm p-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">
              Comment fonctionne Anonym-IA ?
            </h2>
            <div className="grid md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl">📄</span>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">1. Upload du document</h3>
                <p className="text-gray-600">
                  Téléchargez votre document PDF, Word ou ODT. Anonym-IA analyse automatiquement le contenu 
                  pour identifier les données personnelles.
                </p>
              </div>
              <div className="text-center">
                <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl">🤖</span>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">2. Traitement IA</h3>
                <p className="text-gray-600">
                  Notre IA spécialisée en juridique français identifie et remplace les noms, prénoms, 
                  adresses et autres données sensibles par des identifiants anonymes.
                </p>
              </div>
              <div className="text-center">
                <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl">🛡️</span>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">3. Document sécurisé</h3>
                <p className="text-gray-600">
                  Récupérez votre document anonymisé, prêt à être utilisé avec des IA externes ou 
                  partagé en toute sécurité. La dé-anonymisation reste possible.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Cadre réglementaire */}
        <section id="cadre-reglementaire" className="mb-16">
          <div className="bg-white rounded-xl shadow-sm p-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">
              Cadre Réglementaire
            </h2>
            <div className="grid md:grid-cols-2 gap-8">
              <div className="bg-blue-50 p-6 rounded-lg">
                <h3 className="text-2xl font-semibold text-blue-900 mb-4 flex items-center">
                  <span className="mr-3">⚖️</span>
                  RGPD
                </h3>
                <p className="text-blue-800 mb-4">
                  Le Règlement Général sur la Protection des Données impose des obligations strictes 
                  pour le traitement des données personnelles.
                </p>
                <ul className="text-blue-700 space-y-2">
                  <li>• Minimisation des données</li>
                  <li>• Pseudonymisation obligatoire</li>
                  <li>• Droit à l'effacement</li>
                  <li>• Accountability et documentation</li>
                </ul>
              </div>
              <div className="bg-green-50 p-6 rounded-lg">
                <h3 className="text-2xl font-semibold text-green-900 mb-4 flex items-center">
                  <span className="mr-3">🤖</span>
                  IA Act
                </h3>
                <p className="text-green-800 mb-4">
                  La nouvelle réglementation européenne sur l'IA classe l'utilisation de l'IA 
                  dans le secteur juridique comme "à haut risque".
                </p>
                <ul className="text-green-700 space-y-2">
                  <li>• Transparence des algorithmes</li>
                  <li>• Supervision humaine</li>
                  <li>• Gestion des risques</li>
                  <li>• Documentation technique</li>
                </ul>
              </div>
            </div>
            <div className="mt-8 p-6 bg-yellow-50 rounded-lg border-l-4 border-yellow-400">
              <p className="text-yellow-800">
                <strong>💡 Important :</strong> Anonym-IA vous aide à respecter ces obligations en 
                anonymisant vos documents avant tout traitement par des IA externes, réduisant ainsi 
                les risques juridiques et de conformité.
              </p>
            </div>
          </div>
        </section>

        {/* Cas d'usage */}
        <section id="cas-usage" className="mb-16">
          <div className="bg-white rounded-xl shadow-sm p-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">
              Exemples de Cas d'Usage
            </h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {useCases.map((useCase, index) => (
                <div key={index} className="p-6 border border-gray-200 rounded-lg hover:shadow-md transition-shadow">
                  <div className="text-4xl mb-4">{useCase.icon}</div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-3">{useCase.title}</h3>
                  <p className="text-gray-600">{useCase.description}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Liens utiles et guides */}
        <section id="guides" className="mb-16">
          <div className="bg-white rounded-xl shadow-sm p-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">
              Liens Utiles & Guides à Télécharger
            </h2>
            
            {/* Liens externes */}
            <div className="mb-8">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Liens Officiels</h3>
              <div className="grid md:grid-cols-2 gap-4">
                <a 
                  href="https://www.cnil.fr" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors flex items-center"
                >
                  <span className="mr-3 text-xl">🇫🇷</span>
                  <div>
                    <div className="font-medium text-gray-900">CNIL - Commission Nationale Informatique et Libertés</div>
                    <div className="text-sm text-gray-600">Autorité française de protection des données</div>
                  </div>
                </a>
                <a 
                  href="https://edpb.europa.eu" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors flex items-center"
                >
                  <span className="mr-3 text-xl">🇪🇺</span>
                  <div>
                    <div className="font-medium text-gray-900">EDPB - European Data Protection Board</div>
                    <div className="text-sm text-gray-600">Conseil européen de la protection des données</div>
                  </div>
                </a>
                <a 
                  href="https://www.cnb.avocat.fr" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors flex items-center"
                >
                  <span className="mr-3 text-xl">⚖️</span>
                  <div>
                    <div className="font-medium text-gray-900">Conseil National des Barreaux</div>
                    <div className="text-sm text-gray-600">Ressources pour la profession d'avocat</div>
                  </div>
                </a>
                <a 
                  href="https://www.legifrance.gouv.fr" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors flex items-center"
                >
                  <span className="mr-3 text-xl">📚</span>
                  <div>
                    <div className="font-medium text-gray-900">Légifrance</div>
                    <div className="text-sm text-gray-600">Service public de diffusion du droit</div>
                  </div>
                </a>
              </div>
            </div>

            {/* Guides à télécharger */}
            <div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Guides à Télécharger</h3>
              <div className="grid md:grid-cols-2 gap-4">
                {guides.map((guide, index) => (
                  <div key={index} className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <h4 className="font-medium text-gray-900 mb-2">{guide.title}</h4>
                        <p className="text-sm text-gray-600 mb-3">{guide.description}</p>
                        <div className="flex items-center text-xs text-gray-500">
                          <span className="bg-gray-100 px-2 py-1 rounded mr-2">{guide.format}</span>
                          <span>{guide.size}</span>
                        </div>
                      </div>
                      <button className="ml-4 p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors">
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                      </button>
                    </div>
                  </div>
                ))}
              </div>
              <div className="mt-6 p-4 bg-blue-50 rounded-lg">
                <p className="text-blue-800 text-sm">
                  <strong>Note :</strong> Ces guides sont fournis à titre informatif. Pour des conseils juridiques 
                  personnalisés, consultez un avocat spécialisé en droit du numérique et protection des données.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Call to action */}
        <section className="text-center">
          <div className="bg-gradient-to-r from-blue-600 to-blue-700 rounded-xl p-8 text-white">
            <h2 className="text-3xl font-bold mb-4">Prêt à commencer ?</h2>
            <p className="text-xl mb-6 opacity-90">
              Découvrez comment Anonym-IA peut sécuriser vos documents juridiques
            </p>
            <div className="space-x-4">
              <a 
                href="/signup" 
                className="inline-block bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
              >
                Commencer gratuitement
              </a>
              <a 
                href="/pricing" 
                className="inline-block border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-blue-600 transition-colors"
              >
                Voir les tarifs
              </a>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};

export default ResourcesPage; 