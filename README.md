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
The default model is `deepseek-coder:6.7b-instruct`, you can change it by editing `python3/codeassistant.py`, by changing the `MODEL_NAME` variable.

## Install with vim-plug
```
Plug 'leocus/codeassistant.vim'
```
