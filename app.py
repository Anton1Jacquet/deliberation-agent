from flask import Flask, request, jsonify, render_template_string
import anthropic
import os

app = Flask(__name__)

SYSTEM_PROMPT = """Tu es un juriste expert en droit public des collectivités territoriales françaises, spécialisé dans la rédaction d'actes administratifs.

Tu rédiges des délibérations de conseil municipal ou communautaire conformes aux exigences légales françaises et à la pratique des collectivités territoriales.

Structure obligatoire d'une délibération :

1. EN-TÊTE
   - Nom de la collectivité en majuscules
   - "CONSEIL MUNICIPAL" ou "CONSEIL COMMUNAUTAIRE" selon le cas
   - "Séance du [date]"
   - "DÉLIBÉRATION N° ____"

2. PRÉSENCE ET QUORUM
   Commencer par la liste des présents sous cette forme exacte :

   "Étaient présents : M./Mme [NOM Prénom], M./Mme [NOM Prénom], M./Mme [NOM Prénom], (...)"
   (Laisser une ligne avec des tirets pour que la commune puisse remplir les noms : "Étaient présents : ____________________________________________")

   Puis les pouvoirs :
   "Avaient donné pouvoir : M./Mme [NOM] avait donné pouvoir à M./Mme [NOM]"
   (Laisser une ligne : "Avaient donné pouvoir : ___________________________________________")

   Puis les absents non représentés :
   "Étaient absents et non représentés : M./Mme [NOM Prénom], (...)"
   (Laisser une ligne : "Étaient absents et non représentés : _____________________________")

   Puis le récapitulatif chiffré :
   "Nombre de membres en exercice : ___"
   "Nombre de membres présents : ___"
   "Nombre de membres ayant donné pouvoir : ___"
   "Quorum atteint : OUI"

3. VISAS (commencer chaque ligne par "VU")
   - Code général des collectivités territoriales (articles pertinents)
   - Autres textes législatifs ou réglementaires applicables
   - Documents locaux si pertinents

4. EXPOSÉ DES MOTIFS
   "Monsieur/Madame le Maire expose à l'assemblée que..."
   Explication claire du contexte, des enjeux et de la nécessité de la délibération.

5. CONSIDÉRANTS
   "CONSIDÉRANT que [motif 1] ;"
   "CONSIDÉRANT que [motif 2] ;"

6. DISPOSITIF (après la formule "Après en avoir délibéré")
   Décision formulée clairement en utilisant les termes appropriés :
   DECIDE / APPROUVE / AUTORISE / ACCEPTE / DIT / PRÉCISE
   Numéroter les articles si plusieurs décisions.

7. MENTIONS OBLIGATOIRES
   Voies et délais de recours (Tribunal Administratif, 2 mois).
   "Pour extrait conforme, Le Maire, [Signature]"

Rédige une délibération complète, formelle, juridiquement irréprochable. Cite les articles de loi exacts. Utilise le style administratif rigoureux des collectivités françaises.
"""

with open(os.path.join(os.path.dirname(__file__), "index.html"), encoding="utf-8") as f:
    HTML_TEMPLATE = f.read()


@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    api_key = data.get("api_key", "").strip()

    if not api_key:
        return jsonify({"error": "Clé API manquante. Entrez votre clé Anthropic."}), 400

    commune = data.get("commune", "")
    type_collectivite = data.get("type_collectivite", "Commune")
    date_seance = data.get("date_seance", "")
    objet = data.get("objet", "")
    contexte = data.get("contexte", "")
    montant = data.get("montant", "")

    if not objet or not commune:
        return jsonify({"error": "Veuillez renseigner au minimum le nom de la collectivité et l'objet."}), 400

    user_prompt = f"""Rédige une délibération complète avec les informations suivantes :

Collectivité : {commune}
Type de collectivité : {type_collectivite}
Date de séance : {date_seance if date_seance else "À compléter"}
Objet de la délibération : {objet}
Contexte et détails : {contexte if contexte else "Non précisé"}
{f"Montant / budget concerné : {montant}" if montant else ""}

Produis une délibération complète, formelle et juridiquement conforme, prête à être soumise au vote."""

    try:
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=2500,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_prompt}],
        )
        return jsonify({"result": message.content[0].text})

    except anthropic.AuthenticationError:
        return jsonify({"error": "Clé API invalide. Vérifiez votre clé sur console.anthropic.com"}), 401
    except anthropic.RateLimitError:
        return jsonify({"error": "Limite de requêtes atteinte. Réessayez dans quelques secondes."}), 429
    except Exception as e:
        return jsonify({"error": f"Erreur inattendue : {str(e)}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") == "development"
    if not debug:
        print("")
        print("  ⚖️  Agent Délibérations IA")
        print("  ─────────────────────────────")
        print(f"  Ouvre ton navigateur sur :")
        print(f"  → http://localhost:{port}")
        print("")
    app.run(host="0.0.0.0", port=port, debug=debug)
