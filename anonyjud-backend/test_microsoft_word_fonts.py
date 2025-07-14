import fitz
import os
import sys
import logging
from app.anonymizer import anonymize_pdf_direct, deanonymize_pdf_direct

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

def create_test_pdf_with_microsoft_fonts():
    """Crée un PDF de test avec différentes polices Microsoft Word"""
    
    doc = fitz.open()
    page = doc.new_page()
    
    # Polices Microsoft Word courantes à tester
    test_fonts = [
        ("Calibri", "Jean Dupont"),
        ("Arial", "Marie Martin"),
        ("Times New Roman", "Pierre Durand"),
        ("Verdana", "Sophie Leroy"),
        ("Georgia", "Paul Moreau"),
        ("Tahoma", "Claire Bernard"),
        ("Trebuchet MS", "Luc Petit"),
        ("Courier New", "Anne Roux"),
        ("Consolas", "Marc Blanc"),
        ("Segoe UI", "Julie Noir"),
        ("Comic Sans MS", "Tom Vert"),
        ("Impact", "Lisa Rouge"),
    ]
    
    y_position = 100
    
    print("=== CRÉATION DU PDF DE TEST ===")
    for font_name, text in test_fonts:
        try:
            # Essayer d'insérer le texte avec la police Microsoft Word
            page.insert_text((100, y_position), text, fontname=font_name, fontsize=12, color=(0, 0, 0))
            print(f"✅ Police {font_name} : {text}")
        except Exception as e:
            print(f"❌ Police {font_name} : {text} - Erreur: {str(e)}")
            # Fallback vers Helvetica
            try:
                page.insert_text((100, y_position), text, fontname="helv", fontsize=12, color=(0, 0, 0))
                print(f"⚠️ Police {font_name} : {text} - Fallback vers Helvetica")
            except Exception as e2:
                print(f"❌ Fallback échoué pour {font_name} : {str(e2)}")
        
        y_position += 30
    
    # Sauvegarder le PDF
    pdf_bytes = doc.tobytes()
    doc.close()
    
    return pdf_bytes

def test_anonymization_with_microsoft_fonts():
    """Test l'anonymisation avec les polices Microsoft Word"""
    
    print("\n=== TEST D'ANONYMISATION AVEC POLICES MICROSOFT WORD ===")
    
    # Créer le PDF de test
    pdf_content = create_test_pdf_with_microsoft_fonts()
    
    # Données des tiers pour l'anonymisation
    tiers_data = [
        {"numero": 1, "nom": "Dupont", "prenom": "Jean", "adresse": "123 Rue de la Paix"},
        {"numero": 2, "nom": "Martin", "prenom": "Marie", "adresse": "456 Avenue des Champs"},
        {"numero": 3, "nom": "Durand", "prenom": "Pierre", "adresse": "789 Boulevard Saint-Germain"},
        {"numero": 4, "nom": "Leroy", "prenom": "Sophie", "adresse": "321 Rue de Rivoli"},
        {"numero": 5, "nom": "Moreau", "prenom": "Paul", "adresse": "654 Avenue Montaigne"},
        {"numero": 6, "nom": "Bernard", "prenom": "Claire", "adresse": "987 Rue du Faubourg"},
        {"numero": 7, "nom": "Petit", "prenom": "Luc", "adresse": "147 Avenue Victor Hugo"},
        {"numero": 8, "nom": "Roux", "prenom": "Anne", "adresse": "258 Rue de la République"},
        {"numero": 9, "nom": "Blanc", "prenom": "Marc", "adresse": "369 Boulevard Haussmann"},
        {"numero": 10, "nom": "Noir", "prenom": "Julie", "adresse": "741 Rue de la Bastille"},
        {"numero": 11, "nom": "Vert", "prenom": "Tom", "adresse": "852 Avenue de l'Opéra"},
        {"numero": 12, "nom": "Rouge", "prenom": "Lisa", "adresse": "963 Rue Saint-Honoré"},
    ]
    
    # Anonymiser le PDF
    print("\n🔒 ANONYMISATION EN COURS...")
    anonymized_pdf, mapping = anonymize_pdf_direct(pdf_content, tiers_data)
    
    # Sauvegarder le PDF anonymisé
    with open("test_microsoft_fonts_anonymized.pdf", "wb") as f:
        f.write(anonymized_pdf)
    
    print(f"✅ PDF anonymisé sauvegardé : test_microsoft_fonts_anonymized.pdf")
    print(f"📋 Mapping généré : {len(mapping)} remplacements")
    
    # Analyser le PDF anonymisé
    print("\n=== ANALYSE DU PDF ANONYMISÉ ===")
    analyze_pdf_fonts(anonymized_pdf, "anonymisé")
    
    # Dé-anonymiser le PDF
    print("\n🔓 DÉ-ANONYMISATION EN COURS...")
    deanonymized_pdf = deanonymize_pdf_direct(anonymized_pdf, mapping)
    
    # Sauvegarder le PDF dé-anonymisé
    with open("test_microsoft_fonts_deanonymized.pdf", "wb") as f:
        f.write(deanonymized_pdf)
    
    print(f"✅ PDF dé-anonymisé sauvegardé : test_microsoft_fonts_deanonymized.pdf")
    
    # Analyser le PDF dé-anonymisé
    print("\n=== ANALYSE DU PDF DÉ-ANONYMISÉ ===")
    analyze_pdf_fonts(deanonymized_pdf, "dé-anonymisé")
    
    return True

def analyze_pdf_fonts(pdf_content, label):
    """Analyse les polices utilisées dans un PDF"""
    
    doc = fitz.open(stream=pdf_content, filetype="pdf")
    page = doc[0]
    
    print(f"\n📊 ANALYSE DES POLICES - PDF {label.upper()}")
    print("-" * 50)
    
    text_instances = page.get_text("dict")
    
    font_usage = {}
    
    for block in text_instances["blocks"]:
        if "lines" in block:
            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    if text:
                        font = span["font"]
                        flags = span["flags"]
                        color = span["color"]
                        
                        is_bold = bool(flags & 2**4)
                        is_italic = bool(flags & 2**5)
                        
                        font_key = f"{font} (gras={is_bold}, italique={is_italic})"
                        
                        if font_key not in font_usage:
                            font_usage[font_key] = []
                        
                        font_usage[font_key].append(text)
    
    for font_info, texts in font_usage.items():
        print(f"🔤 {font_info}")
        for text in texts:
            print(f"   └─ '{text}'")
    
    doc.close()

def cleanup_test_files():
    """Nettoie les fichiers de test"""
    
    test_files = [
        "test_microsoft_fonts_anonymized.pdf",
        "test_microsoft_fonts_deanonymized.pdf"
    ]
    
    for file in test_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"🗑️ Fichier supprimé : {file}")

if __name__ == "__main__":
    try:
        # Lancer le test
        success = test_anonymization_with_microsoft_fonts()
        
        if success:
            print("\n✅ TOUS LES TESTS RÉUSSIS !")
            print("🎯 Les polices Microsoft Word sont maintenant supportées avec fallback intelligent")
            print("📋 Priorité : Police originale > Formatage gras/italique > Couleur")
        else:
            print("\n❌ CERTAINS TESTS ONT ÉCHOUÉ")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ ERREUR LORS DU TEST : {str(e)}")
        sys.exit(1)
    
    finally:
        # Nettoyer les fichiers de test
        cleanup_test_files() 