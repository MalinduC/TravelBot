import streamlit as st
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.retrievers import WikipediaRetriever
import chromadb

# Function to convert documents to text
def convert_docs_to_text(documents):
    texts = []
    for document in documents:
        with open(document, 'r') as file:
            text = file.read()
            texts.append(text)
    return texts

# Function to split text into chunks
def split_text_into_chunks(text, chunk_size=100):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])
    return chunks

# Function to generate embeddings
def generate_embeddings(chunks):
    embeddings = []
    for chunk in chunks:
        for text in chunk:
            embedding_response = ollama.embeddings(model="llama3", prompt=text)
            embeddings.append(embedding_response)
    return embeddings

# Define the retriever tool
def retriever_tool(user_input):
    docs = retriever.invoke(user_input)
    context = docs[0].page_content[:400]            
    result = chain.invoke({"context": context, "question": user_input})
    return context, result

# Define the default tool
def default_tool(user_input, history):
    query_results = collection.query(query_texts=[user_input], n_results=1)
    context = convert_docs_to_text(query_results["documents"][0])
    context += ''.join(history)
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

        if user_input in places:
            context, result = self.tools['retriever'](user_input)
        else:
            context, result = self.tools['default'](user_input, history)

        return context, result

# Initialize the components
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="Collection")

# Define your documents
doc1 = "C:\\Users\\malin\\Documents\\TravelBot\\Asia Destinations.txt"
doc2 = "C:\\Users\\malin\\Documents\\TravelBot\\Europe Destinations.txt"
doc3 = "C:\\Users\\malin\\Documents\\TravelBot\\Travel Advice.txt"
documents = [doc1, doc2, doc3]

# Add the documents to ChromaDB
collection.add(documents=documents, ids=[f"id{i}" for i in range(len(documents))])

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
history = []

if user_input:
    context, result = agent.handle_conversation(user_input, history)
    history.append(f"User: {user_input}\nAI: {result}\n")
    
    st.subheader("Context")
    st.write(context)
    st.subheader("Response")
    st.write(result)

if st.button("Exit"):
    st.stop()
