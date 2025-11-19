import os
from groq import Groq
from dotenv import load_dotenv
import json
import code_output


def get_correction_from_groq(code_source: str, error_trace: str, target_script_name: str) -> str:
    
    print("\n--- Appel à Groq pour l'analyse ---")
    try:
        load_dotenv()
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    except Exception as e:
        print(f"ERROR API KEY not found {e}")
        return None
    
    with open ('context.txt' , 'r') as f :
        system_prompt = f.read()
    
    # Le User Prompt fournit toutes les données nécessaires à l'analyse
    user_prompt = f"""
    Analysez la trace d'erreur suivante et le code Python.
    
    CODE À CORRIGER (fichier: {target_script_name}):
    ---
    {code_source}
    ---
    
    TRACE D'ERREUR COMPLÈTE:
    ---
    {error_trace}
    ---
    
    Fournissez la correction complète du code Python dans la clé 'corrected_code' et l'explication dans 'explanation'.
    Assurez-vous que la clé 'file_path' est : {target_script_name}
    """

    # 3. Appel API
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="openai/gpt-oss-20b",
            temperature=0.0,
            response_format={"type": "json_object"} 
        )
    
        
        json_text = json.loads(chat_completion.choices[0].message.content)
        print("--> Response recieved from groq")
        return json_text
        
    except Exception as e:
        print(f"ERREUR lors de l'appel à l'API Groq : {e}")
        return None
