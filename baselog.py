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

def ph(h: str,m: object):
    print(f"\n{h}")
    print("***********************")
    print(f"{m}")

def ptype(context: str, o: object):
    print(f"Type of {context}:\n{type(o)}")

def ph1(h: str):
    print(f"\n{h}")
    print("***********************")


def localTest():
    ph1("Starting local test")
    hello = "hello"
    ptype("hello",hello)
    print ("End local test")

if __name__ == '__main__':
    localTest()