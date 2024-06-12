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
Requires `ollama` and vim with python3 support.

## Configuration
The default model is `deepseek-coder:6.7b-instruct`, you can change it by editing `python3/codeassistant.py`, by changing the `model_name` value in the `get_config` function.
Also, to change the server address, simply edit the `url` field in `get_config`.

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

