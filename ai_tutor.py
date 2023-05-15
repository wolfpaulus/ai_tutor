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


def ask(server: str, context: [], question: str = "Please enter your question: ", code: bool = False) -> str:
    try:
        payload = dumps(context).encode(encoding="utf-8", errors="strict")
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
                    context.append({"role": "user", "content": question})
                    context.append({"role": "assistant", "content": content})
            return content
    except ValueError as e:
        print(e)
        return "Hmm, did you initialize the tutor?"
    except KeyboardInterrupt:
        pass
    except Exception as e:
        return str(e.__cause__)


def prompt(server, context: [], p: str = "Please enter your question: ") -> None:
    print_wrapped(ask(server, context, question=input(p)))


def validate(server: str, task: str) -> None:
    context = [
        {"role": "user", "content": task},
        {"role": "user", "content": "Provide feedback on the python implementation below."}
    ]
    notebook_json_string = _message.blocking_request('get_ipynb', request='', timeout_sec=5)
    code = "".join(notebook_json_string["ipynb"]["cells"][-2]["source"])
    print(code)
    print_wrapped(ask(server, context, code, code=True))


def create_context(task: str, steps: str) -> []:
    return [
        {"role": "user", "content": task},
        {"role": "user", "content": "How do I get started?"},
        {"role": "assistant", "content": steps}
    ]


print("""Disclaimer: 
The AI Python Tutor is an educational tool, 
but it may not cover all scenarios or programming nuances. 
Consult the official Python documentation for comprehensive understanding. 

The AI Tutor is not a substitute for personalized instruction.
Users are responsible for verifying code and applying concepts.
The AI Tutor and its developers are not liable for errors or 
consequences from tool usage.""")
