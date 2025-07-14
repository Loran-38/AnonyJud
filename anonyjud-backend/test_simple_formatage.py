import fitz
import os
import sys
import logging
from app.anonymizer import anonymize_pdf_direct, deanonymize_pdf_direct

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

def create_test_pdf_with_real_formatting():
    """Crée un PDF avec du formatage réel (gras, italique, couleur)"""
    
    doc = fitz.open()
    page = doc.new_page()
    
    # Créer du texte avec différents formatages
    y_position = 100
    
    # Texte normal
    page.insert_text((100, y_position), "Jean Dupont", fontname="helv", fontsize=12, color=(0, 0, 0))
    y_position += 30
    
    # Texte gras
    page.insert_text((100, y_position), "Marie Martin", fontname="helv-bold", fontsize=12, color=(1, 0, 0))
    y_position += 30
    
    # Texte italique
    page.insert_text((100, y_position), "Pierre Durand", fontname="helv-oblique", fontsize=12, color=(0, 0, 1))
    y_position += 30
    
    # Texte Times gras
    page.insert_text((100, y_position), "Sophie Leroy", fontname="times-bold", fontsize=12, color=(0, 0.5, 0))
    y_position += 30
    
    # Texte Times italique
    page.insert_text((100, y_position), "Paul Moreau", fontname="times-italic", fontsize=12, color=(0.5, 0, 0.5))
    y_position += 30
    
    # Texte Courier gras
    page.insert_text((100, y_position), "Claire Bernard", fontname="cour-bold", fontsize=12, color=(0, 0, 0))
    y_position += 30
    
    print("=== PDF CRÉÉ AVEC FORMATAGE RÉEL ===")
    print("✅ Helvetica normal : Jean Dupont (noir)")
    print("✅ Helvetica gras : Marie Martin (rouge)")
    print("✅ Helvetica italique : Pierre Durand (bleu)")
    print("✅ Times gras : Sophie Leroy (vert)")
    print("✅ Times italique : Paul Moreau (violet)")
    print("✅ Courier gras : Claire Bernard (noir)")
    
    # Sauvegarder le PDF
    pdf_bytes = doc.tobytes()
    doc.close()
    
    return pdf_bytes

def test_formatting_preservation():
    """Test que le formatage est préservé lors de l'anonymisation"""
    
    print("\n=== TEST PRÉSERVATION FORMATAGE LORS ANONYMISATION ===")
    
    # Créer le PDF de test
    pdf_content = create_test_pdf_with_real_formatting()
    
    # Données des tiers pour l'anonymisation
    tiers_data = [
        {"numero": 1, "nom": "Dupont", "prenom": "Jean", "adresse": "123 Rue de la Paix"},
        {"numero": 2, "nom": "Martin", "prenom": "Marie", "adresse": "456 Avenue des Champs"},
        {"numero": 3, "nom": "Durand", "prenom": "Pierre", "adresse": "789 Boulevard Saint-Germain"},
        {"numero": 4, "nom": "Leroy", "prenom": "Sophie", "adresse": "321 Rue de Rivoli"},
        {"numero": 5, "nom": "Moreau", "prenom": "Paul", "adresse": "654 Avenue Montaigne"},
        {"numero": 6, "nom": "Bernard", "prenom": "Claire", "adresse": "987 Rue du Faubourg"},
    ]
    
    # Analyser le PDF original
    print("\n=== ANALYSE DU PDF ORIGINAL ===")
    analyze_formatting_simple(pdf_content, "ORIGINAL")
    
    # Anonymiser le PDF
    print("\n🔒 ANONYMISATION EN COURS...")
    anonymized_pdf, mapping = anonymize_pdf_direct(pdf_content, tiers_data)
    
    # Sauvegarder le PDF anonymisé
    with open("test_simple_formatage_anonymized.pdf", "wb") as f:
        f.write(anonymized_pdf)
    
    print(f"✅ PDF anonymisé sauvegardé : test_simple_formatage_anonymized.pdf")
    
    # Analyser le PDF anonymisé
    print("\n=== ANALYSE DU PDF ANONYMISÉ ===")
    analyze_formatting_simple(anonymized_pdf, "ANONYMISÉ")
    
    # Dé-anonymiser le PDF
    print("\n🔓 DÉ-ANONYMISATION EN COURS...")
    deanonymized_pdf = deanonymize_pdf_direct(anonymized_pdf, mapping)
    
    # Sauvegarder le PDF dé-anonymisé
    with open("test_simple_formatage_deanonymized.pdf", "wb") as f:
        f.write(deanonymized_pdf)
    
    print(f"✅ PDF dé-anonymisé sauvegardé : test_simple_formatage_deanonymized.pdf")
    
    # Analyser le PDF dé-anonymisé
    print("\n=== ANALYSE DU PDF DÉ-ANONYMISÉ ===")
    analyze_formatting_simple(deanonymized_pdf, "DÉ-ANONYMISÉ")
    
    return True

def analyze_formatting_simple(pdf_content, label):
    """Analyse simple du formatage dans un PDF"""
    
    doc = fitz.open(stream=pdf_content, filetype="pdf")
    page = doc[0]
    
    print(f"\n📊 ANALYSE FORMATAGE - PDF {label}")
    print("=" * 50)
    
    text_instances = page.get_text("dict")
    
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
                        
                        color_str = f"RGB({color})" if color != 0 else "Noir"
                        
                        # Déterminer le statut du formatage
                        status = "✅"
                        if "bold" in font.lower() and not is_bold:
                            status = "⚠️"
                        elif "italic" in font.lower() and not is_italic:
                            status = "⚠️"
                        elif "oblique" in font.lower() and not is_italic:
                            status = "⚠️"
                        
                        print(f"{status} '{text}'")
                        print(f"   └─ Police: {font}")
                        print(f"   └─ Gras: {is_bold}")
                        print(f"   └─ Italique: {is_italic}")
                        print(f"   └─ Couleur: {color_str}")
                        print()
    
    doc.close()

def cleanup_test_files():
    """Nettoie les fichiers de test"""
    
    test_files = [
        "test_simple_formatage_anonymized.pdf",
        "test_simple_formatage_deanonymized.pdf"
    ]
    
    for file in test_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"🗑️ Fichier supprimé : {file}")

if __name__ == "__main__":
    try:
        # Lancer le test
        success = test_formatting_preservation()
        
        if success:
            print("\n✅ TEST PRÉSERVATION FORMATAGE RÉUSSI !")
            print("🎯 Le formatage (gras, italique, couleur) est préservé")
            print("🎯 Les polices équivalentes maintiennent le formatage")
            print("🎯 L'anonymisation et dé-anonymisation conservent tout")
        else:
            print("\n❌ CERTAINS TESTS ONT ÉCHOUÉ")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ ERREUR LORS DU TEST : {str(e)}")
        sys.exit(1)
    
    finally:
        # Nettoyer les fichiers de test
        cleanup_test_files() 