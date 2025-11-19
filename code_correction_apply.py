import json



def apply_code_correction(apply_code:bool , corrections: str) :
    try :
        correction_response = json.loads(corrections)
    except json.JSONDecodeError:
        print (f"ERROR while retreiving correction")

    buggy_script_path = correction_response["script_path"] 
    correction_resume = correction_response["correction_resume"]
    corrected_code = correction_response["corrected_code"]


    if apply_code : 
        try :
            with open(buggy_script_path,"w") as f :
                f.write(corrected_code)
            print("Code est mis à jour avec succées")
        except Exception as e :
            print (f"ERROR while modifying script : {e}")
        
    else :
        print(f"Couldn't modify : {correction_resume}")
        

