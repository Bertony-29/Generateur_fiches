from flask import Flask, render_template, request, session, redirect, flash
from Fiches import detection_erreur, supabase_client
import os, json

app = Flask(__name__)
app.secret_key = "One_for_all_full_cowl_100_%"

@app.route("/", methods=["GET","POST"])
def Bienvenue():
    if not session.get("utilisateur"):
        return redirect("/login")
    

    ma_fiche = None
    nomDuFichier = None
    id_actuel = session.get("utilisateur")
    try:
        if request.method == 'POST':
            fichier = request.files["mon_fichier"]
            if fichier.filename != '':
                nomDuFichier = fichier.filename
                contenu = fichier.read().decode("utf-8")
                ma_fiche = detection_erreur(contenu, id_actuel)
    except Exception as e:
        print(f"Erreur dans le lancement de l'appli: {e}")
    return render_template("index.html", fiches=ma_fiche, nom_fichier=nomDuFichier)
    
@app.route("/history")
def Historique():
    fiches = []
    if not session.get("utilisateur"):
        return redirect("/login")
    
    try:
        id_actuel = session.get("utilisateur")
        
        reponse = supabase_client.table("fiches").select().eq("user_id",id_actuel).order("date_creation",desc=True).execute()
        langages_disponibles = []
        for fiche in reponse.data:
            if fiche['langage'] not in langages_disponibles:
                langages_disponibles.append(fiche['langage'])
            else:
                continue 
        langage = request.args.get('lang')    
        if langage :
            reponse_filtre = reponse = supabase_client.table("fiches").select().eq("user_id",id_actuel).eq("langage",langage).order("date_creation",desc=True).execute()
            fiches = reponse_filtre.data
        else:
            reponse = supabase_client.table("fiches").select().eq("user_id",id_actuel).order("date_creation",desc=True).execute()
            fiches = reponse.data
        
    except Exception as e:
        print(f"Erreur dans l'affichage de l'historique: {e}")
        
    return render_template("historique.html", historique=fiches, langages_dispos=langages_disponibles)

@app.route("/login", methods=["GET","POST"])
def Connexion():
    if request.method == 'POST':
        user_email = request.form.get("email")
        user_password = request.form.get("password")
        try:
            connexion = supabase_client.auth.sign_in_with_password(
                {
                    "email":user_email, 
                    "password": user_password
                })
            id_utilisateur = connexion.user.id
            session["utilisateur"] = id_utilisateur
            return redirect("/")
        except Exception as e:
            flash("Indentifiants incorrects !")
            print(f"Erreur de connexion: {e}")  
            return redirect("/login")  
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def Inscription():
    if request.method == 'POST':
        user_email = request.form.get("email")
        user_password = request.form.get("password")
        try:
            inscription = supabase_client.auth.sign_up(
                {
                    "email": user_email,
                    "password": user_password
                 })
            return redirect("/login")
        except Exception as e :
            flash("Erreur lors de l'inscription !")  
            print(f"Erreur lors de l'inscription: {e}")  
            return redirect("/register")
    return render_template("register.html")


@app.route("/logout")
def Deconnexion():
    session.clear()
    return redirect("/login")


@app.route("/delete/<id_fiche>")
def Supprimer(id_fiche):
    if not session.get("utilisateur"):
        return redirect("/login")
    
    try:
        id_actuel = session.get("utilisateur")
        suppression = supabase_client.table("fiches").delete().eq("id",id_fiche).eq("user_id",id_actuel).execute()
        return redirect("/history")
    except Exception as e:
        flash("Erreur lors de la suppression !")  
        print(f"Erreur lors de la suppression: {e}")  
        return redirect("/history")



if __name__ == "__main__":
    app.run(debug=True)