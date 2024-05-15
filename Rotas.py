from flask import Flask, request, jsonify

from Vendedor import GerenciarVendedor, Vendedor

app = Flask(__name__)
gerenciadorVendedor = GerenciarVendedor()

@app.route('/vendedores', methods=['POST'])
def create_vendedor():
    data = request.json
    vendedor = Vendedor(data['nome'], data['cpf'], data['data_nascimento'], data['email'], data['estado'])
    gerenciadorVendedor.create_vendedor(vendedor)

    resposta = {
        "message": "Vendedor criado com sucesso",
        "data": {
            "nome": vendedor.nome,
            "cpf": vendedor.cpf,
            "data_nascimento": str(vendedor.data_nascimento),
            "email": vendedor.email,
            "estado": vendedor.estado
        }
    }

    return jsonify(resposta), 201

@app.route('/vendedores/<cpf>', methods=['GET'])
def get_vendedor(cpf):
    vendedor = gerenciadorVendedor.read_vendedor(cpf)
    if vendedor:
        return jsonify({"cpf": vendedor[0], "nome": vendedor[1], "data_nascimento": vendedor[2], "email": vendedor[3], "estado": vendedor[4]}), 200
    return jsonify({"message": "Vendedor não encontrado"}), 404

@app.route('/vendedores/<cpf>', methods=['PUT'])
def update_vendedor(cpf):
    data = request.json
    vendedor = Vendedor(data['nome'], data['cpf'], data['data_nascimento'], data['email'], data['estado'])
    gerenciadorVendedor.update_vendedor(vendedor)

    resposta = {
        "message": "Vendedor atualizado com sucesso",
        "data": {
            "nome": vendedor.nome,
            "cpf": vendedor.cpf,
            "data_nascimento": str(vendedor.data_nascimento),
            "email": vendedor.email,
            "estado": vendedor.estado
        }
    }

    return jsonify(resposta), 200

@app.route('/vendedores/<cpf>', methods=['DELETE'])
def delete_vendedor(cpf):
    gerenciadorVendedor.delete_vendedor(cpf)
    return jsonify({"message": "Vendedor deletado com sucesso!"})

@app.route('/vendedores', methods=['GET'])
def get_all_vendedores():
    vendedores = gerenciadorVendedor.read_all_vendedores()
    return jsonify([{"cpf": v[0], "nome": v[1], "data_nascimento": v[2], "email": v[3], "estado": v[4]} for v in vendedores])

if __name__ == '__main__':
    app.run(debug=True)
