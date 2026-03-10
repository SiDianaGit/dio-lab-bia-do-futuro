# Código da Aplicação

Esta pasta contém o código do seu agente financeiro.

## Estrutura 

```
/src/
 ├── app.py              # Aplicação principal (Streamlit/Gradio)
 ├── agente.py           # Lógica do agente
 ├── config.py           # Configurações (API keys, etc.)
 └── vector_store.py     # Lógica para carregamento da base de conhecimento "in memory"
/data/
 ├── Regulatory/
    ├── DesenrolaBrasil.pdf
    ├── L14181-LeiDoSuperendividamento2021.pdf
    └── ResoluçãoCMN_5265de28-11-2025.pdf
 └── produtos_credito.json
/
 └── requirements.txt    # Dependências
```

## requirements.txt

```
streamlit==1.32.0
python-dotenv==1.0.1
PyPDF2==3.0.1
Pillow==10.2.0
anyio==4.3.0 
packaging==23.2 
tenacity==8.2.3 
docutils==0.20.1
langchain
langchain-community
langchain-groq
pypdf
pymupdf
sentence_transformers
torch --index-url https://download.pytorch.org/whl/cpu
torchvision --index-url https://download.pytorch.org/whl/cpu
torchaudio --index-url https://download.pytorch.org/whl/cpu
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


#Verifique se a instalação funcionou
#Para ter certeza de que você está na versão correta (deve ser 0.3.0 ou superior), digite:

pip show google-generativeai

# Rodar a aplicação

python -m streamlit run src/app.py


#Para encerrar a sessão e limpar a memória

deactivate

Remove-Item -Recurse -Force venv

python -m pip cache purge
