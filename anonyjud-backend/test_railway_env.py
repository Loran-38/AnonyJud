#!/usr/bin/env python3
"""
Test de simulation de l'environnement Railway sans pdf-redactor
"""

import sys
import os

# Simuler l'absence de pdf-redactor en empêchant son import
class MockImportError:
    def __init__(self, original_import):
        self.original_import = original_import
    
    def __call__(self, name, *args, **kwargs):
        if name == 'pdf_redactor':
            raise ImportError("No module named 'pdf_redactor'")
        return self.original_import(name, *args, **kwargs)

# Remplacer temporairement la fonction d'import
original_import = __builtins__.__import__
__builtins__.__import__ = MockImportError(original_import)

try:
    print("🧪 TEST: Simulation démarrage Railway sans pdf-redactor")
    print("=" * 60)
    
    # Tenter d'importer l'application
    from app.main import app
    
    print("=" * 60)
    print("✅ SUCCESS: L'application peut démarrer sans pdf-redactor")
    print("📊 État simulé Railway: READY")
    
except Exception as e:
    print("=" * 60)
    print(f"❌ FAIL: Erreur lors du démarrage: {e}")
    print("📊 État simulé Railway: CRASH")
    sys.exit(1)
    
finally:
    # Restaurer l'import original
    __builtins__.__import__ = original_import 