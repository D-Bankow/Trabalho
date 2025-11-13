from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/usuarios')
def usuarios():
    return jsonify([
        {'id': 1, 'nome': 'Davi', 'email': 'davi@email.com'},
        {'id': 2, 'nome': 'Maria', 'email': 'maria@email.com'}
    ])

if __name__ == '__main__':
    app.run(port=5000)
