import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const PricingPage = () => {
  const { currentUser } = useAuth();

  const plans = [
    {
      name: 'Gratuit',
      price: '0€',
      period: 'pour toujours',
      maxProjects: 1,
      features: [
        '1 projet maximum',
        'Anonymisation texte et fichiers',
        'Formats PDF, Word, ODT',
        'Support par email',
        'Conformité RGPD/IA Act'
      ],
      buttonText: 'Commencer gratuitement',
      buttonStyle: 'bg-gray-100 hover:bg-gray-200 text-gray-800',
      popular: false
    },
    {
      name: 'Standard',
      price: '19,99€',
      period: 'par mois',
      maxProjects: 15,
      features: [
        '15 projets maximum',
        'Anonymisation texte et fichiers',
        'Formats PDF, Word, ODT',
        'Support prioritaire',
        'Conformité RGPD/IA Act',
        'Historique des anonymisations',
        'Export des mappings'
      ],
      buttonText: 'Choisir Standard',
      buttonStyle: 'bg-blue-600 hover:bg-blue-700 text-white',
      popular: true
    },
    {
      name: 'Premium',
      price: '49,99€',
      period: 'par mois',
      maxProjects: 'Illimité',
      features: [
        'Projets illimités',
        'Anonymisation texte et fichiers',
        'Formats PDF, Word, ODT',
        'Support prioritaire 24/7',
        'Conformité RGPD/IA Act',
        'Historique des anonymisations',
        'Export des mappings',
        'API d\'intégration',
        'Gestion d\'équipe',
        'Rapports d\'utilisation'
      ],
      buttonText: 'Choisir Premium',
      buttonStyle: 'bg-purple-600 hover:bg-purple-700 text-white',
      popular: false
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-16">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Tarifs simples et transparents
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Choisissez l'offre qui correspond à vos besoins. 
            Commencez gratuitement, passez à un plan payant quand vous voulez.
          </p>
        </div>

        {/* Pricing Cards */}
        <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto mb-16">
          {plans.map((plan, index) => (
            <div
              key={index}
              className={`bg-white rounded-xl shadow-lg overflow-hidden relative ${
                plan.popular ? 'ring-2 ring-blue-500 scale-105' : ''
              }`}
            >
              {plan.popular && (
                <div className="absolute top-0 left-0 right-0 bg-blue-500 text-white text-center py-2 text-sm font-medium">
                  Le plus populaire
                </div>
              )}
              
              <div className={`p-8 ${plan.popular ? 'pt-12' : ''}`}>
                <h3 className="text-2xl font-bold text-gray-900 mb-2">{plan.name}</h3>
                <div className="mb-6">
                  <span className="text-4xl font-bold text-gray-900">{plan.price}</span>
                  <span className="text-gray-600 ml-2">{plan.period}</span>
                </div>
                
                <div className="mb-6">
                  <p className="text-lg font-medium text-gray-900 mb-4">
                    {typeof plan.maxProjects === 'number' 
                      ? `${plan.maxProjects} projet${plan.maxProjects > 1 ? 's' : ''} maximum`
                      : `${plan.maxProjects} projets`
                    }
                  </p>
                </div>

                <ul className="space-y-3 mb-8">
                  {plan.features.map((feature, featureIndex) => (
                    <li key={featureIndex} className="flex items-start">
                      <svg className="w-5 h-5 text-green-500 mr-3 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                      <span className="text-gray-700">{feature}</span>
                    </li>
                  ))}
                </ul>

                <Link
                  to={currentUser ? "/dashboard" : "/signup"}
                  className={`w-full block text-center py-3 px-6 rounded-lg font-medium transition-colors ${plan.buttonStyle}`}
                >
                  {plan.buttonText}
                </Link>
              </div>
            </div>
          ))}
        </div>

        {/* FAQ Section */}
        <div className="bg-white rounded-xl shadow-lg p-8 max-w-4xl mx-auto">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-8">
            Questions fréquentes
          </h2>
          
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Puis-je changer d'offre à tout moment ?
              </h3>
              <p className="text-gray-600">
                Oui, vous pouvez passer à un plan supérieur ou inférieur à tout moment. 
                Les changements prennent effet immédiatement.
              </p>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Mes données sont-elles sécurisées ?
              </h3>
              <p className="text-gray-600">
                Absolument. Nous utilisons Firebase pour un stockage sécurisé et chiffré. 
                Vos données sont protégées selon les standards RGPD.
              </p>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Que se passe-t-il si je dépasse ma limite de projets ?
              </h3>
              <p className="text-gray-600">
                Vous recevrez une notification et pourrez soit supprimer d'anciens projets, 
                soit passer à un plan supérieur pour continuer.
              </p>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                L'anonymisation est-elle réversible ?
              </h3>
              <p className="text-gray-600">
                Oui, nous conservons un mapping sécurisé qui permet de restaurer les données 
                originales si nécessaire (fonction de dé-anonymisation).
              </p>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Proposez-vous des remises pour les équipes ?
              </h3>
              <p className="text-gray-600">
                Contactez-nous pour discuter des tarifs préférentiels pour les équipes 
                de plus de 10 utilisateurs.
              </p>
            </div>
          </div>
        </div>

        {/* CTA Section */}
        <div className="text-center mt-16">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Prêt à commencer ?
          </h2>
          <p className="text-xl text-gray-600 mb-8">
            Essayez gratuitement, aucune carte de crédit requise
          </p>
          <Link
            to="/signup"
            className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg font-medium transition-colors inline-block"
          >
            Commencer maintenant
          </Link>
        </div>
      </div>
    </div>
  );
};

export default PricingPage; 