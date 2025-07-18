import React, { useState } from 'react';

const ResourcesPage = () => {
  const [openFaqItem, setOpenFaqItem] = useState(null);

  const toggleFaqItem = (index) => {
    setOpenFaqItem(openFaqItem === index ? null : index);
  };

  const formatAnswer = (text) => {
    return text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .split('\n')
      .map((line, index) => (
        <span key={index}>
          {index > 0 && <br />}
          <span dangerouslySetInnerHTML={{ __html: line }} />
        </span>
      ));
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
      question: "Y a-t-il des limites au traitement des fichiers PDF ?",
      answer: `Oui. Pour des raisons techniques liées à la structure spécifique des fichiers PDF, certaines limites doivent être prises en compte lors de l'anonymisation :

• **Images non traitées** : les images contenues dans le PDF ne sont pas analysées ni conservées. Les fichiers anonymisés ou désanonymisés ne contiennent donc pas les images présentes dans vos documents originaux.

• **Variations de police et de mise en page** : après anonymisation, des différences mineures peuvent apparaître dans les polices de caractères (style, taille) ainsi que dans la mise en page générale du document, en raison du rendu PDF propre aux bibliothèques de traitement.

• **Optimisation pour l'IA** : le fichier PDF anonymisé est reconstruit pour être lisible par une intelligence artificielle. Cela signifie que tout le contenu textuel est interprétable et exploitable par le modèle de langage (LLM), ce qui garantit une analyse pertinente en aval.`
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
          <nav className="flex flex-wrap space-x-6 justify-center text-sm md:text-base">
            <a href="#faq" className="text-blue-600 hover:text-blue-800 font-medium transition-colors">FAQ</a>
            <a href="#comment-ca-marche" className="text-blue-600 hover:text-blue-800 font-medium transition-colors">Comment ça marche</a>
            <a href="#cadre-reglementaire" className="text-blue-600 hover:text-blue-800 font-medium transition-colors">Cadre réglementaire</a>
            <a href="#conformite-ia-act" className="text-blue-600 hover:text-blue-800 font-medium transition-colors">IA Act & RGPD</a>
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
                      <div className="text-gray-700 leading-relaxed">{formatAnswer(item.answer)}</div>
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

        {/* Conformité IA Act & RGPD - Section détaillée */}
        <section id="conformite-ia-act" className="mb-16">
          <div className="bg-white rounded-xl shadow-sm p-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center flex items-center justify-center">
              <span className="mr-3">🛡️</span>
              Conformité IA Act & RGPD : Vos obligations et comment Anonym-IA vous accompagne
            </h2>

            {/* À qui s'adresse cette synthèse */}
            <div className="mb-8 p-6 bg-blue-50 rounded-lg">
                             <h3 className="text-xl font-semibold text-blue-900 mb-4 flex items-center">
                 <span className="mr-3">👥</span>
                 À qui s'adresse Anonym-IA ?
               </h3>
              <p className="text-blue-800 mb-4">Vous êtes :</p>
              <ul className="text-blue-700 space-y-2 mb-4">
                <li>• Professionnel du droit ou de la justice (magistrat, avocat, greffe, expert)</li>
                <li>• Établissement ou professionnel de santé (médecin, psychologue, hôpital, ARS)</li>
                <li>• Administration publique ou collectivité (préfecture, rectorat, ministère)</li>
                <li>• Responsable RH ou organisme de formation</li>
              </ul>
              <div className="p-4 bg-blue-100 rounded-lg">
                <p className="text-blue-900 font-medium">
                  ➡️ Vous êtes concernés par les <strong>obligations du niveau 3 (systèmes à haut risque)</strong> du 
                  <strong> Règlement européen sur l'intelligence artificielle (AI Act)</strong>, en complément du <strong>RGPD</strong>.
                </p>
              </div>
            </div>

            {/* Vos obligations réglementaires */}
            <div className="mb-8">
              <h3 className="text-2xl font-semibold text-gray-900 mb-6 flex items-center">
                <span className="mr-3">📘</span>
                Vos obligations réglementaires en 2025
              </h3>

              {/* RGPD */}
              <div className="mb-6 p-6 bg-indigo-50 rounded-lg">
                <h4 className="text-lg font-semibold text-indigo-900 mb-4">🔹 1. Respect du RGPD</h4>
                <ul className="text-indigo-700 space-y-2">
                  <li>• Base légale du traitement</li>
                  <li>• Minimisation des données</li>
                  <li>• Limitation de la durée de conservation</li>
                  <li>• Anonymisation ou pseudonymisation des données sensibles</li>
                  <li>• Droit à l'information, à l'accès et à l'effacement</li>
                </ul>
              </div>

              {/* IA Act - Tableau des obligations */}
              <div className="mb-6">
                <h4 className="text-lg font-semibold text-gray-900 mb-4">🔹 2. Respect du AI Act – Niveau 3 (systèmes à haut risque)</h4>
                <div className="overflow-x-auto">
                  <table className="w-full border-collapse bg-white rounded-lg shadow-sm">
                    <thead>
                      <tr className="bg-gray-100">
                        <th className="border border-gray-300 px-4 py-3 text-left font-semibold text-gray-900">Obligation</th>
                        <th className="border border-gray-300 px-4 py-3 text-left font-semibold text-gray-900">Exigence</th>
                        <th className="border border-gray-300 px-4 py-3 text-left font-semibold text-gray-900">Enjeux</th>
                      </tr>
                    </thead>
                    <tbody className="text-sm">
                      <tr className="hover:bg-gray-50">
                        <td className="border border-gray-300 px-4 py-3">✅ Analyse de risques</td>
                        <td className="border border-gray-300 px-4 py-3">Évaluer l'impact du système IA</td>
                        <td className="border border-gray-300 px-4 py-3">Prévenir les atteintes aux droits</td>
                      </tr>
                      <tr className="hover:bg-gray-50">
                        <td className="border border-gray-300 px-4 py-3">✅ Qualité des données</td>
                        <td className="border border-gray-300 px-4 py-3">Données non biaisées, pertinentes</td>
                        <td className="border border-gray-300 px-4 py-3">Éviter les discriminations</td>
                      </tr>
                      <tr className="hover:bg-gray-50">
                        <td className="border border-gray-300 px-4 py-3">✅ Journalisation</td>
                        <td className="border border-gray-300 px-4 py-3">Tracer les traitements IA</td>
                        <td className="border border-gray-300 px-4 py-3">Transparence et auditabilité</td>
                      </tr>
                      <tr className="hover:bg-gray-50">
                        <td className="border border-gray-300 px-4 py-3">✅ Supervision humaine</td>
                        <td className="border border-gray-300 px-4 py-3">Intervention et correction possibles</td>
                        <td className="border border-gray-300 px-4 py-3">Contrôle humain renforcé</td>
                      </tr>
                      <tr className="hover:bg-gray-50">
                        <td className="border border-gray-300 px-4 py-3">✅ Transparence</td>
                        <td className="border border-gray-300 px-4 py-3">Explicabilité du système IA</td>
                        <td className="border border-gray-300 px-4 py-3">Compréhension par les usagers</td>
                      </tr>
                      <tr className="hover:bg-gray-50">
                        <td className="border border-gray-300 px-4 py-3">✅ Sécurité</td>
                        <td className="border border-gray-300 px-4 py-3">Protection contre les intrusions</td>
                        <td className="border border-gray-300 px-4 py-3">Cyberprotection renforcée</td>
                      </tr>
                      <tr className="hover:bg-gray-50">
                        <td className="border border-gray-300 px-4 py-3">✅ Enregistrement CE</td>
                        <td className="border border-gray-300 px-4 py-3">Déclaration et certification</td>
                        <td className="border border-gray-300 px-4 py-3">Conformité réglementaire</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>

            {/* Pourquoi utiliser Anonym-IA */}
            <div className="mb-8 p-6 bg-green-50 rounded-lg">
              <h3 className="text-xl font-semibold text-green-900 mb-4 flex items-center">
                <span className="mr-3">🤖</span>
                Pourquoi utiliser une solution comme Anonym-IA ?
              </h3>
              <ul className="text-green-700 space-y-3 mb-6">
                <li className="flex items-start">
                  <span className="mr-3 text-green-600">🔒</span>
                  <span><strong>Anonymisation automatique</strong> des données sensibles avant traitement IA</span>
                </li>
                <li className="flex items-start">
                  <span className="mr-3 text-green-600">🧾</span>
                  <span><strong>Journalisation intégrée</strong> pour traçabilité complète</span>
                </li>
                <li className="flex items-start">
                  <span className="mr-3 text-green-600">👤</span>
                  <span><strong>Supervision humaine</strong> systématique</span>
                </li>
                <li className="flex items-start">
                  <span className="mr-3 text-green-600">🛡️</span>
                  <span><strong>Réduction des risques juridiques</strong> en cas de contrôle</span>
                </li>
              </ul>

              {/* Avantages audit */}
              <div className="grid md:grid-cols-2 gap-6 mt-6">
                <div className="p-4 bg-green-100 rounded-lg">
                  <h4 className="font-semibold text-green-900 mb-2 flex items-center">
                    <span className="mr-2">🛠️</span>
                    Vous facilitez votre audit
                  </h4>
                  <ul className="text-green-700 text-sm space-y-1">
                    <li>• Preuves d'anonymisation documentées</li>
                    <li>• Données non identifiables = allègement des obligations RGPD (DPIA allégée)</li>
                  </ul>
                </div>
                <div className="p-4 bg-green-100 rounded-lg">
                  <h4 className="font-semibold text-green-900 mb-2 flex items-center">
                    <span className="mr-2">💡</span>
                    Vous préparez l'avenir
                  </h4>
                  <ul className="text-green-700 text-sm space-y-1">
                    <li>• Anticipation des exigences de certification</li>
                    <li>• Interopérabilité avec vos outils existants</li>
                  </ul>
                </div>
              </div>
            </div>

            {/* Exemples concrets */}
            <div className="mb-8">
              <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                <span className="mr-3">🧩</span>
                Exemples concrets d'utilisation
              </h3>
              <div className="overflow-x-auto">
                <table className="w-full border-collapse bg-white rounded-lg shadow-sm">
                  <thead>
                    <tr className="bg-gray-100">
                      <th className="border border-gray-300 px-4 py-3 text-left font-semibold text-gray-900">Secteur</th>
                      <th className="border border-gray-300 px-4 py-3 text-left font-semibold text-gray-900">Cas d'usage</th>
                      <th className="border border-gray-300 px-4 py-3 text-left font-semibold text-gray-900">Risque évité</th>
                    </tr>
                  </thead>
                  <tbody className="text-sm">
                    <tr className="hover:bg-gray-50">
                      <td className="border border-gray-300 px-4 py-3 font-medium">Justice</td>
                      <td className="border border-gray-300 px-4 py-3">Analyse IA de rapports d'expertise</td>
                      <td className="border border-gray-300 px-4 py-3">Divulgation d'identité non autorisée</td>
                    </tr>
                    <tr className="hover:bg-gray-50">
                      <td className="border border-gray-300 px-4 py-3 font-medium">Santé</td>
                      <td className="border border-gray-300 px-4 py-3">Lecture automatisée de documents médicaux</td>
                      <td className="border border-gray-300 px-4 py-3">Risque de ré-identification</td>
                    </tr>
                    <tr className="hover:bg-gray-50">
                      <td className="border border-gray-300 px-4 py-3 font-medium">Éducation</td>
                      <td className="border border-gray-300 px-4 py-3">Correction IA de devoirs</td>
                      <td className="border border-gray-300 px-4 py-3">Traitement inéquitable</td>
                    </tr>
                    <tr className="hover:bg-gray-50">
                      <td className="border border-gray-300 px-4 py-3 font-medium">Collectivités</td>
                      <td className="border border-gray-300 px-4 py-3">Traitement automatisé de dossiers</td>
                      <td className="border border-gray-300 px-4 py-3">Violation de données personnelles</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            {/* Ressources officielles */}
            <div className="mb-8">
              <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                <span className="mr-3">🔗</span>
                Ressources officielles
              </h3>
              <div className="grid md:grid-cols-2 gap-4">
                <a 
                  href="https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX%3A52021PC0206" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors flex items-center"
                >
                  <span className="mr-3 text-xl">📋</span>
                  <div>
                    <div className="font-medium text-gray-900">Texte du AI Act (EUR-Lex)</div>
                    <div className="text-sm text-gray-600">Règlement européen officiel</div>
                  </div>
                </a>
                <a 
                  href="https://digital-strategy.ec.europa.eu/en/policies/european-approach-artificial-intelligence" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors flex items-center"
                >
                  <span className="mr-3 text-xl">🇪🇺</span>
                  <div>
                    <div className="font-medium text-gray-900">Résumé Commission européenne</div>
                    <div className="text-sm text-gray-600">Stratégie numérique européenne</div>
                  </div>
                </a>
                <a 
                  href="https://www.cnil.fr/fr/intelligence-artificielle" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors flex items-center"
                >
                  <span className="mr-3 text-xl">🇫🇷</span>
                  <div>
                    <div className="font-medium text-gray-900">Guide CNIL – IA & RGPD</div>
                    <div className="text-sm text-gray-600">Autorité française de protection des données</div>
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

            {/* Conclusion */}
            <div className="p-6 bg-blue-50 rounded-lg border-l-4 border-blue-400">
              <h3 className="text-lg font-semibold text-blue-900 mb-3 flex items-center">
                <span className="mr-2">✅</span>
                Conclusion
              </h3>
              <p className="text-blue-800">
                <strong>Anonym-IA</strong> vous aide à sécuriser juridiquement vos pratiques, tout en vous permettant 
                d'exploiter la puissance de l'IA dans un cadre 100 % conforme. La conformité devient un levier de 
                confiance et non un frein à l'innovation.
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
                  href="https://eur-lex.europa.eu/eli/reg/2024/1689/oj" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors flex items-center"
                >
                  <span className="mr-3 text-xl">🤖</span>
                  <div>
                    <div className="font-medium text-gray-900">AI Act - Règlement européen sur l'IA</div>
                    <div className="text-sm text-gray-600">Règlement (UE) 2024/1689 du 13 juin 2024</div>
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