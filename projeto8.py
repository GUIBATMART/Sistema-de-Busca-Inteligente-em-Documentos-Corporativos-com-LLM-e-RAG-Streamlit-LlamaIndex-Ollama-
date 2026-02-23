# Projeto 8 - IA com LLM e RAG Para Automatizar a Busca em Documentos Internos da Empresa

# Imports

# Biblioteca para extrair texto de arquivos .docx
import docx2txt  

# Biblioteca para criar aplicações web interativas
import streamlit as st  

# Função para importar o modelo de embeddings 
from langchain_community.embeddings import HuggingFaceEmbeddings

# Usaremos o Ollama para importar o LLM
from llama_index.llms.ollama import Ollama  

# Importa componentes essenciais do Llama Index para ler os documentos e gerar o banco de dados vetorial
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings 

# Filtra warnings
import warnings
warnings.filterwarnings('ignore')

# Configurações da página
st.set_page_config(page_title = "DSA Projeto 8", page_icon = ":mag_right:", layout = "centered")

# Título e subtítulo da aplicação
st.title("🔍 Busca Inteligente em Documentos Internos")
st.subheader("LLMs e RAG Para Automatizar a Busca em Documentos Internos da Empresa")

# Texto de introdução
st.markdown("""
Bem-vindo ao sistema de busca automatizada para documentos internos da empresa! 
Com o uso de Inteligência Artificial, você pode realizar consultas rápidas e obter respostas detalhadas baseadas nos documentos disponíveis.
""")

# Adiciona uma barra lateral com instruções
with st.sidebar:
    st.header("Instruções")
    st.markdown("""
    1. Digite sua pergunta no campo ao lado.
    2. Aguarde enquanto o assistente processa sua consulta.
    3. Receba uma resposta detalhada baseada nos documentos da empresa.
    4. Sistemas de IA podem cometer erros.
    5. Sempre verifique as respostas.
    """)
    st.write("Exemplos de perguntas:")
    st.write("- Como é feita a coleta de informações de ponto e frequência?")
    st.write("- Quando o departamento financeiro efetua o pagamento ao fornecedor?")
    st.write("- Por que usar o método FIFO (First In, First Out) no processo de logística?")

    # Rodapé da aplicação
    st.markdown("""
    ---
    🧠 Data Science Academy - Projeto 8
    """)

# Inicializa a sessão de mensagens se não existir
if "messages" not in st.session_state.keys():  
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá! Como posso ajudar? Digite sua pergunta abaixo."}
    ]

# Define o LLM (Large Language Model)
llm = Ollama(model = "llama3", request_timeout = 600.0)  

# Define o modelo de embeddings
embed_model = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2")

# Função para o Módulo de RAG com LlamaIndex, cacheada pelo Streamlit
@st.cache_resource(show_spinner = False)
def dsa_modulo_rag():

    # Exibe um spinner durante o carregamento
    with st.spinner(text = "Carregando e indexando os documentos Streamlit – aguarde! Isso deve levar de 1 a 2 minutos."):  

        # Lê documentos do diretório especificado
        reader = SimpleDirectoryReader(input_dir = "./documentos", recursive = True)  
        
        # Carrega os dados dos documentos
        docs = reader.load_data()  
        
        # Configura o LLM nos settings globais
        Settings.llm = llm  
        
        # Configura o modelo de embeddings nos settings globais
        Settings.embed_model = embed_model  
        
        # Cria um índice de vetores a partir dos documentos
        index = VectorStoreIndex.from_documents(docs)  
        
        # Retorna o índice criado
        return index  

# Carrega o índice de dados
index = dsa_modulo_rag() 

# Construindo o Motor de Execução da App com RAG
# Este código verifica se um motor de chat já está inicializado na sessão do Streamlit. 
# Se não estiver, ele o inicializa com as configurações do banco vetorial e o armazena no session_state para uso contínuo durante a sessão do usuário.
# chat_mode = "condense_question" gera um pergunta condensada sendo um modo de chat simples criado em cima de um mecanismo de consulta sobre seus dados.
# Essa abordagem funciona para perguntas diretamente relacionadas à base de conhecimento. 
# Como ele sempre consulta a base de conhecimento, pode ter dificuldade em responder a metaperguntas como "o que eu perguntei a você antes?"
# https://docs.llamaindex.ai/en/stable/examples/chat_engine/chat_engine_condense_question/
if "chat_engine" not in st.session_state.keys():  

    # Inicializa o motor de chat
    st.session_state.chat_engine = index.as_chat_engine(chat_mode = "condense_question", verbose = True)  

# Verifica se há uma entrada de chat do usuário
if prompt := st.chat_input("Sua pergunta"):  

    # Adiciona a mensagem do usuário ao estado da sessão
    st.session_state.messages.append({"role": "user", "content": prompt})  

# Exibe as mensagens na interface de chat
for message in st.session_state.messages: 

    # Cria um componente de mensagem na interface 
    with st.chat_message(message["role"]):  

        # Exibe o conteúdo da mensagem
        st.write(message["content"])  

# Se a última mensagem não for do assistente, gera uma resposta
if st.session_state.messages[-1]["role"] != "assistant":

    # Cria um componente de mensagem para o assistente
    with st.chat_message("assistant"):

        # Exibe um spinner enquanto pensa
        with st.spinner("Pensando..."):
            
            # Engenharia de prompt para melhor contextualização
            user_message = st.session_state.messages[-1]["content"]
            
            contextual_prompt = f"Você é um assistente de busca especializado. O usuário fez a seguinte pergunta: '{user_message}'. Considere todos os documentos disponíveis e forneça uma resposta detalhada e precisa."
            
            # Gera uma resposta usando o motor de chat
            response = st.session_state.chat_engine.chat(contextual_prompt)

            # Exibe a resposta gerada
            st.write(response.response)

            # Adiciona a mensagem do assistente ao estado da sessão
            st.session_state.messages.append({"role": "assistant", "content": response.response})


# Fim

# Exemplos de perguntas:

# Como é feita a coleta de informações de ponto e frequência?
# Como é é feito o cálculo de salários?
# Quando o departamento financeiro efetua o pagamento ao fornecedor?
# Por que usar o método FIFO (First In, First Out) no processo de logística?
# Como é feito o monitoramento contínuo dos níveis de mercadorias armazenadas?

