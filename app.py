from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)
ARQUIVO = "produtos.json"  # arquivo que guarda o estoque

# Função para carregar produtos
def carregar_produtos():
    try:
        with open(ARQUIVO, "r") as f:
            return json.load(f)
    except:
        return []

# Função para salvar produtos
def salvar_produtos(produtos):
    with open(ARQUIVO, "w") as f:
        json.dump(produtos, f)

# Página principal do painel
@app.route("/")
def home():
    produtos = carregar_produtos()
    return render_template("index.html", produtos=produtos)

# Adicionar produto
@app.route("/add", methods=["POST"])
def add():
    produtos = carregar_produtos()
    produtos.append({
        "nome": request.form["nome"],
        "preco": request.form["preco"],
        "quantidade": int(request.form["quantidade"])
    })
    salvar_produtos(produtos)
    return redirect("/")

# Editar produto
@app.route("/edit/<int:id>", methods=["POST"])
def edit(id):
    produtos = carregar_produtos()
    produtos[id]["nome"] = request.form["nome"]
    produtos[id]["preco"] = request.form["preco"]
    produtos[id]["quantidade"] = int(request.form["quantidade"])
    salvar_produtos(produtos)
    return redirect("/")

# Deletar produto
@app.route("/delete/<int:id>")
def delete(id):
    produtos = carregar_produtos()
    produtos.pop(id)
    salvar_produtos(produtos)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)