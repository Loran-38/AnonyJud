import React from 'react';
import { Link } from 'react-router-dom';

const HomePage = () => {
  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section avec animations */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
        {/* Arrière-plan animé avec éléments professionnels */}
        <div className="absolute inset-0 gradient-hero animate-gradient-shift">
          
          {/* Logos en arrière-plan avec mouvements variés autour du contenu */}
          <div className="absolute top-16 left-1/4 animate-logo-orbit" style={{animationDelay: '0s'}}>
            <img 
              src="/anonym-ia-logo_ss_nom-ss_fond.png" 
              alt="" 
              className="w-20 h-20 object-contain opacity-6"
              onError={(e) => {
                e.target.style.display = 'none';
                e.target.nextElementSibling.style.display = 'block';
              }}
            />
            <div className="w-20 h-20 text-blue-300 opacity-6 hidden">
              <svg fill="currentColor" viewBox="0 0 24 24" className="w-full h-full">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
              </svg>
            </div>
          </div>
          
          <div className="absolute bottom-20 right-1/3 animate-logo-figure-eight" style={{animationDelay: '10s'}}>
            <img 
              src="/anonym-ia-logo_ss_nom-ss_fond.png" 
              alt="" 
              className="w-18 h-18 object-contain opacity-5"
              onError={(e) => {
                e.target.style.display = 'none';
                e.target.nextElementSibling.style.display = 'block';
              }}
            />
            <div className="w-18 h-18 text-blue-200 opacity-5 hidden">
              <svg fill="currentColor" viewBox="0 0 24 24" className="w-full h-full">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
              </svg>
            </div>
          </div>

          <div className="absolute top-1/3 right-20 animate-background-logo" style={{animationDelay: '20s'}}>
            <img 
              src="/anonym-ia-logo_ss_nom-ss_fond.png" 
              alt="" 
              className="w-16 h-16 object-contain opacity-4"
              onError={(e) => {
                e.target.style.display = 'none';
                e.target.nextElementSibling.style.display = 'block';
              }}
            />
            <div className="w-16 h-16 text-indigo-200 opacity-4 hidden">
              <svg fill="currentColor" viewBox="0 0 24 24" className="w-full h-full">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
              </svg>
            </div>
          </div>

          <div className="absolute bottom-1/4 left-20 animate-logo-orbit" style={{animationDelay: '15s'}}>
            <img 
              src="/anonym-ia-logo_ss_nom-ss_fond.png" 
              alt="" 
              className="w-14 h-14 object-contain opacity-5"
              onError={(e) => {
                e.target.style.display = 'none';
                e.target.nextElementSibling.style.display = 'block';
              }}
            />
            <div className="w-14 h-14 text-blue-400 opacity-5 hidden">
              <svg fill="currentColor" viewBox="0 0 24 24" className="w-full h-full">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
              </svg>
            </div>
          </div>
          
          {/* Particules flottantes dispersées sur toute la page */}
          <div className="absolute top-16 left-12 w-3 h-3 bg-blue-300 rounded-full animate-random-drift" style={{animationDelay: '0s'}}></div>
          <div className="absolute top-32 right-16 w-2 h-2 bg-indigo-400 rounded-full animate-chaotic-float" style={{animationDelay: '2s'}}></div>
          <div className="absolute bottom-32 left-16 w-4 h-4 bg-blue-400 rounded-full animate-drift-v" style={{animationDelay: '4s'}}></div>
          <div className="absolute bottom-16 right-12 w-2 h-2 bg-indigo-300 rounded-full animate-random-drift" style={{animationDelay: '6s'}}></div>
          <div className="absolute top-1/4 right-8 w-3 h-3 bg-blue-200 rounded-full animate-drift-h" style={{animationDelay: '8s'}}></div>
          <div className="absolute bottom-1/4 left-8 w-2 h-2 bg-indigo-200 rounded-full animate-chaotic-float" style={{animationDelay: '10s'}}></div>
          <div className="absolute top-1/2 left-6 w-3 h-3 bg-blue-100 rounded-full animate-float-slow" style={{animationDelay: '12s'}}></div>
          <div className="absolute top-3/4 right-6 w-2 h-2 bg-indigo-100 rounded-full animate-random-drift" style={{animationDelay: '14s'}}></div>
          <div className="absolute top-1/3 left-1/2 w-2 h-2 bg-blue-200 rounded-full animate-drift-v" style={{animationDelay: '16s'}}></div>
          <div className="absolute bottom-1/3 right-1/2 w-3 h-3 bg-indigo-200 rounded-full animate-chaotic-float" style={{animationDelay: '18s'}}></div>
          
          {/* Formes géométriques dispersées aléatoirement */}
          <div className="absolute top-20 left-1/5 w-10 h-10 border border-blue-300 rotate-45 animate-random-drift opacity-25" style={{animationDelay: '1s'}}></div>
          <div className="absolute bottom-24 right-1/5 w-8 h-8 border border-indigo-300 animate-chaotic-float opacity-30" style={{animationDelay: '3s'}}></div>
          <div className="absolute top-1/3 left-12 w-6 h-6 border border-blue-200 rotate-12 animate-drift-h opacity-20" style={{animationDelay: '5s'}}></div>
          <div className="absolute bottom-1/3 right-12 w-12 h-12 border border-indigo-200 animate-float-slow opacity-25" style={{animationDelay: '7s'}}></div>
          <div className="absolute top-2/3 right-1/3 w-7 h-7 border border-blue-100 rotate-30 animate-random-drift opacity-20" style={{animationDelay: '9s'}}></div>
          <div className="absolute bottom-2/3 left-1/3 w-9 h-9 border border-indigo-100 animate-drift-v opacity-15" style={{animationDelay: '11s'}}></div>
          <div className="absolute top-1/6 right-1/6 w-5 h-5 border border-blue-300 rotate-60 animate-chaotic-float opacity-25" style={{animationDelay: '13s'}}></div>
          <div className="absolute bottom-1/6 left-1/6 w-11 h-11 border border-indigo-300 animate-drift-h opacity-20" style={{animationDelay: '15s'}}></div>
        </div>

        {/* Contenu principal */}
        <div className="relative z-10 text-center px-4 max-w-5xl mx-auto">
          {/* Badge animé */}
          <div className="inline-flex items-center px-4 py-2 bg-blue-100 text-blue-800 rounded-full text-sm font-medium mb-8 animate-pulse">
            <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
            Conformité RGPD & IA Act garantie
          </div>

          {/* Titre principal avec animation */}
          <h1 className="text-6xl md:text-7xl font-black text-gray-900 mb-6 leading-tight">
            <span className="inline-block animate-fade-in-up logo-hover-effect" style={{animationDelay: '0.2s'}}>Anonym</span>
            <span className="inline-block text-blue-600 animate-fade-in-up animate-breathe animate-logo-glow logo-hover-effect" style={{animationDelay: '0.4s'}}>-IA</span>
          </h1>

          {/* Sous-titre animé */}
          <p className="text-xl md:text-2xl text-gray-600 mb-12 max-w-3xl mx-auto leading-relaxed animate-text-reveal" style={{animationDelay: '0.6s'}}>
            Transformez vos documents juridiques en données 
            <span className="text-blue-600 font-semibold animate-word-emphasis"> anonymisées </span>
            pour une utilisation 
            <span className="text-green-600 font-semibold animate-word-emphasis" style={{animationDelay: '1s'}}> sécurisée </span>
            de l'IA
          </p>

          {/* Boutons avec animations */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-16 animate-scroll-fade-in" style={{animationDelay: '0.8s'}}>
            <Link 
              to="/signup" 
              className="group relative bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-xl font-semibold text-lg shadow-lg btn-professional"
            >
              <span className="relative z-10">Commencer gratuitement</span>
              <div className="absolute inset-0 bg-blue-700 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            </Link>
            <Link 
              to="/pricing" 
              className="group bg-white hover:bg-gray-50 text-blue-600 px-8 py-4 rounded-xl font-semibold text-lg border-2 border-blue-600 shadow-lg btn-professional"
            >
              Découvrir les tarifs
              <svg className="inline-block w-5 h-5 ml-2 icon-interactive" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </Link>
          </div>

          {/* Statistiques animées */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-2xl mx-auto animate-scroll-fade-in" style={{animationDelay: '1s'}}>
            <div className="text-center animate-parallax-float" style={{animationDelay: '0s'}}>
              <div className="text-3xl font-bold text-blue-600 mb-2 animate-counter" style={{animationDelay: '1.2s'}}>100%</div>
              <div className="text-gray-600 animate-text-reveal" style={{animationDelay: '1.4s'}}>Conforme RGPD</div>
            </div>
            <div className="text-center animate-parallax-float" style={{animationDelay: '0.5s'}}>
              <div className="text-3xl font-bold text-green-600 mb-2 animate-counter" style={{animationDelay: '1.6s'}}>Sécurisé</div>
              <div className="text-gray-600 animate-text-reveal" style={{animationDelay: '1.8s'}}>Chiffrement avancé</div>
            </div>
            <div className="text-center animate-parallax-float" style={{animationDelay: '1s'}}>
              <div className="text-3xl font-bold text-purple-600 mb-2 animate-counter" style={{animationDelay: '2s'}}>Instantané</div>
              <div className="text-gray-600 animate-text-reveal" style={{animationDelay: '2.2s'}}>Traitement rapide</div>
            </div>
          </div>
        </div>

        {/* Flèche de scroll animée */}
        <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
          <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
          </svg>
        </div>
      </section>

      {/* Section Problématique avec animations au scroll */}
      <section className="py-20 gradient-professional">
        <div className="max-w-6xl mx-auto px-4">
          <div className="text-center mb-16 animate-scroll-fade-in">
            <h2 className="text-4xl font-bold text-gray-900 mb-4 animate-text-reveal">
              Pourquoi 
              <span className="animate-word-emphasis text-blue-600"> anonymiser </span>
              vos documents juridiques ?
            </h2>
            <div className="w-24 h-1 bg-blue-600 mx-auto rounded-full animate-parallax-float"></div>
          </div>
          
          <div className="grid md:grid-cols-2 gap-12">
            {/* Risques */}
            <div className="group card-interactive bg-gradient-to-br from-red-50 to-pink-50 p-8 rounded-2xl border border-red-100 animate-scroll-fade-in" style={{animationDelay: '0.2s'}}>
              <div className="flex items-center mb-6">
                <div className="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center mr-4 icon-interactive">
                  <svg className="w-6 h-6 text-red-600" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold text-red-800 animate-text-reveal" style={{animationDelay: '0.4s'}}>
                  Risques sans 
                  <span className="animate-word-emphasis"> anonymisation</span>
                </h3>
              </div>
              <ul className="space-y-4 text-red-700">
                <li className="flex items-start">
                  <span className="w-2 h-2 bg-red-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                  <span><strong>Violation du RGPD</strong> : Exposition de données personnelles</span>
                </li>
                <li className="flex items-start">
                  <span className="w-2 h-2 bg-red-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                  <span><strong>Non-conformité IA Act</strong> : Risques juridiques majeurs</span>
                </li>
                <li className="flex items-start">
                  <span className="w-2 h-2 bg-red-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                  <span><strong>Secret professionnel</strong> : Rupture de confidentialité</span>
                </li>
                <li className="flex items-start">
                  <span className="w-2 h-2 bg-red-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                  <span><strong>Sanctions financières</strong> : Jusqu'à 4% du CA annuel</span>
                </li>
              </ul>
            </div>

            {/* Avantages */}
            <div className="group card-interactive bg-gradient-to-br from-green-50 to-emerald-50 p-8 rounded-2xl border border-green-100 animate-scroll-fade-in" style={{animationDelay: '0.4s'}}>
              <div className="flex items-center mb-6">
                <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mr-4 icon-interactive">
                  <svg className="w-6 h-6 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold text-green-800 animate-text-reveal" style={{animationDelay: '0.6s'}}>
                  Avantages de 
                  <span className="animate-word-emphasis"> l'anonymisation</span>
                </h3>
              </div>
              <ul className="space-y-4 text-green-700">
                <li className="flex items-start">
                  <span className="w-2 h-2 bg-green-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                  <span><strong>Conformité RGPD</strong> : Protection des données personnelles</span>
                </li>
                <li className="flex items-start">
                  <span className="w-2 h-2 bg-green-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                  <span><strong>Respect IA Act</strong> : Utilisation sécurisée de l'IA</span>
                </li>
                <li className="flex items-start">
                  <span className="w-2 h-2 bg-green-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                  <span><strong>Confidentialité préservée</strong> : Secret professionnel maintenu</span>
                </li>
                <li className="flex items-start">
                  <span className="w-2 h-2 bg-green-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                  <span><strong>Tranquillité juridique</strong> : Aucun risque de sanction</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Section Comment ça fonctionne */}
      <section className="py-20 gradient-dynamic animate-gradient-shift">
        <div className="max-w-6xl mx-auto px-4">
          <div className="text-center mb-16 animate-scroll-fade-in">
            <h2 className="text-4xl font-bold text-gray-900 mb-4 animate-text-reveal">
              Comment ça 
              <span className="animate-word-emphasis text-blue-600"> fonctionne </span>
              ?
            </h2>
            <div className="w-24 h-1 bg-blue-600 mx-auto rounded-full animate-parallax-float"></div>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                step: "1",
                title: "Importez vos documents",
                description: "Téléchargez vos fichiers PDF, Word ou ODT contenant des données sensibles",
                icon: "M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z",
                color: "blue"
              },
              {
                step: "2",
                title: "Anonymisation automatique",
                description: "Notre algorithme remplace automatiquement les noms, adresses et données personnelles",
                icon: "M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z",
                color: "green"
              },
              {
                step: "3",
                title: "Utilisez l'IA en sécurité",
                description: "Utilisez vos documents anonymisés avec ChatGPT, Claude ou tout autre IA",
                icon: "M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z",
                color: "purple"
              }
            ].map((item, index) => (
              <div key={index} className="group text-center card-interactive animate-scroll-fade-in" style={{animationDelay: `${0.2 + index * 0.2}s`}}>
                <div className={`relative w-24 h-24 bg-${item.color}-100 rounded-full flex items-center justify-center mx-auto mb-6 icon-interactive animate-parallax-float`} style={{animationDelay: `${index * 0.5}s`}}>
                  <span className={`absolute -top-2 -right-2 w-8 h-8 bg-${item.color}-600 text-white rounded-full flex items-center justify-center text-sm font-bold animate-counter`} style={{animationDelay: `${0.4 + index * 0.2}s`}}>
                    {item.step}
                  </span>
                  <svg className={`w-10 h-10 text-${item.color}-600`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={item.icon} />
                  </svg>
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-4">{item.title}</h3>
                <p className="text-gray-600 leading-relaxed">{item.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Section Conformité juridique */}
      <section className="py-20 bg-gradient-to-r from-blue-600 to-indigo-600 text-white relative overflow-hidden">
        {/* Motifs décoratifs */}
        <div className="absolute top-0 left-0 w-full h-full opacity-10">
          <div className="absolute top-10 left-10 w-32 h-32 border border-white rounded-full"></div>
          <div className="absolute bottom-10 right-10 w-24 h-24 border border-white rounded-full"></div>
          <div className="absolute top-1/2 left-1/4 w-16 h-16 border border-white rotate-45"></div>
        </div>

        <div className="relative z-10 max-w-6xl mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">
              Conformité juridique garantie
            </h2>
            <div className="w-24 h-1 bg-white mx-auto rounded-full"></div>
          </div>
          
          <div className="grid md:grid-cols-2 gap-12">
            <div className="group">
              <div className="flex items-center mb-6">
                <div className="w-16 h-16 bg-white bg-opacity-20 rounded-full flex items-center justify-center mr-4 group-hover:scale-110 transition-transform duration-300">
                  <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zm0 4a1 1 0 011-1h12a1 1 0 011 1v8a1 1 0 01-1 1H4a1 1 0 01-1-1V8z" clipRule="evenodd" />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold">RGPD (2018)</h3>
              </div>
              <p className="text-blue-100 mb-4 leading-relaxed">
                Le Règlement Général sur la Protection des Données impose des règles strictes 
                sur le traitement des données personnelles.
              </p>
              <p className="text-white font-semibold">
                Notre solution : Anonymisation complète des données personnelles 
                avant tout traitement par IA.
              </p>
            </div>

            <div className="group">
              <div className="flex items-center mb-6">
                <div className="w-16 h-16 bg-white bg-opacity-20 rounded-full flex items-center justify-center mr-4 group-hover:scale-110 transition-transform duration-300">
                  <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M9.504 1.132a1 1 0 01.992 0l1.75 1a1 1 0 11-.992 1.736L10 3.152l-1.254.716a1 1 0 11-.992-1.736l1.75-1zM5.618 4.504a1 1 0 01-.372 1.364L5.016 6l.23.132a1 1 0 11-.992 1.736L3 7.723V8a1 1 0 01-2 0V6a.996.996 0 01.52-.878l1.734-.99a1 1 0 011.364.372zm8.764 0a1 1 0 011.364-.372l1.733.99A1.002 1.002 0 0118 6v2a1 1 0 11-2 0v-.277l-1.254.145a1 1 0 11-.992-1.736L14.984 6l-.23-.132a1 1 0 01-.372-1.364zm-7 4a1 1 0 011.364-.372L10 8.848l1.254-.716a1 1 0 11.992 1.736L11 10.723V12a1 1 0 11-2 0v-1.277l-1.246-.855a1 1 0 01-.372-1.364zM3 11a1 1 0 011 1v1.277l1.246.855a1 1 0 11-.992 1.736l-1.75-1A1 1 0 012 14v-2a1 1 0 011-1zm14 0a1 1 0 011 1v2a1 1 0 01-.504.868l-1.75 1a1 1 0 11-.992-1.736L16 13.277V12a1 1 0 011-1zm-9.618 5.504a1 1 0 011.364-.372l.254.145V16a1 1 0 112 0v.277l.254-.145a1 1 0 11.992 1.736l-1.735.992a.995.995 0 01-1.022 0l-1.735-.992a1 1 0 01-.372-1.364z" clipRule="evenodd" />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold">IA Act (2024)</h3>
              </div>
              <p className="text-blue-100 mb-4 leading-relaxed">
                Le nouveau règlement européen sur l'IA impose des obligations strictes 
                pour l'utilisation d'IA avec des données sensibles.
              </p>
              <p className="text-white font-semibold">
                Notre solution : Respect total des exigences de transparence 
                et de protection des données.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Final */}
      <section className="py-20 bg-white">
        <div className="max-w-4xl mx-auto text-center px-4">
          <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-3xl p-12 shadow-xl">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Prêt à utiliser l'IA en toute sécurité ?
            </h2>
            <p className="text-xl text-gray-600 mb-8">
              Commencez gratuitement avec 1 projet inclus
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link 
                to="/signup" 
                className="group bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-xl font-semibold text-lg shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-300"
              >
                Inscription gratuite
                <svg className="inline-block w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </Link>
              <Link 
                to="/pricing" 
                className="bg-gray-100 hover:bg-gray-200 text-gray-800 px-8 py-4 rounded-xl font-semibold text-lg shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-300"
              >
                Voir tous les tarifs
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* CSS personnalisé pour les animations */}
      <style jsx>{`
        @keyframes fade-in-up {
          from {
            opacity: 0;
            transform: translateY(30px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes counter {
          from { opacity: 0; transform: scale(0.5); }
          to { opacity: 1; transform: scale(1); }
        }

        .animate-fade-in-up {
          animation: fade-in-up 0.8s ease-out forwards;
          opacity: 0;
        }

        .animate-counter {
          animation: counter 0.6s ease-out forwards;
        }

        /* Hover effects pour les cartes */
        .group:hover .group-hover\\:scale-110 {
          transform: scale(1.1);
        }

        .group:hover .group-hover\\:translate-x-1 {
          transform: translateX(0.25rem);
        }
      `}</style>
    </div>
  );
};

export default HomePage; 