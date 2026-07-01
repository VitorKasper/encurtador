from service.encurtador import Encutador

def main():
    encutador = Encutador()

    while True:
        print("="*30)
        print("MENU")
        print("1 - Encurtar url")
        print("2 - Buscar encurtador")
        print("3 - Buscar código encurtador")
        print("0 - Sair")
        print("="*30)
        acao = input("Selecione uma opção: ")

        if acao == "1":
            url_encutar = input("Digite a url que deseja encurtar: ")
            response = encutador.encutar_url(
                url=url_encutar
            )
            print(response["mensagem"])
            input("Pressione \"Enter\" para prosseguir...")
        
        elif acao == "2":
            url_procurada = input("Digite a url que deseja buscar: ")
            response = encutador.buscar_url(url=url_procurada)
            print(response["mensagem"])
        
        elif acao == "3":
            codigo = input("Digite o código do link encurtado: ")
            response = encutador.buscar_codigo(codigo=codigo)
            print(response["mensagem"])

        elif acao == "0":
            print("Obrigado por utilizar o nosso sistema!")
            break

        else:
            print("Selecione alguma opção válida!")

        


if __name__ == "__main__":
    main()
