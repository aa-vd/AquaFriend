import os
from langchain.chains import RetrievalQA
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import RetrievalQA
import panel as pn  # GUI

# Secure API Key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Load the text file
loader = TextLoader('WaterConservation.txt', encoding='utf8')

# Check the content of the text file
#documents = loader.load()

# Print the content of the text file
#for doc in documents:
#    print(doc.page_content)
    
# Define embeddings
embeddings = OpenAIEmbeddings()

# Create the index directly using the VectorstoreIndexCreator
index = VectorstoreIndexCreator(embedding=embeddings).from_loaders([loader])

# Initialize the LLM
llm = OpenAI(temperature=0)  # You can adjust the temperature as needed

# Create a RetrievalQA chain with the LLM and the vectorstore retriever
qa_chain = RetrievalQA.from_chain_type(llm, retriever=index.vectorstore.as_retriever())

# Test the query directly
#query = "What are the benefits of low-flow plumbing fixtures?"
#result = qa_chain.run(query)

# Print the result
#print(result)

# Function to handle queries
def collect_messages(_):
    prompt = inp.value_input
    inp.value = ''
    response = ""
    if prompt != "":
        response = qa_chain.run(prompt)
    panels.append(pn.Row('User:', pn.pane.Markdown(prompt, width=600)))
    panels.append(pn.Row('Assistant:', pn.pane.Markdown(response, width=600, styles={'background-color': '#F6F6F6'})))
    return pn.Column(*panels)

# Initialize Panel
pn.extension()
panels = []

inp = pn.widgets.TextInput(value="Hi", placeholder='Enter text here…')
button_conversation = pn.widgets.Button(name="Ask your Query!")
interactive_conversation = pn.bind(collect_messages, button_conversation)

# Dashboard layout
dashboard = pn.Column(
    inp,
    pn.Row(button_conversation),
    pn.panel(interactive_conversation, loading_indicator=True, height=300),
)

dashboard.show()
