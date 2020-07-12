
from flask import Flask, request, jsonify
from scraping import *

app = Flask(__name__)
app.config["DEBUG"] = True
jsontypeerror = {"dados":[{"Message":"Invalid content-type. Must be application/json."}]}


@app.route('/api/tracker', methods=['GET','POST'])
def getRequest():
    if request.method == 'POST':
         #Verifica se o conteudo vindo na requisição é do tipo application/json, caso não for ele retorna um erro
        if request.content_type != 'application/json':
            return jsonify(jsontypeerror)   
        #aqui ele coleta o json da requisicao
        content = request.get_json()
        #aqui está coletano os nome de usuários e transformando em lista uma lista de usuários que é delimitado por ","
        nameusers = content['nomeusuarios'].split(',')
        #Chama a funçaão de scraping 
        return getReturnScraping(nameusers)        
    #Caso a requisição não for do tipo POST ele retorna essa mensagem 
    return jsonify({"Message":"Não foi implementado outros métodos ainda!"})

app.run()



