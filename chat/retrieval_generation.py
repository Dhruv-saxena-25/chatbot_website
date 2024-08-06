from langchain.memory import ConversationBufferWindowMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA 
from chat.data_ingestion import data_ingestion




def generation(vstore):
    retriever = vstore.as_retriever(search_kwargs={"k": 3})
    memory = ConversationBufferWindowMemory(k=6)

    WEBSITE_BOT_TEMPLATE = """
    Your a chatbot of website owned by Dhruv Saxena .
    It analyzes wesite content to provide accurate and helpful responses.
    Ensure your answers are relevant to the information available inside website and if question
    is out of context give answers from you own knowledge base. Your responses should be concise and informative.
    If person greets by saying hi, hello, what's up you have to greet them back.
    CONTEXT:
    {context}

    QUESTION: {question}

    YOUR ANSWER:

    """

    prompt = PromptTemplate(template= WEBSITE_BOT_TEMPLATE, input_variable= ["context", "question"])

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature= 0.89)
    chain = RetrievalQA.from_chain_type(llm=llm,
                                        chain_type= "stuff",
                                        retriever= retriever,
                                        input_key= "query",
                                        memory= memory,
                                        chain_type_kwargs= {"prompt": prompt})

    return chain


if __name__=='__main__':
    vstore = data_ingestion("done")
    chain  = generation(vstore)

    result= chain("can you tell me contact details of Dhruv?")
    print(result['result'])

   


