from flask import Flask, request, jsonify # Serve para: importar a classe Flask, que cria a aplicação web.
from models.task import Task
app = Flask(__name__) # Serve para: criar a aplicação Flask.


# CRUD (create, read, update, delete)
# (Criar / ler / atualizar / deletar)
tasks = [] # criar lista
task_id_control = 1 # sempre declarar "global"


    # funcao de rota POST
@app.route('/tasks', methods={'POST'})
def criar_task():
    global task_id_control # declarar funcao global 
    data = request.get_json()  

    nova_task = Task(id=task_id_control,title=data.get('title'),description=data.get('description'))
    task_id_control += 1
    tasks.append(nova_task)
    print(nova_task)
    return jsonify(nova_task.to_dict()), 201

    # funcao de rota GET 
@app.route("/tasks",methods=['GET'])
def get_taks():
    task_list = [task.to_dict() for task in tasks ] # criando nova lista com "for" dentro , retornando to_dict, funcao em uma linha

    output = { 
    "task": task_list,
    "total_tasks": len(task_list) # contagem de elemntos
} 
    return jsonify(output)

    # funcao de rota GET
@app.route('/tasks/<int:id>',methods =['GET']) # Permite que voce receba requisicao "<int:id>" convertendo para inteiro "int"
def get_task(id):
    task = None
    for t in tasks:
        if t.id ==id:
            return jsonify(t.to_dict())
    
    return jsonify({"mensagem": "Nao foi possivel encontrar a atividade"}), 404

    # funcao de rota PUT
@app.route('/tasks/<int:id>', methods = ["PUT"])
def update_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            print (task)
        if task == None:
            return jsonify ({"mensagem": " Não foipossivel encontrar a atividade"}), 404
        
        data = request.get_json() 
        task.title = data ['title']
        task.description = data ['description']
        task.completed = data ['completed']
        print (task)
        return jsonify ({"mensagem": "Nova Tarefa atualizada com sucesso"})
    
    # funcao de rota delete 
@app.route('/tasks/<int:id>', methods = ["DELETE"])
def delete_task(id):
    task = None

    for t in tasks:
        if t.id == id: 
            task = t
            break 

    if not task:
        return jsonify ({"mensagem": "Não foi possivel encontrar a atividade"}), 404
        
    tasks.remove(task)
    return jsonify ({"mensagem": "Tarefa deletada com sucesso"})


if __name__ == "__main__": # Serve para: garantir que o servidor só será iniciado quando o arquivo for executado diretamente.
    app.run(debug=True)  # Serve para: iniciar o servidor Flask.
