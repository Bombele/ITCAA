import sys

DEPENDENCIES = [
    "torch",
    "transformers",
    "sentence_transformers",
    "faiss",
    "scikit_learn"
]

missing = []
for dep in DEPENDENCIES:
    try:
        __import__(dep)
        print(f"✅ {dep} disponible")
    except ImportError:
        print(f"❌ {dep} manquant")
        missing.append(dep)

if missing:
    sys.exit(1)
else:
    print("✅ Audit IA réussi")