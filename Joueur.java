package monde1;
/**
 * Représente un joueur dans le jeu avec un nom unique et un score.
 * Cette classe gère l'évolution du score et assure l'immuabilité du nom.
 * * @author Bertony
 * @version 1.0
 */
public class Joueur {

	private final String nom;
	private int score, vie;
	private static int nbrJoueur = 0;
	
	// Constructeurs
	/**
	 * Crée un nouveau joueur avec un score initial de zéro.
	 * Si le nom fourni est vide, un nom par défaut (JoueurX) est attribué automatiquement.
	 * @param nom Le nom du joueur. S'il est vide (""), un nom générique est généré.
	 */
	public Joueur(String nom)
	{
		if (nbrJoueur == 0)
		{	
			System.out.println("Nombre de joueurs créés: "+ nbrJoueur);
		}
		nbrJoueur++;
		
		if (nom == null || nom.isEmpty()) 
			this.nom = "Joueur"+nbrJoueur;
		else	
			this.nom = nom;
		this.score = 0;
		this.vie = 5;
	}
	
	// getters
	/**
	 * Retourne le nom du joueur.
	 * @return Le nom du joueur inchangeable.
	 */
	public String getNom() { return this.nom; }
	/**
	 * Retourne le nombre de points accumulés par le joueur.
	 * @return Le score du joueur.
	 */
	public int getScore() { return this.score; }
	/**
	 * Retourne le nombre de joueurs crées depuis le début du programme.
	 * @return Le nombre de joueurs crées.
	 */
	public static int getNbrJoueur() { return nbrJoueur; }
	
	/**
	 * Retourne le nombre de vie restantes du joueur.
	 * @return Le nombre de vie.
	 */
	public int getVie() { return this.vie; }
	// Méthodes
	
	/**
	 * affiche dans la console le nombre de joueurs crées.
	 */
	public static void afficherJoueurs() {
		System.out.println("Nombre de joueurs : " + nbrJoueur);
	}
	/**
	 * Ajoute un nombre de points au score du joueur.
	 * @param pts le nombre de points à ajouter (doit être positif)
	 */
	public void ajouterDesPoints(int pts) {
		this.score += pts;
	}
	/**
	 * Retire un nombre de points au score du joueur.
	 * Si le montant à retirer est supérieur au score actuel, le score est mis à 0.
	 *  @param pts Le nombre de points à soustraire (doit être positif).
	 */
	public void enleverDesPoints(int pts) {
		if (pts >= this.score) {
			this.score = 0;
		}
		else {
			this.score -= pts;
		}
	}
	
	/**
	 * Retire un nombre de vie aux joueurs.
	 * @param v Le nombre de vie à retirer.
	 */
	public void enleverDesVies(int v) {
		if (v >= this.vie) {
			this.vie = 0;
		}
		else {
			this.vie -= v;
		}
	}
	
	/**
     * Fournit une représentation textuelle du joueur sous forme de chaîne.
     * @return Une chaîne au format "nom : score pts" avec gestion du pluriel.
     */
	public String toString() {
		if (this.score <= 1)
			return this.nom +" : "+ this.score +" pt" ;
		else
			return this.nom +" : "+ this.score +" pts" ;
		
	}
	/**
	 * Réinitialise les vies et le score du joueur lorsqu'il recommence le niveau.
	 */
	public void reinitialiser() {
		vie = 5;
		score = 0;
	}
	
	/**
	 * Vérifie si deux joueurs sont identiques.
	 * L'égalité est basée sur le nom, sans tenir compte de la casse.
	 *  @param obj L'objet à comparer avec le joueur courant.
	 * @return true si les noms sont les mêmes, false sinon.
	 */
	public boolean equals(Object obj) {
		if (obj == this)
			return true;
		else if (obj instanceof Joueur) {
			Joueur objJoueur = (Joueur) obj;
			if (objJoueur.nom.compareToIgnoreCase(this.nom) == 0)
				return true;
		}
		return false;
	}
}
