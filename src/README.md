# Código da Aplicação

Esta pasta contém o código do seu agente financeiro.

## Estrutura Sugerida

```
src/
├── app.py              # Aplicação principal (Streamlit/Gradio)
├── agente.py           # Lógica do agente
├── config.py           # Configurações (API keys, etc.)
└── requirements.txt    # Dependências
```

## Exemplo de requirements.txt

```
streamlit
openai
python-dotenv
```

## Como Rodar

```bash
# Instalar dependências
# Execute estes passos na ordem:

# Criar o ambiente:
python -m venv venv

#Ativar o ambiente:
.\venv\Scripts\activate

#Instalar as dependências agora no ambiente limpo:
pip install -r requirements.txt

python -m pip install --upgrade anyio packaging docutils


# Rodar a aplicação
streamlit run src/app.py
```
