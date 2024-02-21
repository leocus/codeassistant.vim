if !has('python3')
    echomsg ':python3 is not available, codeassistant will not be loaded.'
    finish
endif

python3 import codeassistant
python3 codeassistant = codeassistant.AutoComplete()

" command! Comment python3 codeassistant.comment()
command! -range Comment python3 codeassistant.comment(<line1>, <line2>)
command! -range AutoComplete python3 codeassistant.autocomplete(<line1>, <line2>)
