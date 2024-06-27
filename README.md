# CodeAssistant.vim
A vim plugin for code completion with local LLMs.

Comment mode:
[![asciicast](https://asciinema.org/a/Cn6qlS0RU8RqM17smGdu1nrom.svg)](https://asciinema.org/a/Cn6qlS0RU8RqM17smGdu1nrom)

Autocomplete mode:
[![asciicast](https://asciinema.org/a/vGxgwxjt4WptNJTfDUOS95R6p.svg)](https://asciinema.org/a/vGxgwxjt4WptNJTfDUOS95R6p)

## Usage
### AutoCompletion mode
To perform autocompletion, select the lines that you want to complete (in visual mode) and call `:'<,'>AutoComplete`

### Comment mode
To comment a piece of code, select the lines (in visual mode) and call `:'<,'>Comment`

## Requirements
Requires a server for inference vim with python3 support.
An example of server can be [ollama](https://ollama.com) (for local inference), or you can also use remote models (e.g., [groq](groq.com)).

## Configuration
The default model is `deepseek-coder:6.7b-instruct`, you can change it by editing the project-wise file: `.codeassistant_config.json`, by changing the `model_name` value.
Also, to change the server address, simply edit the `url` field.
The config file is created the first time you open vim in a directory.

### Retrieval Aumented Generation
You can enable RAG by switching the `rag` field in the config file, and choosing an appropriate `rag_model` served with ollama.

## Install with vim-plug
First, install ollama from [https://ollama.com/](https://ollama.com/),
then, install the plugin with:
```
Plug 'leocus/codeassistant.vim'
```

## Disclaimer
This plugin uses pretrained LLMs to generate code. Beware of the limitations of LLMs and of possible bugs in the plugin (which are quite likely :) ). If you have any suggestion for improving this plugin or to report any bug, please open an issue! :)

# TODO
- [ ] Add the possibility to have an authentication token

