"""
#**********************************************
Module Name: baselog

Description: 
1. To provide pretty print statements
2. Allow for h1, h2, h3 etc
3. Possibly provide time stamps

Usage:
1. Just see the functions

#Date: 1/20/24
#**********************************************
"""

#**********************************************
# Define module-level variables and constants here
#**********************************************
None

#**********************************************
# Functions
#**********************************************

global_debug = True

def turnOffDebug():
    global global_debug
    global_debug = False

    
def dprint(text: str):
    if global_debug == False :
        return
    print(text)

def p(text: str):
    dprint(f"{text}")

def ph(h: str,m: object):
    dprint(f"\n{h}")
    dprint("***********************")
    dprint(f"{m}")

def ptype(context: str, o: object):
    dprint(f"Type of {context}:\n{type(o)}")

def uph1(h: str):
    print(f"\n{h}")
    print("***********************")

def ph1(h: str):
    dprint(f"\n{h}")
    dprint("***********************")

def prompt(text: str) -> str:
    return input(f"\n> {text}")
    
def localTest():
    ph1("Starting local test")
    hello = "hello"
    ptype("hello",hello)
    print ("End local test")

if __name__ == '__main__':
    localTest()