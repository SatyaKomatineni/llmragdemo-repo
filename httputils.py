"""
# **********************************************
Module Name: http utils

Description: 
1. http utils

Usage:
1. See the functions

#Date: 1/20/24
# **********************************************
"""

# **********************************************
# Imports
# **********************************************
import baselog as log
import requests

# **********************************************
# Define module-level variables and constants here
# **********************************************
None

# **********************************************
# Functions
# **********************************************

def understandResponse(response: requests.Response):
    code = response.status_code
    log.ph("Status", code)
    log.ph("Headers", response.headers)
    log.ph("Text", response.text)
