import json
import re
import os

def clean_email_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    for email in data:
        # Pulisce mittente: [testo](mailto:email) -> email
        if email.get("mittente"):
            email["mittente"] = re.sub(
                r'\[.*?\]\(mailto:(.*?)\)', 
                r'\1', 
                email["mittente"]
            )
        
        # Pulisce link: [testo](url) -> url
        if email.get("link"):
            email["link"] = re.sub(
                r'\[.*?\]\((.*?)\)', 
                r'\1', 
                email["link"]
            )
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Pulito: {filepath}")

# Esegui su tutti i file nella cartella
folder = "data/legit_emails/"
for filename in os.listdir(folder):
    if filename.endswith(".json"):
        clean_email_json(os.path.join(folder, filename))