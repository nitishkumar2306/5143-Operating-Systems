"""
    Used to get the current user and current directory structure which are used to 
    print prompt in command line
"""
import getpass
import os
from colorama import Fore, Style


# ░██╗░░░░░░░██╗██╗░░██╗░█████╗░░█████╗░███╗░░░███╗██╗  ░█████╗░░█████╗░███╗░░░███╗███╗░░░███╗░█████╗░███╗░░██╗██████╗░
# ░██║░░██╗░░██║██║░░██║██╔══██╗██╔══██╗████╗░████║██║  ██╔══██╗██╔══██╗████╗░████║████╗░████║██╔══██╗████╗░██║██╔══██╗
# ░╚██╗████╗██╔╝███████║██║░░██║███████║██╔████╔██║██║  ██║░░╚═╝██║░░██║██╔████╔██║██╔████╔██║███████║██╔██╗██║██║░░██║
# ░░████╔═████║░██╔══██║██║░░██║██╔══██║██║╚██╔╝██║██║  ██║░░██╗██║░░██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║╚████║██║░░██║
# ░░╚██╔╝░╚██╔╝░██║░░██║╚█████╔╝██║░░██║██║░╚═╝░██║██║  ╚█████╔╝╚█████╔╝██║░╚═╝░██║██║░╚═╝░██║██║░░██║██║░╚███║██████╔╝
# ░░░╚═╝░░░╚═╝░░╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝╚═╝░░░░░╚═╝╚═╝  ░╚════╝░░╚════╝░╚═╝░░░░░╚═╝╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═════╝░
def whoami(**kwargs):
    #print('\n')
    current_user = getpass.getuser()
    return current_user

def prompt():
    """
    This function gets the current user and current directory structure which are used to 
    print prompt in command line
"""
    # set default prompt
    current_user = whoami()
    prompt = Fore.GREEN + current_user + Style.RESET_ALL+": "+Fore.BLUE+os.getcwd()+ "$:"+Style.RESET_ALL
    return prompt 
    


