from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from ai_model import llm
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
from Databases.redis.redis_client import add_to_chat, get_recent_chat
import pydantic_models





def organize_docs(files_content):
    parser = PydanticOutputParser(pydantic_object=pydantic_models.Docs)
    instructions = parser.get_format_instructions()
    prompt_template = ChatPromptTemplate.from_template("Condense this document into organized sections that make it easy to find things in a vector store, make sure each metadata is unique: {files_content} {format}")
    prompt = prompt_template.partial(format=instructions)
    chain = prompt | llm | parser
    res: pydantic_models.Docs = chain.invoke({"files_content": files_content})
    print(res)
    docs = []
    for item in res.docs:
        docs.append(Document(page_content=item.content, metadata={"category": item.metadata}))
    return docs

def get_response(results, data, username, context):
    parser = PydanticOutputParser(pydantic_object=pydantic_models.NewMessage)
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="You are in charge of getting the contents of a youtube video base on the users question" 
                        "I will provide the users question and the relavent material, be as straight forward as possible for the user:" 
                        f"Here is the results for the recent question: {results} (if nothing precedes this there were no results and inform the user there is no results)"
                        "Also be sure to print the response out in html so it can be formatted on the frontend"
                        f"{parser.get_format_instructions()}"
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    chain = prompt | llm | parser
    if context != "newUrl":
        add_to_chat(username, "user", data)
        chat = get_recent_chat(username)
        answer = chain.invoke(
            {
                "messages": chat,
            }
        )
        add_to_chat(username, "AI", reply)
    else:
        answer = chain.invoke(
            {
                "messages": [data],
            }
        )

    reply = answer.html_message
    print(reply)
    return reply
    
    
