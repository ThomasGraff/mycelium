
from os import getenv
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

# Configuration à partir des variables d'environnement
AUTHENTIK_HOST = getenv('AUTHENTIK_HOST', 'https://auth.example.com')
AUTHENTIK_CLIENT_ID = getenv('AUTHENTIK_CLIENT_ID')
AUTHENTIK_CLIENT_SECRET = getenv('AUTHENTIK_CLIENT_SECRET')

# URLs construites dynamiquement
AUTHORIZE_URL = f'{AUTHENTIK_HOST}/application/o/authorize/'
TOKEN_URL = f'{AUTHENTIK_HOST}/application/o/token/'
USERINFO_URL = f'{AUTHENTIK_HOST}/application/o/userinfo/'

oauth = OAuth()
oauth.register(
    name='authentik',
    server_metadata_url=f'{AUTHENTIK_HOST}/.well-known/openid-configuration',
    client_id=AUTHENTIK_CLIENT_ID,
    client_secret=AUTHENTIK_CLIENT_SECRET,
    authorize_url=AUTHORIZE_URL,
    access_token_url=TOKEN_URL,
    api_base_url=USERINFO_URL
)

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.get("/login")
async def login(request: Request):
    """
    Initiate OAuth2 login with Authentik
    """
    redirect_uri = request.url_for('auth_callback')
    return await oauth.authentik.authorize_redirect(request, redirect_uri)

@router.get("/callback")
async def auth_callback(request: Request):
    """
    Handle OAuth2 callback from Authentik
    """
    try:
        token = await oauth.authentik.authorize_access_token(request)
        user = await oauth.authentik.parse_id_token(request, token)
        
        # Ici, vous pouvez ajouter votre logique de création de session
        # Par exemple, générer un token JWT, stocker en base, etc.
        
        # Exemple de redirection après authentification réussie
        response = RedirectResponse(url="/dashboard")
        
        # Vous pouvez ajouter le token comme cookie sécurisé
        response.set_cookie(
            key="auth_token", 
            value=token['access_token'], 
            httponly=True, 
            secure=True,
            samesite='lax'
        )
        
        return response
    
    except Exception as e:
        # Gestion des erreurs d'authentification
        raise HTTPException(status_code=401, detail=str(e))

@router.get("/logout")
async def logout(request: Request):
    """
    Logout the user
    """
    # Logique de déconnexion
    response = RedirectResponse(url="/login")
    response.delete_cookie("auth_token")
    return response

@router.get("/me")
async def get_current_user(request: Request):
    """
    Récupérer les informations de l'utilisateur connecté
    """
    # Récupérez le token depuis les cookies ou l'en-tête
    auth_token = request.cookies.get("auth_token")
    
    if not auth_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        # Validez et récupérez les informations utilisateur
        user_info = await oauth.authentik.parse_id_token(auth_token)
        return {"user": user_info}
    
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")