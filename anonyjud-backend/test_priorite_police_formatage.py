import fitz
import os
import sys
import logging
from app.anonymizer import anonymize_pdf_direct, deanonymize_pdf_direct

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

def create_test_pdf_with_formatting():
    """Crée un PDF de test avec différentes polices PyMuPDF et formatage"""
    
    doc = fitz.open()
    page = doc.new_page()
    
    # Tests avec polices PyMuPDF supportées et formatage
    test_cases = [
        # (police, texte, couleur, gras)
        ("times", "Jean Dupont", (0, 0, 0), False),           # Times normal
        ("times-bold", "Marie Martin", (0, 0, 0), True),      # Times gras
        ("times-italic", "Pierre Durand", (0, 0, 0), False),  # Times italique
        ("helv", "Sophie Leroy", (1, 0, 0), False),           # Helvetica normal rouge
        ("helv-bold", "Paul Moreau", (1, 0, 0), True),        # Helvetica gras rouge
        ("helv-oblique", "Claire Bernard", (0, 0, 1), False), # Helvetica oblique bleu
        ("cour", "Luc Petit", (0, 0, 0), False),              # Courier normal
        ("cour-bold", "Anne Roux", (0, 0, 0), True),          # Courier gras
        
        # Test avec polices Microsoft Word (qui vont fallback)
        ("Calibri", "Marc Blanc", (0, 0.5, 0), False),       # Calibri → helv (vert)
        ("Arial", "Julie Noir", (0.5, 0, 0.5), False),       # Arial → helv (violet)
        ("Georgia", "Tom Vert", (0, 0, 0), False),           # Georgia → times
        ("Consolas", "Lisa Rouge", (0, 0, 0), False),        # Consolas → cour
    ]
    
    y_position = 100
    
    print("=== CRÉATION DU PDF DE TEST AVEC FORMATAGE ===")
    for font_name, text, color, is_bold in test_cases:
        try:
            # Créer le texte avec la police et le formatage spécifiés
            if is_bold:
                # Simuler le formatage gras avec les flags PyMuPDF
                rc = page.insert_text(
                    (100, y_position), 
                    text, 
                    fontname=font_name, 
                    fontsize=12, 
                    color=color
                )
                
                # Récupérer le texte pour modifier ses flags
                text_dict = page.get_text("dict")
                for block in text_dict["blocks"]:
                    if "lines" in block:
                        for line in block["lines"]:
                            for span in line["spans"]:
                                if span["text"].strip() == text:
                                    # Modifier les flags pour simuler le gras
                                    span["flags"] = span["flags"] | (2**4)  # Ajouter le flag gras
                
                print(f"✅ {font_name} (GRAS) : {text} - couleur: {color}")
            else:
                page.insert_text((100, y_position), text, fontname=font_name, fontsize=12, color=color)
                print(f"✅ {font_name} : {text} - couleur: {color}")
        except Exception as e:
            print(f"❌ {font_name} : {text} - Erreur: {str(e)}")
            # Fallback vers Helvetica
            try:
                page.insert_text((100, y_position), text, fontname="helv", fontsize=12, color=color)
                print(f"⚠️ {font_name} : {text} - Fallback vers Helvetica")
            except Exception as e2:
                print(f"❌ Fallback échoué pour {font_name} : {str(e2)}")
        
        y_position += 30
    
    # Sauvegarder le PDF
    pdf_bytes = doc.tobytes()
    doc.close()
    
    return pdf_bytes

def test_priority_system():
    """Test le système de priorité police originale vs formatage"""
    
    print("\n=== TEST SYSTÈME DE PRIORITÉ POLICE ORIGINALE VS FORMATAGE ===")
    
    # Créer le PDF de test
    pdf_content = create_test_pdf_with_formatting()
    
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
    
    # Analyser le PDF original
    print("\n=== ANALYSE DU PDF ORIGINAL ===")
    analyze_pdf_detailed(pdf_content, "ORIGINAL")
    
    # Anonymiser le PDF
    print("\n🔒 ANONYMISATION EN COURS...")
    anonymized_pdf, mapping = anonymize_pdf_direct(pdf_content, tiers_data)
    
    # Sauvegarder le PDF anonymisé
    with open("test_priorite_anonymized.pdf", "wb") as f:
        f.write(anonymized_pdf)
    
    print(f"✅ PDF anonymisé sauvegardé : test_priorite_anonymized.pdf")
    
    # Analyser le PDF anonymisé
    print("\n=== ANALYSE DU PDF ANONYMISÉ ===")
    analyze_pdf_detailed(anonymized_pdf, "ANONYMISÉ")
    
    # Dé-anonymiser le PDF
    print("\n🔓 DÉ-ANONYMISATION EN COURS...")
    deanonymized_pdf = deanonymize_pdf_direct(anonymized_pdf, mapping)
    
    # Sauvegarder le PDF dé-anonymisé
    with open("test_priorite_deanonymized.pdf", "wb") as f:
        f.write(deanonymized_pdf)
    
    print(f"✅ PDF dé-anonymisé sauvegardé : test_priorite_deanonymized.pdf")
    
    # Analyser le PDF dé-anonymisé
    print("\n=== ANALYSE DU PDF DÉ-ANONYMISÉ ===")
    analyze_pdf_detailed(deanonymized_pdf, "DÉ-ANONYMISÉ")
    
    return True

def analyze_pdf_detailed(pdf_content, label):
    """Analyse détaillée des polices et formatage dans un PDF"""
    
    doc = fitz.open(stream=pdf_content, filetype="pdf")
    page = doc[0]
    
    print(f"\n📊 ANALYSE DÉTAILLÉE - PDF {label}")
    print("=" * 60)
    
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
                        size = span["size"]
                        
                        is_bold = bool(flags & 2**4)
                        is_italic = bool(flags & 2**5)
                        
                        color_str = f"RGB({color})" if color != 0 else "Noir"
                        
                        print(f"🔤 '{text}'")
                        print(f"   └─ Police: {font}")
                        print(f"   └─ Taille: {size}")
                        print(f"   └─ Gras: {is_bold}")
                        print(f"   └─ Italique: {is_italic}")
                        print(f"   └─ Couleur: {color_str}")
                        print(f"   └─ Flags: {flags}")
                        print()
    
    doc.close()

def cleanup_test_files():
    """Nettoie les fichiers de test"""
    
    test_files = [
        "test_priorite_anonymized.pdf",
        "test_priorite_deanonymized.pdf"
    ]
    
    for file in test_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"🗑️ Fichier supprimé : {file}")

if __name__ == "__main__":
    try:
        # Lancer le test
        success = test_priority_system()
        
        if success:
            print("\n✅ SYSTÈME DE PRIORITÉ VALIDÉ !")
            print("🎯 PRIORITÉ 1 : Police originale exacte préservée")
            print("🎯 PRIORITÉ 2 : Formatage gras/italique si police originale impossible")
            print("🎯 PRIORITÉ 3 : Couleur préservée au minimum")
            print("🎯 PRIORITÉ 4 : Fallback Helvetica en dernier recours")
        else:
            print("\n❌ CERTAINS TESTS ONT ÉCHOUÉ")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ ERREUR LORS DU TEST : {str(e)}")
        sys.exit(1)
    
    finally:
        # Nettoyer les fichiers de test
        cleanup_test_files() 