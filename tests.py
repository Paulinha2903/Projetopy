# Esse código testa automaticamente se a rota de criação de tarefas da API está funcionando corretamente — enviando dados, 
# validando resposta e guardando o ID gerado.



import pytest # Importa a biblioteca de testes pytest, usada para executar testes automatizados.
import requests # Importa a biblioteca requests, usada para fazer requisições HTTP em Python.

# CRIAÇÃO DE TEST CRUD 

BASE_URL = 'http://127.0.0.1:5000' # Define uma variável com o endereço base da API local.
tasks = [] # Cria uma lista vazia para armazenar IDs das tarefas criadas durante o teste.

def test_create_task(): # Define uma função de teste.
    new_task_data = {  # Cria um dicionário Python com os dados que serão enviados para a API.
        "title": "Nova Tarefa",
        "description": "Descricão da nova tarefa"
    }
    response = requests.post(f"{BASE_URL}/tasks", json=new_task_data) # Envia uma requisição POST para a API criando uma tarefa.
    # f"{BASE_URL}/tasks" → monta a URL final.
    # # json=new_task_data → envia os dados em JSON.

    assert response.status_code == 200  # Verifica se a resposta HTTP foi sucesso (código 200) Se não for, o teste falha.
    response_json = response.json() 
    assert "menssagem" in response_json # Confirma que o campo mensagem existe na resposta.
    assert "id" in response_json # Confirma que a API retornou o ID da tarefa criada.
    tasks.append(response_json['id']) # Adiciona o ID retornado à lista tasks para usar em outros testes (ex: atualizar ou deletar).

def test_get_tasks():
    response = requests.get(f"{BASE_URL}/tasks")
    assert response.status_code == 200
    response_json = response.json()
    assert "task" in response_json
    assert "total_tasks" in response_json

def test_get_task():
    if tasks:
        task_id = tasks [0]
        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 200
        response_json = response.json()
        assert task_id == response_json['id']

def test_update_task():
    if tasks:
        task_id = tasks[0]
        payload = {
            "completed": True,
            "description": "Nova descricao",
            "title": "Titulo atualizado"
        }

        response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=payload)
        response.status_code == 200
        response_json = response.json()
        assert "mensagem" in response_json

        # nova requisicao a tarafa especifica

        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 200
        response_json = response.json()
        assert response_json["title"] == payload["title"]
        assert response_json["description"] == payload["description"]



def test_delete_task(): 
    if tasks:
        task_id = tasks[0]
        response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
        response.status_code = 200

        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 404