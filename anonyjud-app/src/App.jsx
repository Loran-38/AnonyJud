import React, { Suspense, lazy } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Navbar from './components/Navbar';
import './index.css';

// Lazy loading des composants de page
const HomePage = lazy(() => import('./pages/HomePage'));
const PricingPage = lazy(() => import('./pages/PricingPage'));
const SignupPage = lazy(() => import('./pages/SignupPage'));
const LoginPage = lazy(() => import('./pages/LoginPage'));
const DashboardPage = lazy(() => import('./pages/DashboardPage'));
const AccountPage = lazy(() => import('./pages/AccountPage'));
const ForgotPasswordPage = lazy(() => import('./pages/ForgotPasswordPage'));

// Composant de loading
const LoadingSpinner = () => (
  <div className="min-h-screen flex items-center justify-center">
    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
  </div>
);

// Composant pour protéger les routes privées
function PrivateRoute({ children }) {
  const { currentUser } = useAuth();
  return currentUser ? children : <Navigate to="/login" />;
}

// Composant pour rediriger les utilisateurs connectés
function PublicRoute({ children }) {
  const { currentUser } = useAuth();
  return !currentUser ? children : <Navigate to="/dashboard" />;
}

function AppContent() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <Suspense fallback={<LoadingSpinner />}>
          <Routes>
            {/* Routes publiques */}
            <Route path="/" element={<HomePage />} />
            <Route path="/pricing" element={<PricingPage />} />
            
            {/* Routes d'authentification */}
            <Route 
              path="/signup" 
              element={
                <PublicRoute>
                  <SignupPage />
                </PublicRoute>
              } 
            />
            <Route 
              path="/login" 
              element={
                <PublicRoute>
                  <LoginPage />
                </PublicRoute>
              } 
            />
            <Route 
              path="/forgot-password" 
              element={
                <PublicRoute>
                  <ForgotPasswordPage />
                </PublicRoute>
              } 
            />
            
            {/* Routes privées */}
            <Route 
              path="/dashboard" 
              element={
                <PrivateRoute>
                  <DashboardPage />
                </PrivateRoute>
              } 
            />
            <Route 
              path="/account" 
              element={
                <PrivateRoute>
                  <AccountPage />
                </PrivateRoute>
              } 
            />
            
            {/* Redirection par défaut */}
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </Suspense>
      </div>
    </Router>
  );
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App; 