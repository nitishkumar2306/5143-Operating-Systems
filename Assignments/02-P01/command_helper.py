"""
This file is about  handling of multiple comands.
"""

import sys
#sys.path.insert(0,'./cmd')
from cmds.cat import cat,less,head,tail,cp,touch, mv, rm
from cmds.grep import grep
from cmds.list import ls,ll
from cmds.mkdir import mkdir
from cmds.cd import cd
from cmds.c_pwd import c_pwd
# from clear import clear_terminal
from cmds.echo import echo

from cmds.history import show_history
from cmds.history import add_to_history
from cmds.history import *
from cmds.whoami import whoami
from cmds.wc import wc
from ifconfig import ifconfig
from cmds.ps import ps
from cmds.who import who
from cmds.chmod import chmod
from cmds.sort import sort

class CommandHelper(object):
    """
    This function collect  existing command in dis. commands as key command and value is method name.
    Invoke the respective method as per requirements

    Methods:
        exists (string) : checks if a command exists (dictionary points to the function)
        invoke (string) : Call the respective command function and if help in args  then returns the doc string for a function 
    """
    def __init__(self):
        self.commands = {}
        self.commands["ls"] = ls
        self.commands["ll"] = ll
        self.commands["cat"] = cat
        self.commands["grep"] = grep
        self.commands["less"] = less
        self.commands["head"] = head
        self.commands["tail"] = tail
        self.commands["rm"] = rm
        self.commands["cp"] = cp
        self.commands["mv"] = mv
        self.commands["sort"] = sort
        self.commands["who"] = who
        self.commands["mkdir"] = mkdir
        self.commands["cd"]=cd
        self.commands["pwd"]=c_pwd
        # self.commands["clear"]=clear_terminal
        self.commands["echo"]=echo
        self.commands["touch"]=touch

        self.commands["ps"]=ps
        self.commands["ifconfig"]=ifconfig
        self.commands["whoami"]=whoami
        self.commands["wc"]=wc
        self.commands["chmod"]=chmod
        self.commands["history"] = show_history

        self.commands["add_to_history"] = add_to_history

        self.command_history = []

        
    def invoke(self, **kwargs):
        if "cmd" in kwargs:
            cmd = kwargs["cmd"]
        else:
            cmd = ""

        if "params" in kwargs:
            params = kwargs["params"]
        else:
            params = []
        if "flags" in kwargs:
            flags = kwargs["flags"]
        else:
            flags = []
        if "input" in kwargs:
            input = kwargs["input"]
        else:
            input = []          

        if "help" in kwargs:
            if kwargs["help"]=="help":
                print("\r")
                return self.commands[cmd].__doc__
            else:
                #ls: unrecognized option '--helpp'
                #Try 'ls --help' for more information.
                 
                return "\r %s : unrecognized option '%s' \n Try %s --help for more information " % (cmd, kwargs["help"], cmd)

        else:
            # print("Line 47", self.commands[cmd](params=params,flags=flags,input=input),"---------ends")
            return self.commands[cmd](params=params,flags=flags,input=input)
        
 

    def exists(self, cmd):
        #print(self.commands)
        return cmd in self.commands


