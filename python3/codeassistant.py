import vim
import json
import requests


MODEL_NAME = "deepseek-coder:6.7b-instruct"


class AutoComplete:
    def __init__(self):
        self.payload = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "system", "content": "You are an helpful coding assistant. Your goal is to help the user with every request."}
            ],
            "stream": False
        }
        
    def get_selection(self, buffer_lines, start_line, end_line):
        prompt = "```\n"
        for i in range(start_line - 1, end_line):
            prompt += buffer_lines[i] + "\n"

        prompt += "```"
        return prompt


    def query_model(self, prompt):
        payload = self.payload.copy()
        payload["messages"].append({"role": "user", "content": prompt})

        url = 'http://localhost:11434/api/chat'
        headers = {'Content-type': 'application/json'}
        response = requests.post(url, data=json.dumps(payload), headers=headers)

        out = json.loads(response.text)["message"]["content"]

        return out

    def parse_code(self, out):
        code = []
        reading = False
        for line in out.split("\n"):
            if reading and "```" not in line:
                code += [line]
            elif not reading and "```" in line:
                reading = True
            elif reading and "```" in line:
                reading = False
                break
        
        return code

    def exec_prompt(self, start_line, end_line, prompt) -> None:
        buffer_lines = vim.current.buffer
        prompt = self.get_selection(buffer_lines, start_line, end_line) + "\n" + prompt

        out = self.query_model(prompt)

        code = self.parse_code(out)

        # Replace text
        del buffer_lines[start_line - 1:end_line]
        vim.api.buf_set_lines(buffer_lines, start_line - 1, start_line - 1 + len(code), False, code)

    def comment(self, start_line, end_line) -> None:
        prompt = "Rewrite the code above, line by line, by adding documentation and comments."
        vim.async_call(self.exec_prompt, start_line=start_line, end_line=end_line, prompt=prompt)

    def autocomplete(self, start_line, end_line) -> None:
        prompt = "Continue the implementation of this piece of code."
        vim.async_call(self.exec_prompt, start_line=start_line, end_line=end_line, prompt=prompt)

    def postprocess(self, out):
        code = []
        reading = False
        for line in out.split("\n"):
            if reading and "```" not in line:
                code += [line]
            elif not reading and "```" in line:
                reading = True
            elif reading and "```" in line:
                reading = False
                break
        return code
        
