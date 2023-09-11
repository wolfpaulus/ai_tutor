import azure.functions as func
from azure.identity import ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient
from json import dumps, loads
import logging
import openai
import re

KV_NAME = "KV-func0042"
SECRET_KEY = "OPENAI-SECRET-KEY"
DEPLOYMENT_NAME_OIA = "oai_deploy"
API_BASE = "https://eastus2.api.cognitive.microsoft.com/"
API_VERSION = "2023-07-01-preview"


key = None
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

temperature = 0.2
max_tokens = 4020
tone = "helpful, empathetic, and friendly"
role = "tutor"
objective = "to truthfully answer computer science and Python programming related questions"
audience = "students with no prior Python programming experience"
points_of_view = "Consider multiple perspectives or opinions."
limitations = "Never respond with code or implementation. You will not be able to put Python code into a response. Do not respond with code."
format = "Give a response in markdown format."
max_code_segment_length = 14  # max number of lines of code to show in response
msg = [
    {
        "role": "system",
        "content": f"You are a {tone} {role}. Your objective is {objective}. Your audience is {audience}. {points_of_view} {limitations} {format}"
    }
]


def _get_key() -> str:
    """ Get the openai key from Azure Key Vault. This takes a while :-( """
    url = f"https://{KV_NAME}.vault.azure.net"
    sc = SecretClient(vault_url=url, credential=ManagedIdentityCredential())
    secret = sc.get_secret(SECRET_KEY)
    return str(secret.value)


def _ask_openai(context: list) -> (int, str):
    """ Ask the openai engine for a response."""
    global key
    if not key:
        key = _get_key()

    messages = msg.copy()
    messages.extend(context)

    openai.api_key = key
    openai.api_type = "azure"
    openai.api_base = API_BASE
    openai.api_version = API_VERSION

    response = openai.ChatCompletion.create(
        engine=DEPLOYMENT_NAME_OIA,
        temperature=temperature,
        max_tokens=max_tokens,
        messages=messages)
    result = response.choices[0].message.content
    code = re.search("```[^```]+```", result)

    # remove source-code if too long
    if code and max_code_segment_length < code.string.count("\n"):
        result = re.sub("```[^```]+```", " ... source code removed ... ", result)
    return result


@app.route(route="ask", methods=["POST"])
def ask(req: func.HttpRequest) -> func.HttpResponse:
    """ Ask endpoint."""
    logging.info("ask was called")
    try:
        payload = req.get_body().decode(encoding='utf-8', errors='strict')
        result = _ask_openai(loads(payload))
        return func.HttpResponse(body=dumps(result), status_code=200, mimetype="application/json", charset="utf-8")
    except ValueError as e:
        logging.error(e)
        return func.HttpResponse("Hmm, did you initialize the tutor?", status_code=500)
    except Exception as e:
        logging.error(e)
        return func.HttpResponse(str("Something went wrong, please try again."), status_code=500)


@app.route(route="health")
def health_check(req: func.HttpRequest) -> func.HttpResponse:
    """ Health check endpoint."""
    logging.info('health_check was called.')
    return func.HttpResponse("OK", status_code=200)
