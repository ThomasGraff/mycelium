from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import yaml
import os

router = APIRouter()

# Fonction pour lire le fichier YAML et le convertir en JSON
def read_yaml_template():
    file_path = "/workspaces/mycelium/templates/base.yaml" 
    if not os.path.exists(file_path):
        raise FileNotFoundError("Le fichier YAML n'a pas été trouvé.")
    
    with open(file_path, "r") as file:
        try:
            yaml_content = yaml.safe_load(file)
            return yaml_content
        except yaml.YAMLError as exc:
            raise ValueError("Erreur lors de la lecture du fichier YAML") from exc

# Route pour obtenir le template en JSON
@router.get("/")
async def get_template():
    try:
        yaml_content = read_yaml_template()
        return JSONResponse(content=yaml_content)
    except (FileNotFoundError, ValueError) as e:
        raise HTTPException(status_code=500, detail=str(e))
