from pathlib import Path

import chromadb
import streamlit as st
from langchain_community.retrievers import WikipediaRetriever
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM

# Function to convert documents to text
def convert_docs_to_text(documents):
    texts = []
    for document in documents:
        with open(document, "r", encoding="utf-8") as file:
            text = file.read()
            texts.append(text)
    return texts

# Define the retriever tool
def retriever_tool(user_input):
    docs = retriever.invoke(user_input)
    context = docs[0].page_content[:400]            
    result = chain.invoke({"context": context, "question": user_input})
    return context, result

# Define the default tool
def default_tool(user_input, history):
    query_results = collection.query(query_texts=[user_input], n_results=1)
    context = query_results["documents"][0][0]
    context += "".join(history)
    result = chain.invoke({"context": context, "question": user_input})
    return context, result

# Agent class
class Agent:
    def __init__(self, role, goal, backstory, tools):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.tools = tools

    def handle_conversation(self, user_input, history):
        places = ["tokyo", "bangkok", "bali", "kyoto", "singapore", "paris", "rome", "barcelona", "amsterdam", "berlin"]
        normalized_input = user_input.strip().lower()

        if normalized_input in places:
            context, result = self.tools['retriever'](user_input)
        else:
            context, result = self.tools['default'](user_input, history)

        return context, result

# Initialize the components
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="Collection")

# Define local knowledge files using project-relative paths
project_dir = Path(__file__).resolve().parent
documents = [
    project_dir / "Asia Destinations.txt",
    project_dir / "Europe Destinations.txt",
    project_dir / "Travel Advice.txt",
]
document_texts = convert_docs_to_text(documents)

# Add the documents to ChromaDB
collection.add(documents=document_texts, ids=[f"id{i}" for i in range(len(document_texts))])

# Setup the model and prompt
template = '''
Answer the question below. 

Here is the conversation history: {context}

Question: {question}

Answer:
'''

model = OllamaLLM(model="gemma2:2b")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model
retriever = WikipediaRetriever()

agent = Agent(
    role="Travel Advisor", 
    goal="Determine whether the user prompt contains a place in the list of places", 
    backstory="Responsible for reading user prompts and determining whether the user might need information on a specific place.",
    tools={'retriever': retriever_tool, 'default': default_tool}
)

# Streamlit UI
st.title("Travel Advisor")
st.write("Type in a place to learn more about it!")

user_input = st.text_input("Enter a place or question:")
if "history" not in st.session_state:
    st.session_state.history = []

if user_input:
    context, result = agent.handle_conversation(user_input, st.session_state.history)
    st.session_state.history.append(f"User: {user_input}\nAI: {result}\n")
    
    st.subheader("Context")
    st.write(context)
    st.subheader("Response")
    st.write(result)

if st.button("Exit"):
    st.stop()
