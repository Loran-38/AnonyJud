import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Navbar = () => {
  const { currentUser, userProfile, logout, PLANS } = useAuth();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const location = useLocation();

  const handleLogout = async () => {
    try {
      await logout();
    } catch (error) {
      console.error('Erreur lors de la déconnexion:', error);
    }
  };

  const isActive = (path) => location.pathname === path;

  return (
    <nav className="bg-white shadow-lg">
      <div className="w-full px-4">
        <div className="flex items-center justify-between py-4">
          {/* Logo à gauche */}
          <div className="flex items-center space-x-3">
            <Link to="/" className="flex items-center space-x-2">
              <img 
                src="/logo-anonym-ia.png" 
                alt="Anonym-IA Logo" 
                className="w-8 h-8 object-contain"
                onError={(e) => {
                  // Fallback vers l'icône SVG si l'image n'est pas trouvée
                  e.target.style.display = 'none';
                  e.target.nextElementSibling.style.display = 'block';
                }}
              />
              <svg className="w-8 h-8 text-blue-600 hidden" fill="currentColor" viewBox="0 0 24 24">
                <path d="M9.4 16.6L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0L19.2 12l-4.6-4.6L16 6l6 6-6 6-1.4-1.4z"/>
              </svg>
              <span className="text-2xl font-bold text-blue-600">Anonym-IA</span>
            </Link>
          </div>

          {/* Navigation centrale */}
          <div className="hidden md:flex items-center space-x-8">
            <Link
              to="/"
              className={`text-gray-700 hover:text-blue-600 transition-colors font-medium ${
                isActive('/') ? 'text-blue-600 border-b-2 border-blue-600 pb-1' : ''
              }`}
            >
              Accueil
            </Link>
            <Link
              to="/pricing"
              className={`text-gray-700 hover:text-blue-600 transition-colors font-medium ${
                isActive('/pricing') ? 'text-blue-600 border-b-2 border-blue-600 pb-1' : ''
              }`}
            >
              Tarifs
            </Link>
            {currentUser && (
              <Link
                to="/dashboard"
                className={`text-gray-700 hover:text-blue-600 transition-colors font-medium ${
                  isActive('/dashboard') ? 'text-blue-600 border-b-2 border-blue-600 pb-1' : ''
                }`}
              >
                Dashboard
              </Link>
            )}
          </div>

          {/* Compte et actions à droite */}
          <div className="hidden md:flex items-center space-x-4">
            {currentUser ? (
              <div className="flex items-center space-x-3">
                {/* Info utilisateur */}
                <Link 
                  to="/account"
                  className="flex items-center space-x-2 bg-gray-50 hover:bg-gray-100 rounded-lg px-3 py-2 transition-colors"
                >
                  <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                    <span className="text-white font-medium text-sm">
                      {(currentUser.displayName || 'U').charAt(0).toUpperCase()}
                    </span>
                  </div>
                  <div className="text-sm">
                    <p className="font-medium text-gray-900">
                      {currentUser.displayName || 'Utilisateur'}
                    </p>
                    {userProfile && (
                      <p className="text-gray-600 text-xs">
                        Plan {PLANS[userProfile.plan]?.name || 'Gratuit'}
                      </p>
                    )}
                  </div>
                </Link>
                
                {/* Bouton déconnexion */}
                <button
                  onClick={handleLogout}
                  className="bg-gray-100 hover:bg-gray-200 text-gray-800 px-4 py-2 rounded-lg text-sm font-medium transition-colors"
                >
                  Déconnexion
                </button>
              </div>
            ) : (
              <div className="flex items-center space-x-3">
                <Link
                  to="/login"
                  className="text-gray-700 hover:text-blue-600 transition-colors font-medium"
                >
                  Connexion
                </Link>
                <Link
                  to="/signup"
                  className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium transition-colors"
                >
                  Inscription
                </Link>
              </div>
            )}
          </div>

          {/* Menu Mobile Button */}
          <button
            className="md:hidden text-gray-700"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>

        {/* Menu Mobile */}
        {isMenuOpen && (
          <div className="md:hidden py-4 border-t bg-gray-50">
            <div className="flex flex-col space-y-3">
              {/* Navigation */}
              <div className="space-y-2">
                <Link
                  to="/"
                  className={`block px-3 py-2 rounded-lg text-gray-700 hover:text-blue-600 hover:bg-white transition-colors ${
                    isActive('/') ? 'text-blue-600 bg-white font-medium' : ''
                  }`}
                  onClick={() => setIsMenuOpen(false)}
                >
                  Accueil
                </Link>
                <Link
                  to="/pricing"
                  className={`block px-3 py-2 rounded-lg text-gray-700 hover:text-blue-600 hover:bg-white transition-colors ${
                    isActive('/pricing') ? 'text-blue-600 bg-white font-medium' : ''
                  }`}
                  onClick={() => setIsMenuOpen(false)}
                >
                  Tarifs
                </Link>
                {currentUser && (
                  <Link
                    to="/dashboard"
                    className={`block px-3 py-2 rounded-lg text-gray-700 hover:text-blue-600 hover:bg-white transition-colors ${
                      isActive('/dashboard') ? 'text-blue-600 bg-white font-medium' : ''
                    }`}
                    onClick={() => setIsMenuOpen(false)}
                  >
                    Dashboard
                  </Link>
                )}
              </div>

              {/* Compte */}
              <div className="pt-3 border-t border-gray-200">
                {currentUser ? (
                  <div className="space-y-3">
                    <Link 
                      to="/account"
                      className="flex items-center space-x-3 px-3 py-2 bg-white hover:bg-gray-50 rounded-lg transition-colors"
                      onClick={() => setIsMenuOpen(false)}
                    >
                      <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                        <span className="text-white font-medium text-sm">
                          {(currentUser.displayName || 'U').charAt(0).toUpperCase()}
                        </span>
                      </div>
                      <div className="flex-1">
                        <p className="font-medium text-gray-900 text-sm">
                          {currentUser.displayName || 'Utilisateur'}
                        </p>
                        {userProfile && (
                          <p className="text-gray-600 text-xs">
                            Plan {PLANS[userProfile.plan]?.name || 'Gratuit'}
                          </p>
                        )}
                      </div>
                    </Link>
                    <button
                      onClick={() => {
                        handleLogout();
                        setIsMenuOpen(false);
                      }}
                      className="w-full bg-gray-100 hover:bg-gray-200 text-gray-800 px-4 py-2 rounded-lg text-sm font-medium transition-colors"
                    >
                      Déconnexion
                    </button>
                  </div>
                ) : (
                  <div className="space-y-2">
                    <Link
                      to="/login"
                      className="block px-3 py-2 rounded-lg text-gray-700 hover:text-blue-600 hover:bg-white transition-colors font-medium"
                      onClick={() => setIsMenuOpen(false)}
                    >
                      Connexion
                    </Link>
                    <Link
                      to="/signup"
                      className="block bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium transition-colors text-center"
                      onClick={() => setIsMenuOpen(false)}
                    >
                      Inscription
                    </Link>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar; 