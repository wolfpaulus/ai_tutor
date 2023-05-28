"""
    AI Tutor init code for colab integration
"""

from json import dumps, loads
from urllib.request import Request, urlopen
from IPython.display import Markdown, display, clear_output


def ask(context: [], question, code: bool = False) -> str:
    """
    Ask the AI tutor a question.
    :param context: task and steps
    :param question: student question
    :param code: whether or not to review code
    :return: answer, hopefully in markdown format
    """
    try:
        context.append({"role": "user", "content": question})  # add question to context
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
                    context.append({"role": "assistant", "content": content})  # add response to context
            return content
    except ValueError as e:
        print(e)
        return "Hmm, did you initialize the tutor?"
    except Exception as e:
        return str(e)


def prompt(context: [], p: str = "Enter your question: ") -> None:
    """
    :param context:
    :param p: prompt, in case you don't like the default
    :return: answer, hopefully in markdown format
    """
    try:
        clear_output()
        print()
        question = input(p)
        display(Markdown(ask(context, question)))
    except KeyboardInterrupt:
        pass


def validate(task: str) -> None:
    """
    Request a code review from the AI tutor.
    :param task:
    :return: answer, hopefully in markdown format
    """
    from google.colab import _message
    context = [
        {"role": "user", "content": task},
        {"role": "user", "content": "Provide feedback on the python implementation below."}
    ]
    notebook_json_string = _message.blocking_request('get_ipynb', request='', timeout_sec=5)
    pycode = "".join(notebook_json_string["ipynb"]["cells"][-2]["source"])
    clear_output()
    print(pycode)
    display(Markdown(ask(context, pycode, code=True)))


def create_context(task: str, steps: str) -> []:
    """
    :param task: The task to be completed
    :param steps: The steps to complete the task
    :return: list of dictionaries
    """
    return [
        {"role": "assistant", "content": f"The goal is to {task}, using this approach: {steps}"},
        {"role": "user", "content": "How do I get started?"}
    ]


server = "https://erau13.techcasitaproductions.com/"
#server = "http://localhost:8080/"
print("""Disclaimer: 
The AI Python Tutor is an educational tool, 
but it may not cover all scenarios or programming nuances. 
Consult the official Python documentation for comprehensive understanding. 

The AI Tutor is not a substitute for personalized instruction.
Users are responsible for verifying code and applying concepts.
The AI Tutor and its developers are not liable for errors or 
consequences from tool usage.""")
