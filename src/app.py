import streamlit as st
import PyPDF2
from PIL import Image
from config import configure_api
from agente import analisar_com_rag

# Configuração da página da interface
st.set_page_config(page_title="Bússola De Crédito", page_icon="🧭", layout="centered")

# Inicializa a API do Google Gemini
try:
    configure_api()
except Exception as e:
    st.error(f"Erro de configuração: {e}")
    st.stop()

st.title("🧭 Bússola De Crédito")
st.markdown("Seu amigo experiente para traduzir contratos e te ajudar a sair das dívidas.")

# Área lateral atualizada para suportar múltiplos arquivos e imagens
with st.sidebar:
    st.header("Análise de Contrato e Faturas")
    st.write("Faça o upload do seu contrato bancário em PDF ou envie fotos/prints das faturas ou ofertas do aplicativo.")
    
    # Permitir múltiplos arquivos e formatos de imagem
    uploaded_files = st.file_uploader(
        "Envie seus arquivos (PDF, PNG, JPG)", 
        type=["pdf", "png", "jpg", "jpeg"], 
        accept_multiple_files=True
    )
    
    texto_contrato = ""
    imagens_contrato = []
    
    if uploaded_files:
        for file in uploaded_files:
            try:
                # Se for PDF, extrai o texto
                if file.name.lower().endswith('.pdf'):
                    reader = PyPDF2.PdfReader(file)
                    for page in reader.pages:
                        texto_extraid = page.extract_text()
                        if texto_extraid:
                            texto_contrato += texto_extraid + "\n"
                
                # Se for Imagem, abre com o Pillow e guarda na lista
                elif file.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                    img = Image.open(file)
                    imagens_contrato.append(img)
                    st.image(img, caption=f"Imagem carregada: {file.name}", use_column_width=True)
                    
            except Exception as e:
                st.error(f"Erro ao ler o arquivo {file.name}: {e}")
                
        st.success("Documentos carregados! O Bússola já está pronto para ler as 'letras miúdas'.")

# Gerenciamento de estado do chat
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Saudação inicial conforme definido na documentação
    saudacao_inicial = "Olá! Sou o Bússola. Estou aqui para te ajudar a traduzir esses contratos complicados e encontrar o melhor caminho para sair das dívidas. Se você tiver algum contrato ou print de oferta de negociação, pode subir aqui na barra lateral. Vou ler as 'letras miúdas' para você agora mesmo."
    st.session_state.messages.append({"role": "assistant", "content": saudacao_inicial})

# Exibe o histórico do chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Caixa de entrada para o usuário
if prompt := st.chat_input("Pergunte sobre sua dívida, CET ou envie um print..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Resposta do Agente
    with st.chat_message("assistant"):
        with st.spinner("Analisando seus dados e lendo as imagens..."):
            # Agora passamos os textos extraídos E as imagens para a função
            resposta = analisar_com_rag(texto_contrato, imagens_contrato, prompt)
            st.markdown(resposta)
                           
    # Salva a resposta no histórico
    st.session_state.messages.append({"role": "assistant", "content": resposta})
