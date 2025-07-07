import { sendPasswordResetEmail } from 'firebase/auth';
import { auth } from '../firebase/config';

// Configuration des paramètres d'email personnalisés
const actionCodeSettings = {
  // URL de redirection après réinitialisation
  url: `${window.location.origin}/login`,
  // Gestion du code dans l'app
  handleCodeInApp: false,
};

// Template HTML pour l'email de réinitialisation
export const customEmailTemplate = {
  subject: 'Réinitialisation de votre mot de passe AnonyJud',
  html: `
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Réinitialisation de mot de passe - AnonyJud</title>
      <style>
        body {
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
          line-height: 1.6;
          color: #333;
          max-width: 600px;
          margin: 0 auto;
          padding: 20px;
          background-color: #f8fafc;
        }
        .container {
          background-color: white;
          border-radius: 12px;
          box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
          overflow: hidden;
        }
        .header {
          background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
          color: white;
          padding: 30px;
          text-align: center;
        }
        .logo {
          font-size: 28px;
          font-weight: bold;
          margin-bottom: 10px;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 10px;
        }
        .shield-icon {
          width: 32px;
          height: 32px;
          background-color: rgba(255, 255, 255, 0.2);
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
        }
        .content {
          padding: 40px 30px;
        }
        .title {
          font-size: 24px;
          font-weight: 600;
          color: #1f2937;
          margin-bottom: 20px;
        }
        .message {
          font-size: 16px;
          color: #6b7280;
          margin-bottom: 30px;
          line-height: 1.7;
        }
        .button {
          display: inline-block;
          background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
          color: white;
          padding: 16px 32px;
          text-decoration: none;
          border-radius: 8px;
          font-weight: 600;
          font-size: 16px;
          text-align: center;
          margin: 20px 0;
          box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
          transition: all 0.3s ease;
        }
        .button:hover {
          transform: translateY(-2px);
          box-shadow: 0 6px 16px rgba(37, 99, 235, 0.4);
        }
        .security-note {
          background-color: #f3f4f6;
          border-left: 4px solid #2563eb;
          padding: 20px;
          margin: 30px 0;
          border-radius: 0 8px 8px 0;
        }
        .security-title {
          font-weight: 600;
          color: #1f2937;
          margin-bottom: 10px;
          display: flex;
          align-items: center;
          gap: 8px;
        }
        .security-text {
          color: #6b7280;
          font-size: 14px;
        }
        .footer {
          background-color: #f9fafb;
          padding: 30px;
          text-align: center;
          border-top: 1px solid #e5e7eb;
        }
        .footer-text {
          color: #6b7280;
          font-size: 14px;
          margin-bottom: 15px;
        }
        .footer-links {
          display: flex;
          justify-content: center;
          gap: 20px;
          flex-wrap: wrap;
        }
        .footer-link {
          color: #2563eb;
          text-decoration: none;
          font-size: 14px;
        }
        .footer-link:hover {
          text-decoration: underline;
        }
        .divider {
          height: 1px;
          background: linear-gradient(to right, transparent, #e5e7eb, transparent);
          margin: 30px 0;
        }
        @media (max-width: 600px) {
          body {
            padding: 10px;
          }
          .content {
            padding: 30px 20px;
          }
          .header {
            padding: 25px 20px;
          }
          .footer {
            padding: 25px 20px;
          }
        }
      </style>
    </head>
    <body>
      <div class="container">
        <!-- Header -->
        <div class="header">
          <div class="logo">
            <div class="shield-icon">🛡️</div>
            AnonyJud
          </div>
          <p style="margin: 0; opacity: 0.9;">Anonymisation de documents juridiques</p>
        </div>

        <!-- Content -->
        <div class="content">
          <h1 class="title">Réinitialisation de votre mot de passe</h1>
          
          <p class="message">
            Bonjour,<br><br>
            Vous avez demandé la réinitialisation de votre mot de passe pour votre compte AnonyJud. 
            Cliquez sur le bouton ci-dessous pour créer un nouveau mot de passe sécurisé.
          </p>

                     <div style="text-align: center;">
             <a href="%LINK%" class="button">
               Réinitialiser mon mot de passe
             </a>
           </div>

          <div class="security-note">
            <div class="security-title">
              🔒 Sécurité et confidentialité
            </div>
            <div class="security-text">
              • Ce lien expire dans <strong>1 heure</strong> pour votre sécurité<br>
              • Si vous n'avez pas demandé cette réinitialisation, ignorez cet email<br>
              • Votre compte reste sécurisé jusqu'à ce que vous cliquiez sur le lien<br>
              • Créez un mot de passe fort avec au moins 8 caractères
            </div>
          </div>

          <div class="divider"></div>

          <p class="message">
            <strong>Pourquoi AnonyJud ?</strong><br>
            Avec l'IA Act et le RGPD, l'anonymisation des documents juridiques est devenue essentielle. 
            AnonyJud vous aide à protéger les données personnelles de vos clients tout en respectant 
            la réglementation européenne.
          </p>
        </div>

        <!-- Footer -->
        <div class="footer">
          <p class="footer-text">
            Cet email a été envoyé par AnonyJud - Solution d'anonymisation juridique
          </p>
          
                     <div class="footer-links">
             <a href="https://anonyjud-app-production.up.railway.app" class="footer-link">Accueil</a>
             <a href="https://anonyjud-app-production.up.railway.app/pricing" class="footer-link">Tarifs</a>
             <a href="mailto:support@anonyjud.com" class="footer-link">Support</a>
           </div>
          
          <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid #e5e7eb;">
                         <p style="color: #9ca3af; font-size: 12px; margin: 0;">
               Si vous avez des difficultés avec le bouton, copiez et collez ce lien dans votre navigateur :<br>
               <span style="word-break: break-all; color: #2563eb;">%LINK%</span>
             </p>
          </div>
        </div>
      </div>
    </body>
    </html>
  `
};

// Service pour envoyer l'email de réinitialisation
export const sendCustomPasswordResetEmail = async (email) => {
  try {
    await sendPasswordResetEmail(auth, email, actionCodeSettings);
    return { success: true, message: 'Email de réinitialisation envoyé avec succès' };
  } catch (error) {
    console.error('Erreur envoi email:', error);
    
    let errorMessage = 'Une erreur est survenue lors de l\'envoi de l\'email.';
    
    switch (error.code) {
      case 'auth/user-not-found':
        errorMessage = 'Aucun compte n\'existe avec cette adresse email.';
        break;
      case 'auth/invalid-email':
        errorMessage = 'L\'adresse email n\'est pas valide.';
        break;
      case 'auth/too-many-requests':
        errorMessage = 'Trop de tentatives. Veuillez réessayer plus tard.';
        break;
      case 'auth/network-request-failed':
        errorMessage = 'Erreur de connexion. Vérifiez votre connexion internet.';
        break;
      default:
        errorMessage = 'Une erreur inattendue est survenue. Veuillez réessayer.';
    }
    
    return { success: false, error: errorMessage };
  }
};

// Configuration pour Firebase Auth (à utiliser dans la console Firebase)
export const firebaseAuthConfig = {
  // Template d'email personnalisé pour la réinitialisation de mot de passe
  passwordReset: {
    subject: 'Réinitialisation de votre mot de passe AnonyJud',
    senderName: 'AnonyJud',
    replyTo: 'support@anonyjud.com',
    customDomain: window.location.origin,
  }
};

const emailService = {
  sendCustomPasswordResetEmail,
  customEmailTemplate,
  firebaseAuthConfig
};

export default emailService; 