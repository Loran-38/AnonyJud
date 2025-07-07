import React from 'react';
import { Link } from 'react-router-dom';

const HomePage = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Hero Section */}
      <div className="w-full px-4 py-16">
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            AnonyJud
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Anonymisez vos documents juridiques en toute sécurité pour utiliser l'IA 
            en conformité avec l'IA Act et le RGPD
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link 
              to="/pricing" 
              className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg font-medium transition-colors"
            >
              Voir les tarifs
            </Link>
            <Link 
              to="/signup" 
              className="bg-white hover:bg-gray-50 text-blue-600 px-8 py-3 rounded-lg font-medium border-2 border-blue-600 transition-colors"
            >
              Commencer gratuitement
            </Link>
          </div>
        </div>

        {/* Problem Section */}
        <div className="bg-white rounded-xl shadow-lg p-8 mb-12">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-8">
            Pourquoi anonymiser vos documents juridiques ?
          </h2>
          
          <div className="grid md:grid-cols-2 gap-8">
            <div className="bg-red-50 p-6 rounded-lg border-l-4 border-red-400">
              <h3 className="text-xl font-semibold text-red-800 mb-4 flex items-center">
                <svg className="w-6 h-6 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
                Risques sans anonymisation
              </h3>
              <ul className="text-red-700 space-y-2">
                <li>• <strong>Violation du RGPD</strong> : Exposition de données personnelles</li>
                <li>• <strong>Non-conformité IA Act</strong> : Risques juridiques majeurs</li>
                <li>• <strong>Secret professionnel</strong> : Rupture de confidentialité</li>
                <li>• <strong>Sanctions financières</strong> : Jusqu'à 4% du CA annuel</li>
              </ul>
            </div>

            <div className="bg-green-50 p-6 rounded-lg border-l-4 border-green-400">
              <h3 className="text-xl font-semibold text-green-800 mb-4 flex items-center">
                <svg className="w-6 h-6 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                Avantages de l'anonymisation
              </h3>
              <ul className="text-green-700 space-y-2">
                <li>• <strong>Conformité RGPD</strong> : Protection des données personnelles</li>
                <li>• <strong>Respect IA Act</strong> : Utilisation sécurisée de l'IA</li>
                <li>• <strong>Confidentialité préservée</strong> : Secret professionnel maintenu</li>
                <li>• <strong>Tranquillité juridique</strong> : Aucun risque de sanction</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Features Section */}
        <div className="bg-white rounded-xl shadow-lg p-8 mb-12">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-8">
            Comment ça fonctionne ?
          </h2>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="bg-blue-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-2">1. Importez vos documents</h3>
              <p className="text-gray-600">Téléchargez vos fichiers PDF, Word ou ODT contenant des données sensibles</p>
            </div>

            <div className="text-center">
              <div className="bg-green-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-2">2. Anonymisation automatique</h3>
              <p className="text-gray-600">Notre algorithme remplace automatiquement les noms, adresses et données personnelles</p>
            </div>

            <div className="text-center">
              <div className="bg-purple-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-2">3. Utilisez l'IA en sécurité</h3>
              <p className="text-gray-600">Utilisez vos documents anonymisés avec ChatGPT, Claude ou tout autre IA</p>
            </div>
          </div>
        </div>

        {/* Legal Compliance Section */}
        <div className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-xl shadow-lg p-8 mb-12">
          <h2 className="text-3xl font-bold text-center mb-8">
            Conformité juridique garantie
          </h2>
          
          <div className="grid md:grid-cols-2 gap-8">
            <div>
              <h3 className="text-xl font-semibold mb-4 flex items-center">
                <svg className="w-6 h-6 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zm0 4a1 1 0 011-1h12a1 1 0 011 1v8a1 1 0 01-1 1H4a1 1 0 01-1-1V8z" clipRule="evenodd" />
                </svg>
                RGPD (2018)
              </h3>
              <p className="text-blue-100 mb-4">
                Le Règlement Général sur la Protection des Données impose des règles strictes 
                sur le traitement des données personnelles.
              </p>
              <p className="text-blue-100">
                <strong>Notre solution :</strong> Anonymisation complète des données personnelles 
                avant tout traitement par IA.
              </p>
            </div>

            <div>
              <h3 className="text-xl font-semibold mb-4 flex items-center">
                <svg className="w-6 h-6 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M9.504 1.132a1 1 0 01.992 0l1.75 1a1 1 0 11-.992 1.736L10 3.152l-1.254.716a1 1 0 11-.992-1.736l1.75-1zM5.618 4.504a1 1 0 01-.372 1.364L5.016 6l.23.132a1 1 0 11-.992 1.736L3 7.723V8a1 1 0 01-2 0V6a.996.996 0 01.52-.878l1.734-.99a1 1 0 011.364.372zm8.764 0a1 1 0 011.364-.372l1.733.99A1.002 1.002 0 0118 6v2a1 1 0 11-2 0v-.277l-1.254.145a1 1 0 11-.992-1.736L14.984 6l-.23-.132a1 1 0 01-.372-1.364zm-7 4a1 1 0 011.364-.372L10 8.848l1.254-.716a1 1 0 11.992 1.736L11 10.723V12a1 1 0 11-2 0v-1.277l-1.246-.855a1 1 0 01-.372-1.364zM3 11a1 1 0 011 1v1.277l1.246.855a1 1 0 11-.992 1.736l-1.75-1A1 1 0 012 14v-2a1 1 0 011-1zm14 0a1 1 0 011 1v2a1 1 0 01-.504.868l-1.75 1a1 1 0 11-.992-1.736L16 13.277V12a1 1 0 011-1zm-9.618 5.504a1 1 0 011.364-.372l.254.145V16a1 1 0 112 0v.277l.254-.145a1 1 0 11.992 1.736l-1.735.992a.995.995 0 01-1.022 0l-1.735-.992a1 1 0 01-.372-1.364z" clipRule="evenodd" />
                </svg>
                IA Act (2024)
              </h3>
              <p className="text-blue-100 mb-4">
                Le nouveau règlement européen sur l'IA impose des obligations strictes 
                pour l'utilisation d'IA avec des données sensibles.
              </p>
              <p className="text-blue-100">
                <strong>Notre solution :</strong> Respect total des exigences de transparence 
                et de protection des données.
              </p>
            </div>
          </div>
        </div>

        {/* CTA Section */}
        <div className="text-center bg-white rounded-xl shadow-lg p-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Prêt à utiliser l'IA en toute sécurité ?
          </h2>
          <p className="text-xl text-gray-600 mb-8">
            Commencez gratuitement avec 1 projet inclus
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link 
              to="/signup" 
              className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg font-medium transition-colors"
            >
              Inscription gratuite
            </Link>
            <Link 
              to="/pricing" 
              className="bg-gray-100 hover:bg-gray-200 text-gray-800 px-8 py-3 rounded-lg font-medium transition-colors"
            >
              Voir tous les tarifs
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage; 