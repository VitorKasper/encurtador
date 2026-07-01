import webbrowser
import random

class Encutador():
    def __init__(self):
        self.links = [[],[]]

    def verifica_url(self, url, encurtador=True):
        tipo = 0 if encurtador else 1
        try:
            indice = self.links[tipo].index(url)
            return {
                "sucesso": True,
                "mensagem": indice
            }
        
        except:
            return {
                "sucesso": False,
                "mensagem": f"URL não localizada!"
            }

    def gerar_cod_encutador(self):
        alfabeto = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

        while True:
            val = random.randrange(10000, 99999)
            hash_simples = str(val)

            valores = []
            for i in range(2):
                val = random.randrange(0, 5)          
                while val in valores:
                    val = random.randrange(0, 5)          
                valores.append(val)
            
            for valor in valores:
                number = hash_simples[valor]

                letra = alfabeto[int(number)]

                s = list(hash_simples)

                s[valor] = letra

                hash_simples = "".join(s)

            if not hash_simples in self.links[0]:
                break
        
        return {
            "sucesso": True,
            "mensagem": hash_simples
        }



    def encutar_url(self, url):
        response = self.verifica_url(url=url, encurtador=False)
        if response["sucesso"]:
            return {
                "sucesso": True,
                "mensagem": f"URL já encurtada: {self.links[0][response["mensagem"]]}"
            }
        
        response = self.gerar_cod_encutador()

        hash_simples = response["mensagem"]

        self.links[0].append(f"https://encutador.com.br/{hash_simples}")
        self.links[1].append(url)

        return {
            "sucesso": True,
            "mensagem": f"Encurtador gerado com sucesso: https://encutador.com.br/{hash_simples}"
        }
        
    def buscar_url(self, url):
        response = self.verifica_url(url=url, encurtador=True)
        if response["sucesso"]:
            destino = self.links[1][response["mensagem"]]
            webbrowser.open(destino)  # 🔁 redireciona
            return {
                "sucesso": True,
                "mensagem": f"Redirecionando para {destino}..."
            }
        
        return {
            "sucesso": False,
            "mensagem": "Link inexistente! Gere um encurtador!"
        }
        

