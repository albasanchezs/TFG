from bs4 import BeautifulSoup
import requests
import numpy as np
import string
import re
def Preproc(input):
    """
        -Convert text to lowercase
        - Remove numbers
        -Remove punctuation
        - Remove whitespaces
    """
    result = re.sub(r'\d +', '', input.lower())
    result=result.translate(string.maketrans("",""),string.punctuation).strip()