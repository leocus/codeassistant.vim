import os
import vim
import json
import glob
import pickle
import requests

from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


VECTORSTOREPATH = ".codeassistant_vectorstore/"
ALLOWED_EXTENSIONS = [".py", ".json", ".js", ".c", ".cpp", ".java"]


def get_config():
    return {
        "model_name": "deepseek-coder:6.7b-instruct",
        "url": "http://localhost:11434/api/chat",
        "token": "no-token-needed",
        "rag": False,  # Disabled by default to keep compatibility
        "chunk_size": 500,  # Used for RAG
        "rag_model": "deepseek-coder:1.3b",
    }


class AutoComplete:
    def __init__(self):
        self.config = get_config()
        self.headers = {
            "Authorization": f"Bearer {self.config['token']}",
            "Content-Type": "application/json"
        }
        self.payload = {
            "model": self.config["model_name"],
            "messages": [
                {
                    "role": "system",
                    "content": "You are an helpful coding assistant. Your goal is to help the user with every request.",  # noqa: E501
                },
            ],
            "stream": False,
        }
        
        if self.config["rag"]:
            # Check if the vector store exists
            if not os.path.exists(VECTORSTOREPATH):
                self.refresh_vectorstore()
            else:
                # Load existing vectorstore
                self.vectorstore = Chroma(persist_directory=VECTORSTOREPATH, embedding_function=OllamaEmbeddings(model=self.config["rag_model"]))

    def refresh_vectorstore(self):
        splits = []
        files = glob.glob('*', recursive=True)
        files.extend(glob.glob('*/*', recursive=True))

        for file in files:
            # Check if the file is in the blacklist
            to_be_used = False
            i = 0
            while i < len(ALLOWED_EXTENSIONS) and not to_be_used:
                if file.endswith(ALLOWED_EXTENSIONS[i]):
                    to_be_used = True
                i += 1

            if to_be_used:
                # Load the file's content
                print(f"Adding {file} to the vector store")
                try:
                    loader = TextLoader(file)
                    data = loader.load()
                    
                    # Split the file content
                    text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.config['chunk_size'], chunk_overlap=0)
                    splitted_doc = text_splitter.split_documents(data)

                    for doc in splitted_doc:
                        doc.page_content = f"File: {file}\n" + doc.page_content

                    # Add the chunks to the list of chunks
                    splits.extend(splitted_doc)

                except Exception as e:
                    print(e)

        # Check n. of documents
        if len(splits) > 0:
            # Build vector store
            self.vectorstore = Chroma.from_documents(documents=splits, embedding=OllamaEmbeddings(model=self.config["rag_model"]), persist_directory=VECTORSTOREPATH)
            # pickle.dump(self.vectorstore, open(VECTORSTOREPATH, "wb"))
        else:
            self.vectorstore = None

    def get_selection(self, buffer_lines, start_line, end_line):
        prompt = "```\n"
        for i in range(start_line - 1, end_line):
            prompt += buffer_lines[i] + "\n"

        prompt += "```"
        return prompt

    def query_model(self, prompt, use_rag=False):
        payload = self.payload.copy()

        # Search for a similar piece of code if RAG is enabled
        if use_rag and self.vectorstore:
            docs = self.vectorstore.similarity_search(prompt)

            prompt = "# Relevant context " + "\n".join(docs[i].page_content for i in range(len(docs))) + "\n" + prompt

        payload["messages"].append({"role": "user", "content": prompt})

        url = self.config["url"]
        response = requests.post(url, data=json.dumps(payload), headers=self.headers)
        response = json.loads(response.text)

        if "choices" in response: 
            return response["choices"][0]["message"]["content"]
        else:
            return response["message"]["content"]


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

    def exec_prompt(self, start_line, end_line, prompt, replace=False, use_rag=False) -> None:
        buffer_lines = vim.current.buffer
        prompt = prompt + "\n" + self.get_selection(buffer_lines, start_line, end_line)

        out = self.query_model(prompt, use_rag)

        code = self.parse_code(out)

        # Replace text
        if replace:
            del buffer_lines[start_line - 1 : end_line]
        else: 
            start_line = end_line

        vim.api.buf_set_lines(
            buffer_lines,
            start_line - 1,
            start_line - 1 + len(code),
            False,
            code,
        )

    def comment(self, start_line, end_line) -> None:
        prompt = "\nTask: Rewrite the code below, line by line, by adding documentation and comments."
        vim.async_call(
            self.exec_prompt,
            start_line=start_line,
            end_line=end_line,
            prompt=prompt,
            replace=True,
            use_rag=False,
        )

    def autocomplete(self, start_line, end_line) -> None:
        prompt = "\nTask: Continue the implementation of this piece of code: "
        vim.async_call(
            self.exec_prompt,
            start_line=start_line,
            end_line=end_line,
            prompt=prompt,
            replace=False,
            use_rag=True,
        )

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
