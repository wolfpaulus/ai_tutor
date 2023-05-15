"""
    AI Tutor init code for colab integration
"""
from IPython.display import display, Markdown, Latex, HTML
from json import dumps, loads
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import textwrap
from google.colab import _message


def print_wrapped(text: str) -> None:
    wrapper = textwrap.TextWrapper(width=90, replace_whitespace=False)
    for element in wrapper.wrap(text):
        print(element)


def ask(question: str, code: bool = False) -> str:
    if code:
        c = [
            {"role": "user", "content": task},
            {"role": "user", "content": "Provide feedback on the python implementation below."}
        ]
    else:
        c = context
    c.append({"role": "user", "content": question})
    payload = dumps(c).encode(encoding="utf-8", errors="strict")
    req = Request(server, method="POST")
    req.add_header('User-Agent', 'Mozilla/5.0')
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    req.add_header('Accept', 'application/json')
    req.add_header('Content-Length', str(len(payload)))
    with urlopen(req, timeout=100, data=payload) as resp:
        status = resp.status
        content = loads(resp.read().decode())
        if status == 200:
            if not code:
                c.append({"role": "assistant", "content": content})
        return content


print("""Disclaimer: 
The AI Python Tutor is an educational tool, 
but it may not cover all scenarios or programming nuances. 
Consult the official Python documentation for comprehensive understanding. 

The AI Tutor is not a substitute for personalized instruction.
Users are responsible for verifying code and applying concepts.
The AI Tutor and its developers are not liable for errors or 
consequences from tool usage.""")

'''
    setup the server, task, and context variables like so:`
    server = "https://.../"
    task = 'Create the first 100 prime numbers.'
    context = [
        {"role": "user", "content": task},
        {"role": "user", "content": "How do I get started?"},
        {"role": "assistant", "content": """1. Initialize an empty list to store the prime numbers.
            2. Start with a number, let's say 2, and check if it is prime.
            3. If the number is prime, add it to the list of primes.
            4. Increment the number and repeat steps 2 and 3 until you have found n prime numbers."""}
    ]
'''
server = ""
task = ""
context = []
