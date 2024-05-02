import os
import sys
import constants

# for rag
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

# for template runnable
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables import Runnable


def format_docs(docs):
  return "\n\n".join([d.page_content for d in docs])

class FormatTexts(Runnable):
  def __init__(self, text):
    self.text = text
  
  def run(self):
    return "\n".join(self.text.splitlines())


os.environ["OPENAI_API_KEY"] = constants.APIKEY
# Load the document, split it into chunks, embed each chunk and load it into the vector store.
loader = DirectoryLoader('./', glob="data/*.txt", loader_cls=TextLoader)
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)
embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(texts, embeddings)
retriever = db.as_retriever()

# Get input
query = None
if len(sys.argv) > 1:
  query = sys.argv[1]

print(f"Input is : [{query}]")

# Get most relevant doc
# embedding_vector = OpenAIEmbeddings().embed_query(query)
# docs = db.similarity_search_by_vector(embedding_vector)
# doc_res = docs[0].page_content
# print("Get relevant : ", doc_res)

# Get My Persona P
with open('./data/my_persona.txt', 'r') as file:
  # 파일 내용을 읽어 변수에 저장
  Persona = file.read()
  # Persona = format_texts([Persona])
print(f"My Persona is : {Persona}")

# Generate Answer
template = """
Answer the question based only on the following context.
In context, you should answer the other person in the position of 'me'.
Generate a natural answer to the question based on the given {persona}'.
:

{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
model = ChatOpenAI()

chain = (
    {"persona": lambda x: Persona, "context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

print(chain.invoke(query))
