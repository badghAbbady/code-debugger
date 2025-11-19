import sys
import os
import json
import virtual_env
import code_output
import code_correction_agent
import code_correction_apply


VENV_DIR = ".target_venv" 
REQUIREMENTS_PATH = "requirements.txt" 

def run_smart_debugger(target_script_path: str):
    
    target_script_name = os.path.basename(target_script_path)
    
    print(f"\n🤖 Démarrage du Smart Debugger pour : {target_script_name}")
    print("------------------------------------------------------")
    
    python_path = virtual_env.create_and_install_venv(VENV_DIR, REQUIREMENTS_PATH)
    
    if not python_path:
        print("🛑 ARRÊT : Échec de la préparation de l'environnement virtuel.")
        return

    results = code_output.run_target_script(target_script_path)

    if not results["success"]:
        
        error_trace = results["stderr"]

        try:
            with open(target_script_path, 'r') as f:
                target_code = f.read()
        except FileNotFoundError:
            print(f"🛑 ERREUR : Fichier source '{target_script_path}' introuvable.")
            return

        json_correction_str = code_correction_agent.get_correction_from_groq(target_code, error_trace, target_script_name)
        if json_correction_str:
            
            try:
                correction_data = json.loads(json_correction_str)
            except json.JSONDecodeError:
                print("🛑 ARRÊT : L'IA n'a pas renvoyé un format JSON valide.")
                return
            
            explanation = correction_data.get("correction_resume")
            corrected_code = correction_data.get("corrected_code")

            print("\n==============================================")
            print(f"       🧠 ANALYSE IA POUR : {target_script_name} ")
            print("==============================================")
            
            # Afficher la Trace d'Erreur (pour le contexte)
            print("\n🚨 L'erreur capturée est la suivante :")
            print(error_trace) # Affiche la trace d'erreur complète
            
            # Afficher l'Explication de l'IA
            print("\n👉 Voici l'analyse de l'IA (Explication) :")
            print(f"   {explanation}")
            
            # Afficher la Correction Proposée
            print("\n🔧 Voici le code corrigé proposé :")
            print("---------------------------------------------")
            print(corrected_code)
            print("---------------------------------------------")
            
            # --- FIN DE L'AFFICHAGE DE LA CORRECTION ---

            # 4. DEMANDE DE CONFIRMATION
            print("\n-----------------------------------------------------")
            user_confirm = input("Voulez-vous **APPLIQUER** cette correction au fichier ? (oui/non) : ").strip().lower()
            
            if user_confirm == 'oui':
                # Appel de la fonction d'application si confirmation
                code_correction_apply.apply_code_correction(apply_code=True,corrections=json_correction_str)
            else:
                print("❌ Correction non appliquée. Le script original reste inchangé.")
        
    else:
         print("\n✅ Le script a réussi. Aucune erreur détectée.")

# ----------------------------------------------------------------------
## 6. POINT D'ENTRÉE (Lancement via argument de la ligne de commande)
# ----------------------------------------------------------------------

if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print("Usage incorrect.")
        print("Syntaxe correcte : python main.py \"chemin/vers/votre/fichier.py\"")
        sys.exit(1)
        
    file_path_arg = sys.argv[1]
    
    if not os.path.exists(file_path_arg):
        print(f"🛑 ERREUR : Le fichier spécifié '{file_path_arg}' n'existe pas.")
        sys.exit(1)
        
    run_smart_debugger(file_path_arg)