from database import show_recent_chat_history
import time
def Dict_convertor(USER_ID):
    history=show_recent_chat_history(USER_ID)
    list=[]
    for role,message in history:
        list.append({"role":role,"content":message})
    return list


    