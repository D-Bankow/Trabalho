import requests

response = requests.get('http://127.0.0.1:5000/usuarios')
if response.status_code == 200:
    usuarios = response.json()
    for u in usuarios:
        if 'email' in u:
            print(f"Usuário válido: {u['nome']} - {u['email']}")
