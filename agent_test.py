from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph import StateGraph,END
from langchain_core.messages import HumanMessage
from typing import TypedDict
from dict_convertor import Dict_convertor
from database import add_message,get_username,get_user_id
import time
from Chromadb import context_provider
from dotenv import load_dotenv
import os
from csv_functions import metadata
from binary_convertor import binay_reader

async def agent(EMAIL:str,query:str,filename=""):
    class state(TypedDict):
        llm:BaseChatModel
        query: str
        database_query: str
        response :str
        decision : str
        internet_results : str
        context: str
        filename: str
        user_id:int
        username:str
        tokens:dict
        file_metadata: list

    def decision(agentstate:state):
        print(agentstate["context"])
        if agentstate["context"] in ["File not found","File not provided."]:
            query=agentstate["query"]
            prompt=[{"role":"user","content":f"""
                You are a router.
                Decide if this question needs internet access.
                Reply ONLY:
                SEARCH
                or
                NO_SEARCH
                Question:
                {query}
                """}]
            llm=ChatGroq(model="llama-3.1-8b-instant",api_key=api_key,temperature=0)
            response=llm.invoke(prompt)
            print(response.content)
            return {"decision":response.content}
        else:
            return {"decision":""}
    def search(agentstate:state):
        if agentstate["decision"].lower() == "search":
            search=TavilySearch(api_key=tavily_api_key,max_results=5,search_depth="basic")
            print("Search performed")
            raw_results=search.invoke(agentstate["query"])
            if isinstance(raw_results, dict):
                results = raw_results.get("results", [])
            elif isinstance(raw_results, list):
                results = raw_results
            else:
                results = []
            results_text = "\n\n".join(
                    f"Source: {r.get('url', 'N/A')}\nTitle: {r.get('title', 'N/A')}\nContent: {r.get('content', '')[:500]}"
                    for r in results
                )
            # print(results_text)
            return {"internet_results":results_text}
        else:
            return {"internet_results":"NONE"}

    def llm():
        model=input("Enter your model:")
        if model.lower() in ["google","gemma4","gemma"]:
            load_dotenv()
            api_key=os.getenv("GOOGLE_API_KEY")
            llm=ChatGoogleGenerativeAI(model="gemma-4-26b-a4b-it",api_key=api_key)
            print("====Google model selected====")
            return llm
        elif model.lower() in ["ollama","llama3.2:3b","local"]:
            llm=ChatOllama(model="llama3.2:3b")
            print("====Ollama model selected====")
            return llm
        else:
            print("Wrong model selected.")

    def user_name(user_id:int):
        try:
            username=get_username(user_id)
        except Exception as e:
            print("User name not found")
        return username

    def context_node(agentstate:state):
        time1=time.time()
        agentstate["context"]=context_provider(agentstate["query"],agentstate["filename"])
        print("The time taken in database query:",time.time()-time1)
        return {"context":agentstate["context"]}

    def select_filename()->str:
        file_type=input("Enter file type:")
        if file_type.lower() in [""," ","nothing"]:
            print("====no file selected====")
            return ""
        elif file_type.lower() in ["pdf",".pdf"]:
            folder = r"./pdfs"
            files = os.listdir(folder)
            print("=====Select file=====")
            print("press 0 to not select any file")
            for fileno,file in enumerate(files,start=1):
                print(f"press {fileno} to select {file}")
            n=int(input("fileno-> "))
            n=max(0,n)
            if n == 0:
                print("====no file selected====")
                return ""
            try:
                filename=files[n-1]
                print(f"====={filename} selected=====")
                return filename
            except IndexError :
                print("====no file selected====")
                return ""
        elif file_type.lower() in ["csv",".csv"]:
            folder = r"./csv"
            files = os.listdir(folder)
            print("=====Select file=====")
            print("press 0 to not select any file")
            for fileno,file in enumerate(files,start=1):
                print(f"press {fileno} to select {file}")
            n=int(input("fileno-> "))
            n=max(0,n)
            if n == 0:
                print("====no file selected====")
                return ""
            try:
                filename=files[n-1]
                print(f"====={filename} selected=====")
                return filename
            except IndexError :
                print("====no file selected====")
                return ""

    graph=StateGraph(state)
    graph.add_node("context",context_node)
    graph.add_node("decision",decision)
    graph.add_node("internet_search",search)
    graph.add_edge("context","decision")
    graph.add_edge("decision","internet_search")
    graph.add_edge("internet_search",END)
    graph.set_entry_point("context")
    app=graph.compile()
    load_dotenv()
    api_key=os.getenv("GROQ_API_KEY")
    tavily_api_key=os.getenv("TAVILY_API_KEY")
    model_name=ChatGroq(model="openai/gpt-oss-120b",api_key=api_key,max_tokens=2048,verbose=False,streaming=True)
    user_id=int(get_user_id(EMAIL))
    try:
        username=user_name(user_id)
    except IndexError as e:
        print("User not exsits.")
    file_metadata=metadata(filename)
    
    if query.strip().lower() in ["bye","goodbye","exit","ok bye",""," "]:
        print("bye 👋")
        yield "bye 👋"
        return
    try:
        result=app.invoke({"query":query,"llm":model_name,"user_id":user_id,"username":username,"filename":filename,"file_metadata":file_metadata})
        async def agent_node(result):
                prompt=[{"role":"system","content":f""" user's name is {result["username"]}.please give the summarized response.You are given the following context if there is information about the question you should use this otherwise use your own knowledge: context:{result["context"]} and the metadata is: {result['file_metadata']} and you can use the internet resourses if needed,the internet resourses are {result["internet_results"]}. if internet resourses are available then also give referece of it otherwise do not give the reference and give summerized result."""},{"role":"system","content":"""
                    You are an AI assistant.
                    Always format your answers using valid Markdown.
                    Rules:
                    - Use # for titles.
                    - Use ## for sections.
                    - Leave one blank line before and after headings.
                    - Use numbered lists correctly.
                    - Use bullet lists where appropriate.
                    - Wrap code in triple backticks.
                    - Use tables when helpful.
                    - Do not return plain text.
                    Do NOT generate citation markers such as:
                    - 1†source
                    - 【1†source】
                    - [1]
                    - Source 1
                    """}]
                time1=time.time()
                add_message("user",result["query"],result["user_id"])
                print("Time takein in adding message:",time.time()-time1)
                content=Dict_convertor(result["user_id"])
                time2=time.time()
                print("Time taking content:",time.time()-time2)
                llm_message=prompt+content
                try:
                    time3=time.time()
                    _result = ""
                    async for chunk in result["llm"].astream(llm_message):
                        text=chunk.content
                        _result+=text
                        yield text
                    print("llm envoke time:",time.time()-time3)
                except Exception as e:
                    print("Exception :",e)
                    try:
                        result["llm"]=ChatGroq(model="llama-3.3-70b-versatile",api_key=api_key,max_tokens=2048,streaming=True)
                        _result = ""
                        async for chunk in result["llm"].astream(llm_message):
                            text=chunk.content
                            _result+=text
                            yield text
                        print("llama3.3 versatile invoke.")
                    except Exception as e:
                        print("Exception:",e)
                        try:
                            result["llm"]=ChatGroq(model="llama-3.1-8b-instant",api_key=api_key,max_tokens=2048,streaming=True)
                            _result = ""
                            async for chunk in result["llm"].astream(llm_message):
                                text=chunk.content
                                _result+=text
                                yield text
                            print("llama 3.2 instant invoke.")
                        except Exception as e:
                            print("Exception:",e)
                            _result=str(e)
                            yield "we are sorry about that,You entered too many tokens 🤔. please try later"
                add_message("assistant",_result,result["user_id"])
                result["response"]=_result
        async def image_node(result):
            vison_llm=ChatGroq(model="qwen/qwen3.6-27b",api_key=api_key,temperature=0.7,max_tokens=3096,streaming=True)
            add_message("user",result["query"],result["user_id"])
            content=Dict_convertor(result["user_id"])
            image_base64=binay_reader(result["filename"])
            prompt=[{"role":"system","content":"you are an assistant whose job is to answer the question from the image which is asked by the user and give summarized results."}]
            image = [HumanMessage(
            content=[
                    {
                        "type": "image_url",
                        "image_url": {
                        "url": f"data:image/{result["filename"].split(".")[-1]};base64,{image_base64}"
                        }
                    }
                ]
            )]
            llm_message=prompt+content+image
            _result=""
            try:
                async for chunk in vison_llm.astream(llm_message):
                    text=chunk.content
                    _result+=text
                    yield text
            except Exception as e:
                try:
                    google_api=os.getenv("GOOGLE_API_KEY")
                    vison_llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite",api_key=google_api)
                    async for chunk in vison_llm.astream(llm_message):
                        text=chunk.content
                        _result+=text
                        yield text
                    print("Google image model invoke.")
                except Exception as e:
                    try:
                        vison_llm=ChatOllama(model="qwen3-vl:2b",temperature=0.7,num_ctx=8192)
                        async for chunk in vison_llm.astream(llm_message):
                            text=chunk.content
                            _result+=text
                            yield text
                        print("local image model invoke.")
                    except Exception as e:
                        print("Exception:",e)
                        _result=str(e)
                        yield "we are sorry about that,You entered too many tokens 🤔. please try later"
                        
            add_message("assistant",_result,result["user_id"])
            result["response"]=_result

        if result["filename"].split(".")[-1] in ["pdf","csv"] or result["filename"] =="":
            async for chunk in agent_node(result):
                yield chunk
        elif result["filename"].split(".")[-1] in ["png","jpg","jpeg"]:
            async for chunk in image_node(result):
                yield chunk
        else:
            print("error in llm.")
            print(result["filename"])
            print(result["filename"].split(".")[-1])
            return
            
    except Exception as e:
        print("Exception:",e)
        yield "error"


