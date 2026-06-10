import  os, json, time
from dotenv import load_dotenv
from google import genai
from supabase import Client, create_client


load_dotenv()

try:  
    client = genai.Client()
    url: str = os.getenv("SUPABASE_URL")
    key: str = os.getenv("SUPABASE_KEY")
    supabase_client: Client = create_client(url,key)
except Exception as e:
    print(f"Erreur: {e}")
    exit()

def detection_erreur(textFichier: str, id_utilisateur: str) -> list: # J'ai remplacé nomFichier par textFichier
    try:
        dossier = "mesFiches"
        os.makedirs(dossier, exist_ok=True)
    except Exception as e:
        print(f"Erreur: {e}")    
    
    consigne = f"""Tu es un assistant spécialisé dans l'apprentissage de la programmation informatique.
                    Ton rôle est d'analyser le code fourni et de générer une 'Fiche de Survie' précise et concise pour un étudiant débutant.
                    Ne fais qu'UNE SEULE grande réponse structurée.

                    Structure ta réponse EXACTEMENT comme ceci (en utilisant ces balises) en determinant trois points importants dans le code (syntaxe, variable, ...) :

                    [TITRE] : Nom du concept principal.
                    [LANGAGE] : Le langage de programmation utilisé.
                    [SYNTHESE] : L'essentiel en 2 phrases maximum.
                    [DANGER] : Liste les 2 ou 3 fautes de syntaxe ou de logique les plus courantes sur ce code précis.
                    [SYMPTOME] : Quel message d'erreur s'affiche dans la console quand on fait ces fautes ?
                    [DOC] : Un lien vers la documentation officielle du langage liée au concept. Si il y en a pas, 
                    utiliser une ressource que tu juges pertinante pour comprendre le concept.
                    Réponds uniquement au format JSON, pas en format liste, et avec les clés suivantes : titre, langage, synthese, dangers (liste), symptomes (liste), lien_doc.

                    Voici le code à analyser :
                    {textFichier}    
                    """
                  
    try:
        reponse = client.models.generate_content(model='gemini-2.5-flash',contents=consigne)
        print("Analyse en cours...")
        texte_nettoye = reponse.text.replace('```json', '').replace('```', '').strip()
        donnees = json.loads(texte_nettoye)
        
        if isinstance(donnees, dict):
            if "titre" in donnees:
                fiche = [donnees]
                
            else:
                fiche = list(donnees.values())
        else:
            fiche = donnees            

        for concept in fiche:
            try:
                concept["user_id"] = id_utilisateur
                reponse_bdd = supabase_client.table("fiches").insert(concept).execute()
                print(f"Succès : Le concept '{concept['titre']}' a été sauvegardé dans la base de données.")
            except Exception as ex:
                print(f"Erreur lors de l'insertion du concept: {ex}")    
            
        return fiche
    except Exception as e:
        print(f"Une erreur est survenue lors de l'analyse : {e}")
