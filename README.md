# 🔍 Sistema de Busca Inteligente em Documentos com IA (LLM + RAG)

Aplicação web para busca semântica em documentos corporativos utilizando arquitetura **RAG (Retrieval-Augmented Generation)**.

O sistema permite que usuários façam perguntas em linguagem natural e recebam respostas fundamentadas no conteúdo real dos documentos internos da empresa.

---

## 🚀 Visão Geral

Este projeto implementa uma solução de **IA aplicada à gestão do conhecimento corporativo**, transformando documentos internos em uma base pesquisável por meio de linguagem natural.

A aplicação:

- 📂 Lê documentos automaticamente (PDF, DOCX, TXT)
- 🧠 Gera embeddings vetoriais
- 📊 Cria um índice vetorial
- 🔎 Realiza busca semântica
- 🤖 Gera respostas contextualizadas com LLM local

---

## 🏗 Arquitetura da Solução

### 1️⃣ Ingestão de Documentos
- Leitura automática da pasta `/documentos`
- Extração e estruturação do texto

### 2️⃣ Geração de Embeddings
- Modelo `sentence-transformers/all-MiniLM-L6-v2`
- Conversão do texto em vetores semânticos

### 3️⃣ Indexação Vetorial
- Criação de `VectorStoreIndex`
- Armazenamento para recuperação eficiente

### 4️⃣ Pipeline RAG
- Usuário faz pergunta
- Sistema recupera trechos semanticamente relevantes
- LLM gera resposta fundamentada nos documentos

---

## 🧠 Stack Tecnológica

- Python  
- Streamlit  
- LlamaIndex  
- Ollama  
- Llama 3.2  
- HuggingFace Embeddings  

---

## 📂 Estrutura do Projeto
