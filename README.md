# Encurtador de URL

Encurtador de URLs rápido, moderno e leve em Python. Possui tanto **Interface Web interativa (Site)** quanto modo **Terminal (CLI)**, mantendo os links em memória durante a sessão.

---

## 🌐 Interface Web (Site)

O projeto conta com uma interface web com tema Dark/Glassmorphism, suporte a cópia rápida, busca por código e redirecionamento direto no navegador.

### Como rodar o site

```bash
python src/app.py
```

Após iniciar, abra no seu navegador:
👉 **[http://localhost:5000](http://localhost:5000)**

### Funcionalidades do Site

- **Encurtar URL**: Cole qualquer link longo e receba uma URL encurtada com código único de 5 dígitos alfanuméricos.
- **Redirecionamento Web Real**: Acesse `http://localhost:5000/<codigo>` para ser redirecionado instantaneamente (HTTP 302) ao link original.
- **Buscar / Redirecionar**: Digite apenas o código ou a URL encurtada para localizar e acessar o destino.
- **Histórico da Sessão**: Acompanhe todos os links encurtados durante a sessão com botão de cópia rápida em 1 clique.
- **Detecção de Duplicados**: URLs já encurtadas na sessão retornam o mesmo código gerado anteriormente.

---

## 💻 Modo Terminal (CLI)

Se preferir usar diretamente pelo console interativo:

```bash
cd src
python main.py
```

Opções do menu:
1. **Encurtar URL**
2. **Buscar encurtador**
3. **Buscar código encurtador**
0. **Sair**

---

## 📂 Estrutura do Projeto

```
encurtador/
├── src/
│   ├── app.py                  # Servidor Flask e rotas da API/Redirecionamento
│   ├── main.py                 # Menu interativo via terminal (CLI)
│   ├── service/
│   │   └── encurtador.py       # Lógica central de encurtamento e busca
│   ├── templates/
│   │   ├── index.html          # Página principal do site
│   │   └── 404.html            # Página de link não encontrado
│   └── static/
│       ├── css/
│       │   └── style.css       # Estilos modernos Dark/Glassmorphism
│       └── js/
│           └── main.js         # Integração assíncrona do frontend
└── tests/
    ├── test_encurtador.py      # Testes unitários do serviço
    └── test_app.py             # Testes de integração da aplicação Flask
```

---

## 🧪 Testes Automatizados

Para rodar a suíte de testes:

```bash
python -m unittest discover tests
```

---

## ⚙️ Requisitos e Instalação

- Python 3.10+

Instale as dependências com:

```bash
pip install -r requirements.txt
```

