import webbrowser
import random
import re
from datetime import datetime

class Encutador:
    def __init__(self):
        # links[0] = lista de URLs encurtadas (padrão https://encutador.com.br/{codigo})
        # links[1] = lista de URLs originais
        self.links = [[], []]
        self.registros = {}  # codigo -> { "url_original", "url_encurtada", "criado_em", "cliques" }

    def normalizar_url(self, url: str) -> str:
        url = url.strip()
        if not url:
            return url
        if not re.match(r"^https?://", url, re.IGNORECASE):
            return f"https://{url}"
        return url

    def extrair_codigo(self, entrada: str) -> str:
        """Extrai o código de 5 caracteres se a entrada for uma URL completa ou já for o próprio código."""
        entrada = entrada.strip()
        # Se for uma URL (ex: http://localhost:5000/a1b2c ou https://encutador.com.br/a1b2c)
        if "/" in entrada:
            entrada = entrada.rstrip("/").split("/")[-1]
        return entrada

    def verifica_url(self, url, encurtador=True):
        tipo = 0 if encurtador else 1
        try:
            indice = self.links[tipo].index(url)
            return {
                "sucesso": True,
                "mensagem": indice
            }
        except ValueError:
            return {
                "sucesso": False,
                "mensagem": "URL não localizada!"
            }

    def gerar_cod_encutador(self):
        alfabeto = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

        while True:
            val = random.randrange(10000, 99999)
            hash_simples = str(val)

            valores = []
            for _ in range(2):
                val_pos = random.randrange(0, 5)          
                while val_pos in valores:
                    val_pos = random.randrange(0, 5)          
                valores.append(val_pos)
            
            for valor in valores:
                number = hash_simples[valor]
                letra = alfabeto[int(number)]
                s = list(hash_simples)
                s[valor] = letra
                hash_simples = "".join(s)

            if hash_simples not in self.registros:
                break
        
        return {
            "sucesso": True,
            "mensagem": hash_simples
        }

    def encutar_url(self, url, base_url="https://encutador.com.br"):
        url_normalizada = self.normalizar_url(url)
        response = self.verifica_url(url=url_normalizada, encurtador=False)
        
        if response["sucesso"]:
            indice = response["mensagem"]
            url_encurtada_padrao = self.links[0][indice]
            codigo = self.extrair_codigo(url_encurtada_padrao)
            
            # Formata conforme a base solicitada
            base = base_url.rstrip("/") if base_url else "https://encutador.com.br"
            url_formatada = f"{base}/{codigo}"

            return {
                "sucesso": True,
                "codigo": codigo,
                "url_original": url_normalizada,
                "url_encurtada": url_formatada,
                "ja_existia": True,
                "mensagem": f"URL já encurtada: {self.links[0][indice]}"
            }
        
        resp_cod = self.gerar_cod_encutador()
        hash_simples = resp_cod["mensagem"]
        url_encurtada_padrao = f"https://encutador.com.br/{hash_simples}"

        self.links[0].append(url_encurtada_padrao)
        self.links[1].append(url_normalizada)

        base = base_url.rstrip("/") if base_url else "https://encutador.com.br"
        url_formatada = f"{base}/{hash_simples}"

        self.registros[hash_simples] = {
            "codigo": hash_simples,
            "url_original": url_normalizada,
            "url_encurtada_padrao": url_encurtada_padrao,
            "criado_em": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "cliques": 0
        }

        return {
            "sucesso": True,
            "codigo": hash_simples,
            "url_original": url_normalizada,
            "url_encurtada": url_formatada,
            "ja_existia": False,
            "mensagem": f"Encurtador gerado: {url_encurtada_padrao}\nCódigo de acesso: {hash_simples}"
        }

    def obter_destino(self, termo: str, registrar_clique=False):
        """Busca o destino por código ou por URL encurtada completa."""
        termo = termo.strip()
        codigo = self.extrair_codigo(termo)

        if codigo in self.registros:
            if registrar_clique:
                self.registros[codigo]["cliques"] += 1
            return {
                "sucesso": True,
                "codigo": codigo,
                "destino": self.registros[codigo]["url_original"],
                "mensagem": f"Redirecionando para {self.registros[codigo]['url_original']}..."
            }

        # Fallback para self.links caso não esteja em self.registros
        resp_url = self.verifica_url(url=f"https://encutador.com.br/{codigo}", encurtador=True)
        if resp_url["sucesso"]:
            destino = self.links[1][resp_url["mensagem"]]
            return {
                "sucesso": True,
                "codigo": codigo,
                "destino": destino,
                "mensagem": f"Redirecionando para {destino}..."
            }

        return {
            "sucesso": False,
            "mensagem": "Link inexistente! Gere um encurtador!"
        }

    def buscar_url(self, url, abrir_navegador=True):
        resp = self.obter_destino(url, registrar_clique=True)
        if resp["sucesso"]:
            if abrir_navegador:
                webbrowser.open(resp["destino"])
            return {
                "sucesso": True,
                "mensagem": resp["mensagem"],
                "destino": resp["destino"]
            }
        return {
            "sucesso": False,
            "mensagem": "Link inexistente! Gere um encurtador!"
        }
    
    def buscar_codigo(self, codigo, abrir_navegador=True):
        return self.buscar_url(codigo, abrir_navegador=abrir_navegador)

    def listar_links(self, base_url=""):
        base = base_url.rstrip("/") if base_url else ""
        lista = []
        for codigo, item in self.registros.items():
            url_enc = f"{base}/{codigo}" if base else item["url_encurtada_padrao"]
            lista.append({
                "codigo": codigo,
                "url_original": item["url_original"],
                "url_encurtada": url_enc,
                "criado_em": item["criado_em"],
                "cliques": item["cliques"]
            })
        # Mais recentes primeiro
        lista.reverse()
        return lista


# Alias com grafia corrigida para conveniência
Encurtador = Encutador
