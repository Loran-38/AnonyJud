import React from 'react';
import { Link } from 'react-router-dom';

const HomePage = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Hero Section */}
      <div className="w-full px-4 py-20">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-20">
            {/* Logo et titre principal */}
            <div className="flex justify-center mb-8">
              <div className="relative">
                <div className="absolute -inset-4 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-full blur opacity-20"></div>
                <div className="relative bg-white rounded-full p-6 shadow-lg">
                  <svg className="w-16 h-16 text-blue-600" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.94-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>
                  </svg>
                </div>
              </div>
            </div>
            
            <h1 className="text-6xl font-bold text-gray-900 mb-6 bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
              AnonyJud
            </h1>
            <p className="text-2xl text-gray-600 mb-4 max-w-4xl mx-auto leading-relaxed">
              Anonymisez vos documents juridiques en toute sécurité pour utiliser l'IA 
              en conformité avec l'IA Act et le RGPD
            </p>
            <p className="text-lg text-gray-500 mb-12 max-w-2xl mx-auto">
              La solution de référence pour les professionnels du droit
            </p>
            
            {/* Boutons CTA avec animations */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-16">
              <Link 
                to="/pricing" 
                className="group bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white px-8 py-4 rounded-xl font-semibold transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl"
              >
                <span className="flex items-center justify-center">
                  Voir les tarifs
                  <svg className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                  </svg>
                </span>
              </Link>
              <Link 
                to="/signup" 
                className="group bg-white hover:bg-gray-50 text-blue-600 px-8 py-4 rounded-xl font-semibold border-2 border-blue-600 transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl"
              >
                <span className="flex items-center justify-center">
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                  Commencer gratuitement
                </span>
              </Link>
            </div>
            
            {/* Badges de confiance */}
            <div className="flex flex-wrap justify-center gap-6 text-sm text-gray-500">
              <div className="flex items-center space-x-2">
                <svg className="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                <span>Conforme RGPD</span>
              </div>
              <div className="flex items-center space-x-2">
                <svg className="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                <span>Respect IA Act 2024</span>
              </div>
              <div className="flex items-center space-x-2">
                <svg className="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                <span>Sécurisé & Fiable</span>
              </div>
            </div>
          </div>
        </div>

        {/* Problem Section */}
        <div className="max-w-6xl mx-auto mb-20">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Pourquoi anonymiser vos documents juridiques ?
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              L'utilisation d'IA avec des données sensibles expose à des risques juridiques majeurs
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 gap-8">
            {/* Risques */}
            <div className="group relative">
              <div className="absolute -inset-1 bg-gradient-to-r from-red-600 to-pink-600 rounded-xl blur opacity-25 group-hover:opacity-75 transition duration-300"></div>
              <div className="relative bg-white p-8 rounded-xl shadow-lg">
                <div className="flex items-center mb-6">
                  <div className="bg-red-100 rounded-full p-3 mr-4">
                    <svg className="w-8 h-8 text-red-600" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900">
                    Risques sans anonymisation
                  </h3>
                </div>
                <div className="space-y-4">
                  <div className="flex items-start space-x-3">
                    <div className="bg-red-500 rounded-full w-2 h-2 mt-2 flex-shrink-0"></div>
                    <div>
                      <h4 className="font-semibold text-gray-900">Violation du RGPD</h4>
                      <p className="text-gray-600">Exposition de données personnelles</p>
                    </div>
                  </div>
                  <div className="flex items-start space-x-3">
                    <div className="bg-red-500 rounded-full w-2 h-2 mt-2 flex-shrink-0"></div>
                    <div>
                      <h4 className="font-semibold text-gray-900">Non-conformité IA Act</h4>
                      <p className="text-gray-600">Risques juridiques majeurs</p>
                    </div>
                  </div>
                  <div className="flex items-start space-x-3">
                    <div className="bg-red-500 rounded-full w-2 h-2 mt-2 flex-shrink-0"></div>
                    <div>
                      <h4 className="font-semibold text-gray-900">Secret professionnel</h4>
                      <p className="text-gray-600">Rupture de confidentialité</p>
                    </div>
                  </div>
                  <div className="flex items-start space-x-3">
                    <div className="bg-red-500 rounded-full w-2 h-2 mt-2 flex-shrink-0"></div>
                    <div>
                      <h4 className="font-semibold text-gray-900">Sanctions financières</h4>
                      <p className="text-gray-600">Jusqu'à 4% du CA annuel</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Avantages */}
            <div className="group relative">
              <div className="absolute -inset-1 bg-gradient-to-r from-green-600 to-emerald-600 rounded-xl blur opacity-25 group-hover:opacity-75 transition duration-300"></div>
              <div className="relative bg-white p-8 rounded-xl shadow-lg">
                <div className="flex items-center mb-6">
                  <div className="bg-green-100 rounded-full p-3 mr-4">
                    <svg className="w-8 h-8 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900">
                    Avantages de l'anonymisation
                  </h3>
                </div>
                <div className="space-y-4">
                  <div className="flex items-start space-x-3">
                    <div className="bg-green-500 rounded-full w-2 h-2 mt-2 flex-shrink-0"></div>
                    <div>
                      <h4 className="font-semibold text-gray-900">Conformité RGPD</h4>
                      <p className="text-gray-600">Protection des données personnelles</p>
                    </div>
                  </div>
                  <div className="flex items-start space-x-3">
                    <div className="bg-green-500 rounded-full w-2 h-2 mt-2 flex-shrink-0"></div>
                    <div>
                      <h4 className="font-semibold text-gray-900">Respect IA Act</h4>
                      <p className="text-gray-600">Utilisation sécurisée de l'IA</p>
                    </div>
                  </div>
                  <div className="flex items-start space-x-3">
                    <div className="bg-green-500 rounded-full w-2 h-2 mt-2 flex-shrink-0"></div>
                    <div>
                      <h4 className="font-semibold text-gray-900">Confidentialité préservée</h4>
                      <p className="text-gray-600">Secret professionnel maintenu</p>
                    </div>
                  </div>
                  <div className="flex items-start space-x-3">
                    <div className="bg-green-500 rounded-full w-2 h-2 mt-2 flex-shrink-0"></div>
                    <div>
                      <h4 className="font-semibold text-gray-900">Tranquillité juridique</h4>
                      <p className="text-gray-600">Aucun risque de sanction</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Features Section */}
        <div className="max-w-6xl mx-auto mb-20">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Comment ça fonctionne ?
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Un processus simple en 3 étapes pour protéger vos données
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {/* Étape 1 */}
            <div className="group text-center relative">
              <div className="relative mb-8">
                <div className="absolute -inset-4 bg-gradient-to-r from-blue-600 to-cyan-600 rounded-full blur opacity-25 group-hover:opacity-75 transition duration-300"></div>
                <div className="relative bg-white rounded-full w-20 h-20 flex items-center justify-center mx-auto shadow-lg group-hover:shadow-xl transition-shadow">
                  <svg className="w-10 h-10 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <div className="absolute -top-2 -right-2 bg-blue-600 text-white rounded-full w-8 h-8 flex items-center justify-center text-sm font-bold">
                  1
                </div>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Importez vos documents</h3>
              <p className="text-gray-600 leading-relaxed">
                Téléchargez vos fichiers PDF, Word ou ODT contenant des données sensibles
              </p>
            </div>

            {/* Étape 2 */}
            <div className="group text-center relative">
              <div className="relative mb-8">
                <div className="absolute -inset-4 bg-gradient-to-r from-green-600 to-emerald-600 rounded-full blur opacity-25 group-hover:opacity-75 transition duration-300"></div>
                <div className="relative bg-white rounded-full w-20 h-20 flex items-center justify-center mx-auto shadow-lg group-hover:shadow-xl transition-shadow">
                  <svg className="w-10 h-10 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                </div>
                <div className="absolute -top-2 -right-2 bg-green-600 text-white rounded-full w-8 h-8 flex items-center justify-center text-sm font-bold">
                  2
                </div>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Anonymisation automatique</h3>
              <p className="text-gray-600 leading-relaxed">
                Notre algorithme remplace automatiquement les noms, adresses et données personnelles
              </p>
            </div>

            {/* Étape 3 */}
            <div className="group text-center relative">
              <div className="relative mb-8">
                <div className="absolute -inset-4 bg-gradient-to-r from-purple-600 to-pink-600 rounded-full blur opacity-25 group-hover:opacity-75 transition duration-300"></div>
                <div className="relative bg-white rounded-full w-20 h-20 flex items-center justify-center mx-auto shadow-lg group-hover:shadow-xl transition-shadow">
                  <svg className="w-10 h-10 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                </div>
                <div className="absolute -top-2 -right-2 bg-purple-600 text-white rounded-full w-8 h-8 flex items-center justify-center text-sm font-bold">
                  3
                </div>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Utilisez l'IA en sécurité</h3>
              <p className="text-gray-600 leading-relaxed">
                Utilisez vos documents anonymisés avec ChatGPT, Claude ou tout autre IA
              </p>
            </div>
          </div>
        </div>

        {/* Legal Compliance Section */}
        <div className="max-w-6xl mx-auto mb-20">
          <div className="relative overflow-hidden bg-gradient-to-br from-blue-600 via-indigo-600 to-purple-600 rounded-3xl shadow-2xl">
            {/* Effet de fond */}
            <div className="absolute inset-0 bg-gradient-to-r from-blue-600/20 to-purple-600/20"></div>
            <div className="absolute top-0 left-0 w-full h-full">
              <div className="absolute top-10 left-10 w-20 h-20 bg-white/10 rounded-full blur-xl"></div>
              <div className="absolute bottom-10 right-10 w-32 h-32 bg-white/5 rounded-full blur-2xl"></div>
              <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-40 h-40 bg-white/5 rounded-full blur-3xl"></div>
            </div>
            
            <div className="relative p-12 text-white">
              <div className="text-center mb-12">
                <h2 className="text-4xl font-bold mb-4">
                  Conformité juridique garantie
                </h2>
                <p className="text-xl text-blue-100 max-w-3xl mx-auto">
                  Respectez les réglementations européennes les plus strictes
                </p>
              </div>
              
              <div className="grid md:grid-cols-2 gap-12">
                {/* RGPD */}
                <div className="group">
                  <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 hover:bg-white/20 transition-all duration-300">
                    <div className="flex items-center mb-6">
                      <div className="bg-white/20 rounded-full p-3 mr-4">
                        <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zm0 4a1 1 0 011-1h12a1 1 0 011 1v8a1 1 0 01-1 1H4a1 1 0 01-1-1V8z" clipRule="evenodd" />
                        </svg>
                      </div>
                      <div>
                        <h3 className="text-2xl font-bold">RGPD</h3>
                        <p className="text-blue-100 text-sm">Règlement 2018</p>
                      </div>
                    </div>
                    <p className="text-blue-100 mb-4 leading-relaxed">
                      Le Règlement Général sur la Protection des Données impose des règles strictes 
                      sur le traitement des données personnelles.
                    </p>
                    <div className="bg-white/10 rounded-lg p-4">
                      <p className="text-white font-semibold">Notre solution :</p>
                      <p className="text-blue-100">
                        Anonymisation complète des données personnelles avant tout traitement par IA.
                      </p>
                    </div>
                  </div>
                </div>

                {/* IA Act */}
                <div className="group">
                  <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 hover:bg-white/20 transition-all duration-300">
                    <div className="flex items-center mb-6">
                      <div className="bg-white/20 rounded-full p-3 mr-4">
                        <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M9.504 1.132a1 1 0 01.992 0l1.75 1a1 1 0 11-.992 1.736L10 3.152l-1.254.716a1 1 0 11-.992-1.736l1.75-1zM5.618 4.504a1 1 0 01-.372 1.364L5.016 6l.23.132a1 1 0 11-.992 1.736L3 7.723V8a1 1 0 01-2 0V6a.996.996 0 01.52-.878l1.734-.99a1 1 0 011.364.372zm8.764 0a1 1 0 011.364-.372l1.733.99A1.002 1.002 0 0118 6v2a1 1 0 11-2 0v-.277l-1.254.145a1 1 0 11-.992-1.736L14.984 6l-.23-.132a1 1 0 01-.372-1.364zm-7 4a1 1 0 011.364-.372L10 8.848l1.254-.716a1 1 0 11.992 1.736L11 10.723V12a1 1 0 11-2 0v-1.277l-1.246-.855a1 1 0 01-.372-1.364zM3 11a1 1 0 011 1v1.277l1.246.855a1 1 0 11-.992 1.736l-1.75-1A1 1 0 012 14v-2a1 1 0 011-1zm14 0a1 1 0 011 1v2a1 1 0 01-.504.868l-1.75 1a1 1 0 11-.992-1.736L16 13.277V12a1 1 0 011-1zm-9.618 5.504a1 1 0 011.364-.372l.254.145V16a1 1 0 112 0v.277l.254-.145a1 1 0 11.992 1.736l-1.735.992a.995.995 0 01-1.022 0l-1.735-.992a1 1 0 01-.372-1.364z" clipRule="evenodd" />
                        </svg>
                      </div>
                      <div>
                        <h3 className="text-2xl font-bold">IA Act</h3>
                        <p className="text-blue-100 text-sm">Règlement 2024</p>
                      </div>
                    </div>
                    <p className="text-blue-100 mb-4 leading-relaxed">
                      Le nouveau règlement européen sur l'IA impose des obligations strictes 
                      pour l'utilisation d'IA avec des données sensibles.
                    </p>
                    <div className="bg-white/10 rounded-lg p-4">
                      <p className="text-white font-semibold">Notre solution :</p>
                      <p className="text-blue-100">
                        Respect total des exigences de transparence et de protection des données.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
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