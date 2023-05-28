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
api_key = os.getenv('OPENAI_API_KEY', '')
max_code_segment_length = 14

model = "gpt-3.5-turbo-0301"
temperature = 0.2
tone = "helpful, empathetic, and friendly"
role = "tutor"
objective = "to truthfully answer computer science and Python programming related questions"
audience = "students with no prior Python programming experience"
points_of_view = "Consider multiple perspectives or opinions."
limitations = "Never respond with code or implementation. You will not be able to put Python code into a response. Do not respond with code."
format = "Give a response in markdown format."

msg = [
    {
        "role": "system",
        "content": f"You are a {tone} {role}. Your objective is {objective}. Your audience is {audience}. {points_of_view} {limitations} {format}"
    }
]


class MyServer(BaseHTTPRequestHandler):

    def _ask_openai(self, context: list) -> (int, str):
        openai.api_key = api_key
        messages = msg.copy()
        messages.extend(context)
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
        except Exception as e:
            print(e)
            return 500, "Something went wrong, please try again."

    def do_GET(self) -> None:
        if self.path == "/health":
            status, content, content_type = 200, "OK", "text/html"
        else:
            status, content, content_type = 404, "Not Found", "text/html"
        self.send_response(status)
        self.send_header("Content-type", content_type)
        self.end_headers()
        self.wfile.write(bytes(content, "utf-8"))

    def do_POST(self):
        post_body = self.rfile.read(int(self.headers.get('content-length')))
        try:
            payload = json.loads(post_body.decode(encoding='utf-8', errors='strict'))
            status, result = self._ask_openai(payload)
        except ValueError as e:
            try:
                payload = json.loads(post_body.decode(encoding='unicode_escape', errors='strict'))
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
