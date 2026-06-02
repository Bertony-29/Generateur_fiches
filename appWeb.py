from flask import Flask, render_template, request
from Fiches import detection_erreur, supabase_client
import os, json

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def Bienvenue():
    ma_fiche = None
    nomDuFichier = None
    try:
        if request.method == 'POST':
            fichier = request.files["mon_fichier"]
            if fichier.filename != '':
                nomDuFichier = fichier.filename
                contenu = fichier.read().decode("utf-8")
                ma_fiche = detection_erreur(contenu)
    except Exception as e:
        print(f"Erreur dans le lancement de l'appli: {e}")
    return render_template("index.html", fiches=ma_fiche, nom_fichier=nomDuFichier)
    
@app.route("/historique")
def historique():
    fiches = []
    try:
        reponse = supabase_client.table("fiches").select().order("date_creation",desc=True).execute()
        fiches = reponse.data
    
    except Exception as e:
        print(f"Erreur dans l'affichage de l'historique: {e}")
        
    return render_template("historique.html", historique=fiches)












if __name__ == "__main__":
    app.run(debug=True)