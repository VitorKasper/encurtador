from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import sys

try:
    from dotenv import load_dotenv
    # Carrega o .env localizado na raiz do projeto
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))
except ImportError:
    pass

# Garante que o diretório src esteja no sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from service.encurtador import Encurtador

app = Flask(__name__, template_folder="templates", static_folder="static")
encurtador_service = Encurtador()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/encurtar", methods=["POST"])
def api_encurtar():
    data = request.get_json(silent=True) or {}
    url = data.get("url", "").strip()

    if not url:
        return jsonify({
            "sucesso": False,
            "mensagem": "Por favor, informe uma URL válida."
        }), 400

    base_url = request.host_url.rstrip("/")
    resultado = encurtador_service.encutar_url(url=url, base_url=base_url)

    return jsonify(resultado), 200

@app.route("/api/buscar", methods=["POST"])
def api_buscar():
    data = request.get_json(silent=True) or {}
    termo = data.get("termo") or data.get("codigo") or data.get("url") or ""
    termo = termo.strip()

    if not termo:
        return jsonify({
            "sucesso": False,
            "mensagem": "Por favor, informe um código ou link encurtado."
        }), 400

    resultado = encurtador_service.obter_destino(termo, registrar_clique=False)
    if resultado["sucesso"]:
        return jsonify(resultado), 200
    else:
        return jsonify(resultado), 404

@app.route("/api/links", methods=["GET"])
def api_links():
    base_url = request.host_url.rstrip("/")
    links = encurtador_service.listar_links(base_url=base_url)
    return jsonify({
        "sucesso": True,
        "total": len(links),
        "links": links
    }), 200

@app.route("/<codigo>")
def redirecionar(codigo):
    # Ignora requisições para favicon ou arquivos internos que cheguem aqui
    if codigo in ("favicon.ico", "robots.txt", "static", "api"):
        return "", 404

    resultado = encurtador_service.obter_destino(codigo, registrar_clique=True)
    if resultado["sucesso"]:
        return redirect(resultado["destino"], code=302)

    return render_template("404.html", codigo=codigo), 404

if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    porta = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "True").lower() in ("true", "1", "yes")

    print(f"\n* Servidor do Encurtador rodando em: http://127.0.0.1:{porta}\n")
    app.run(host=host, port=porta, debug=debug)

