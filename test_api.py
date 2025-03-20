import httpx
import uvicorn
import asyncio

import json
from typing import List
import random

from db.db_session import DB_Session
from models.utilisateur_db import UtilisateurDB
from schemas.auth_data import AuthData
from schemas.user_data import UserInfoData, UserCreationData
from core.password_tools import get_password_hash
from core.api_roles import ApiRole


from main import app

users = [
    UserCreationData( 
        username = "admin", 
        email = "admin@admin.com", 
        password ="admin", 
        role = ApiRole.admin.value),
    UserCreationData( 
        username ="Julian Dupont", 
        email =  "jul@yan.com", 
        password ="Julian", 
        role = ApiRole.cycliste.value),
    UserCreationData( 
        username ="Tadej", 
        email =  "tad@ej.com", 
        password ="Tadej", 
        role = ApiRole.cycliste.value),
    UserCreationData( 
        username ="Jonas", 
        email =  "jon@as.com", 
        password ="Jonas",
        role = ApiRole.cycliste.value),
    UserCreationData( 
        username ="Antoine", 
        email =  "ant@oine.com", 
        password ="Antoine", 
        role = ApiRole.cycliste.value),
    UserCreationData( 
        username ="Nicolas", 
        email =  "nic@olas.com", 
        password ="Nicolas", 
        role = ApiRole.cycliste.value)]

#______________________________________________________________________________
#
# region 1 : /auth login
#______________________________________________________________________________
async def test_login():
    """Test pour obtenir un token d'accès valide"""
   
    user_data = users[0]
    response = await get_login_response(user_data)

    if response.status_code == 200 :
        print ("test_login : OK")
        #print (response.json().get("access_token"))
    else : 
        print ("test_login : errors / ko")
        

async def get_login_response(user_data : UserCreationData) :
    
    auth_data = AuthData(
        username=user_data.username, 
        password=user_data.password)
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://127.0.0.1:8000/auth",
             data = auth_data.model_dump_json())

        return response
    
def get_token(loginresponse):
    access_token = loginresponse.json().get("access_token")
    return access_token

def get_headers(jwt_token) :
    str_token = str(jwt_token)
    headers = {
        'Authorization': f'Bearer {str_token}',  # Ajout du token dans l'en-tête Authorization
    }
    return headers


#______________________________________________________________________________
#
# region 2 : /auth logout
#______________________________________________________________________________
async def test_logout():
    
    user_data = users[1]

    admin_login_response = await get_login_response(user_data)
    jwt_token = get_token(admin_login_response)
    headers = get_headers(jwt_token)

    # Appel à la route de déconnexion
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            "http://127.0.0.1:8000/auth", 
            headers=headers)

    # Vérifications
    if response.status_code == 200 :
        print ("test_logout: OK")
    else : 
        print ("test_logout : errors / ko")



#______________________________________________________________________________
#
# region 3 et 4 /coach/users  create user
#______________________________________________________________________________

async def test_create_user(role : ApiRole):
    
    current_user_data = None
    match role : 
        case ApiRole.admin : current_user_data = users[0]
        case ApiRole.cycliste : current_user_data = users[1]

    login_response = await get_login_response(current_user_data)
    jwt_token = get_token(login_response)
    headers = get_headers(jwt_token)
    
    prefix = "user" if role == ApiRole.cycliste else "coach"
           
    n = str(random.randint(3, 99))
    proto_email = prefix +str(n) + ".fakemail@fakeprovider.com"
    proto_username = prefix+ str(n)

    # Données utilisateur à envoyer
    user_data = UserCreationData(
        email = proto_email,
        username = proto_username, 
        role = role,
        password= proto_username)
    

    # Simuler l'appel à la route de création d'utilisateur
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://127.0.0.1:8000/user", 
            data = user_data.model_dump_json(),
            headers = headers)

    # Vérifications
    if response.status_code == 200 :
        print ("test_create_user : OK")
        #print(response.json())
    else : 
        print ("test_create_user : errors / ko")

    #assert response.json()["email"] == user_data["email"]

async def test_create_user_coach():
    return await test_create_user(ApiRole.admin)

async def test_create_user_cyclist():
    return await test_create_user(ApiRole.cycliste)

#______________________________________________________________________________
#
# region 5 : coach/users
#______________________________________________________________________________
async def test_get_users():

    admin_data = users[0]

    admin_login_response = await get_login_response(admin_data)
    jwt_token = get_token(admin_login_response)
    headers = get_headers(jwt_token)

    # Envoie une requête GET pour récupérer la liste des utilisateurs
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://127.0.0.1:8000/coach/users", 
            headers=headers )

    # Vérifie la réponse et les résultats attendus
    if response.status_code == 200 :
        print ("test_get_users : OK")
        print(response.json())
    else : 
        print ("test_get_users : errors / ko")
    
    # users = []
    # try : 
    #     json_data = response.json()
    #     users : List[UserInfoData] = [UserInfoData.model_validate(user_data) for user_data in json_data]
    # except:
    #     pass
    
    # for user in users : 
    #     print(user)



#______________________________________________________________________________
#
# region  start_uvicorn
#______________________________________________________________________________
async def start_uvicorn():
    config = uvicorn.Config("main:app", host="127.0.0.1", port=8000, reload=True)
    server = uvicorn.Server(config)
    
    # Démarrer le serveur
    await server.serve()

#______________________________________________________________________________
#
# region  stop_uvicorn
#______________________________________________________________________________
async def stop_uvicorn(server_task : asyncio.Task):
    server_task.cancel()  # Annuler la tâche du serveur Uvicorn
    try:
        await server_task  # Attendre que la tâche soit bien terminée
    except asyncio.CancelledError:
        pass  # Ignorer l'exception d'annulation


#______________________________________________________________________________
#
# region all_tests
#______________________________________________________________________________
async def all_tests() :

    # Créer et démarrer le serveur Uvicorn
    print("Start uvicorn server...")
    server_task = asyncio.create_task(start_uvicorn())
    
    # Attendre un peu pour que le serveur démarre (1 seconde)
    await asyncio.sleep(1)
 
    tests = []
    tests.append(test_login)
    tests.append(test_logout)
    tests.append(test_create_user_coach)
    tests.append(test_create_user_cyclist)
    tests.append(test_get_users)

    # Faire les requêtes HTTP
    print("_________________________________________________________")
    for test in tests:
        await test()
        print("_________________________________________________________")

    # Après avoir effectué les tests, arrêter le serveur proprement
    print("Stop uvicorn server...")
    await stop_uvicorn(server_task)

    print("done.")

if __name__ == "__main__":
    asyncio.run(all_tests())

