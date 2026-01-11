"""Configuration for the LLM Council."""

import requests

# Demander les IPs au démarrage
print("=" * 50)
print("Configuration des adresses IP des modèles")
print("=" * 50)

ip_model_1 = input("Entrez l'IP pour le modèle 1 (port 8002): ").strip()
ip_model_2 = input("Entrez l'IP pour le modèle 2 (port 8003): ").strip()
ip_chairman = input("Entrez l'IP pour le Chairman (port 8004): ").strip()

print("\nDétection des modèles en cours...")

# Fonction pour récupérer le nom du modèle depuis l'endpoint
def get_model_name(base_url):
    # Extraire l'IP et le port de l'URL /api/query
    info_url = base_url.replace('/api/query', '/')
    try:
        response = requests.get(info_url, timeout=5)
        data = response.json()
        # La réponse contient {"status":"ok","model":"llama3.2:1b","type":"Council Member 1"}
        return data.get('model', 'unknown')
    except Exception as e:
        print(f"⚠️  Erreur lors de la détection pour {info_url}: {e}")
        return "unknown"

# Construire les URLs
url_1 = f"http://{ip_model_1}:8002/api/query"
url_2 = f"http://{ip_model_2}:8003/api/query"
url_chairman = f"http://{ip_chairman}:8004/api/query"

# Détecter les noms des modèles
model_name_1 = get_model_name(url_1)
model_name_2 = get_model_name(url_2)
chairman_model_name = get_model_name(url_chairman)

print(f"\n✓ {model_name_1} -> {url_1}")
print(f"✓ {model_name_2} -> {url_2}")
print(f"✓ Chairman: {chairman_model_name} -> {url_chairman}")
print("=" * 50)
print()

# Council members with mapping to their endpoint
COUNCIL_MODELS = [
    url_1,
    url_2,
]

COUNCIL_MODEL_NAMES = {
    url_1: model_name_1,
    url_2: model_name_2,
}

# Chairman model - synthesizes final response
CHAIRMAN_ENDPOINT = url_chairman
CHAIRMAN_MODEL_NAME = chairman_model_name


