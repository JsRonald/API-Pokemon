from flask import Flask, render_template, request
import urllib.request
import json

app = Flask(__name__)


def procurar(nome_pokemon):
    url = f"https://pokeapi.co/api/v2/pokemon/{nome_pokemon.lower()}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        resposta = urllib.request.urlopen(req)
        dados = resposta.read()
        dados_pokemon = json.loads(dados)
        return dados_pokemon, None

    except urllib.error.HTTPError as e:
        print(f"Erro HTTP: {e.code} - {e.reason}")
        return None, "Pokemon não encontrado"
    except urllib.error.URLError as e:
        print(f"Erro de URL: {e.reason}")
        return None ,"Erro de conexão"
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None,"Erro desconhecido"


@app.route("/", methods=["GET", "POST"])
def home():
    dados_pokemon = None
    id_pokemon = None  

    if request.method == "POST":
        if request.form.get("txtPokemon"):
            nome_pokemon = request.form.get("txtPokemon")
            dados_pokemon,erro= procurar(nome_pokemon)
            if dados_pokemon:
                id_pokemon= dados_pokemon.get('id')
    else:
        dados_pokemon,erro= procurar("1")
        if dados_pokemon:
                id_pokemon= dados_pokemon.get('id')
    return render_template("index.html", dados_pokemon=dados_pokemon, id_pokemon=id_pokemon,erro= erro)


@app.route("/proximo/<int:id_pokemon>/next")
def proximo(id_pokemon):
    id_pokemon_next = id_pokemon + 1
    dados_pokemon_next,erro = procurar(str(id_pokemon_next))
    return render_template("index.html", dados_pokemon=dados_pokemon_next, id_pokemon=id_pokemon_next,erro= erro)

@app.route("/proximo/<int:id_pokemon>/previous")
def anterior(id_pokemon):
    id_pokemon_prev = max(1,id_pokemon - 1)
    dados_pokemon_prev,erro = procurar(str(id_pokemon_prev))
    return render_template("index.html", dados_pokemon=dados_pokemon_prev, id_pokemon=id_pokemon_prev,erro= erro)

if __name__ == "__main__":
    app.run(debug=True)
