# Encurtador de URL

Encurtador de URL feito em Python, criado como um desafio pessoal: **construir do zero, sem uso de IA, no menor tempo possível.**

> Tempo total: **30 minutos**

## Como funciona

O programa roda via terminal com um menu interativo. Ele mantém os links em memória durante a sessão (sem banco de dados).

- **Encurtar URL:** recebe uma URL longa e gera um código curto no formato `https://encutador.com.br/XXXXX`. Se a URL já foi encurtada antes, retorna o código existente.
- **Buscar encurtador:** recebe um link curto completo e abre a URL original no navegador.
- **Buscar por código:** recebe apenas o código curto (ex: `a3b9c`) sem precisar digitar a URL completa, e redireciona da mesma forma.

O código curto é gerado com 5 caracteres alfanuméricos, onde dois dígitos de um número aleatório são substituídos por letras do alfabeto.

## Estrutura

```
src/
├── main.py                  # Menu e loop principal
└── service/
    └── encurtador.py        # Lógica de encurtamento e busca
```

## Como rodar

```bash
cd src
python main.py
```

Requer Python 3.x. Sem dependências externas.

## Limitações

- Os links são armazenados apenas em memória — ao encerrar o programa, tudo é perdido.
- Os links curtos gerados (`encutador.com.br/...`) são fictícios e não funcionam como URLs reais na web.
