import google.generativeai as genai
from PIL import Image

# O prompt baseia-se estritamente nas regras de segurança e persona da documentação.
SYSTEM_PROMPT = """Você é o Bússola, um assistente de análise de dívidas. Sua prioridade máxima é a precisão factual. Você atua como um amigo experiente do mercado financeiro que traduz o "economês" para ajudar o usuário.
Seu tom de voz deve ser Empático, Direto/Lúcido, Didático e Capacitador. Não julgue o gasto passado do usuário; foque na solução. Sempre que precisar calcular o valor final de uma dívida, use a fórmula 
de juros compostos e descreva o passo a passo para o usuário.

VERIFICAÇÃO: Antes de afirmar uma taxa de juros, localize o valor numérico exato no documento.
ISENÇÃO: Sempre que identificar uma possível irregularidade, use: 'Isso apresenta indícios de [problema], recomendo validar com um especialista'.
PROIBIÇÃO: Nunca utilize as palavras 'Garantia', 'Certeza Absoluta' ou 'Ganho Certo'.
CONTEXTO: Se o usuário perguntar algo fora do documento enviado e você não tiver acesso à base de dados atualizada do Banco Central para aquele item, responda: 'Não encontrei essa informação no seu documento e não tenho acesso aos dados externos desse banco no momento'.

REGRAS DE LIMITAÇÃO (O QUE VOCÊ NÃO PODE FAZER):
1. Não toma decisões nem executa pagamentos.
2. Não substitui o advogado (não dá assessoria jurídica formal).
3. Não garante aprovação de crédito ou acordos com o banco.
4. Não faz previsões de mercado "certas" (ex: não preveja a taxa Selic com 100% de certeza).
5. Não altera dados no sistema do banco, Serasa, Boa Vista ou SPC.
"""

def get_bussola_model():
    """Inicializa o modelo Gemini com temperatura baixa para respostas determinísticas."""
    # Temperatura configurada entre 0.1 e 0.3 conforme documentação para evitar alucinações.
    generation_config = genai.types.GenerationConfig(
        temperature=0.2, 
    )
    
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash', # Excelente para contextos longos (como contratos)
        system_instruction=SYSTEM_PROMPT,
        generation_config=generation_config
    )
    return model

def calcular_juros_compostos(principal, taxa_mensal, meses):
    """
    Ferramenta de validação para garantir que o Bússola não alucine 
    em cálculos de dívida acumulada.
    """
    # Fórmula: M = P * (1 + i)^n
    montante = principal * (1 + taxa_mensal)**meses
    return round(montante, 2)


def analisar_com_rag(texto_documento, imagens_documento, mensagem_usuario):
    """
    Função multimodal de RAG. Aceita texto extraído (PDFs) e imagens (faturas/prints) 
    como contexto para a pergunta do usuário.
    """
    model = get_bussola_model()
    
    # O conteúdo do prompt agora será uma lista, permitindo misturar texto e imagens
    conteudo_prompt = []
    
    # Adiciona o contexto em texto, se houver
    if texto_documento:
        conteudo_prompt.append(f"Documento de Referência em Texto:\n---\n{texto_documento}\n---")
        
    # Adiciona os objetos de imagem nativamente
    if imagens_documento:
        conteudo_prompt.append("Imagens de Referência (faturas, prints ou fotos de contratos/ofertas):")
        # O Gemini aceita objetos PIL.Image diretamente na lista de conteúdo
        conteudo_prompt.extend(imagens_documento)
        
    # Instrução estrita da documentação para tratamento de erro de imagem ilegível
    instrucao_seguranca = (
        "\nATENÇÃO: Se as imagens fornecidas estiverem borradas ou ilegíveis a ponto de "
        "comprometer a leitura exata do CET, juros ou valores, responda EXATAMENTE com a "
        "seguinte mensagem e interrompa a análise: 'Poxa, não consegui ler bem essa foto. "
        "Pode tentar tirar outra mais nítida ou enviar o PDF original? Preciso ver os números "
        "com clareza para não errar o cálculo.'"
    )
    
    conteudo_prompt.append(f"\nPergunta do usuário: {mensagem_usuario}" + instrucao_seguranca)

    # Gera a resposta passando a lista multimodal
    resposta = model.generate_content(conteudo_prompt)
    return resposta.text
