"""
Super Simple HTTP Server in Python .. not for production just for learning and fun
Author: Wolf Paulus (https://wolfpaulus.com)
"""
import json
import re
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from json import dumps
import openai

hostName = "0.0.0.0"
serverPort = 8080
api_key = os.environ['OPENAI_API_KEY']
api_model = "gpt-3.5-turbo"  # 'gpt-4'
api_temperature = 0.3
max_code_segment_length = 12
messages = [
    {
        "role": "system",
        "content": "You are a helpful, empathetic, and friendly assistant. Your goal is to answer computer science and programming related question, as truthfully as you can but you will not show the implementation."
    },
    {
        "role": "system",
        "content": "Additionally, you never show Python source code."
    }
]
accept_format = {"role": "user", "content": "Please respond in Markdown"}


class MyServer(BaseHTTPRequestHandler):

    def _ask_openai(self, my_messages: list) -> (int, str):
        openai.api_key = api_key
        model = api_model
        temperature = api_temperature
        messages.extend(my_messages)
        messages.append(accept_format)

        try:
            completion = openai.ChatCompletion.create(
                model=model,
                temperature=temperature,
                messages=messages)
            result = completion['choices'][0]["message"]["content"]
            code = re.search("```[^```]+```", result)
            if code and max_code_segment_length < code.string.count("\n"):  # remove source sode if too long
                result = re.sub("```[^```]+```", " ... source code removed ... ", result)
            return 200, result
        except:
            return 500, "Something went wrong, please try again."

    def do_POST(self):
        post_body = self.rfile.read(int(self.headers.get('content-length')))
        try:
            payload = json.loads(post_body.decode(encoding='utf-8', errors='strict'))
            print(payload)
            status, result = self._ask_openai(payload)
        except ValueError as e:
            try:
                payload = json.loads(post_body.decode(encoding='unicode_escape', errors='strict'))
                print(payload)
                status, result = self._ask_openai(payload)
            except ValueError as e:
                status, result = 501, str(e)
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(dumps(result), "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Server started")
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    print("Server stopped.")
