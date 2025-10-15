"
" ~/.vimrc
"

set number				" show line numbers
set wrap linebreak nolist		" line break at word
set showmatch				" highlight matching brace
set visualbell				" set visual bell (no beeping)
set hlsearch ignorecase incsearch	" highlight matches, ignore case, search incrementally
set autoindent				" auto indent new lines
set shiftwidth=8
set softtabstop=8
set textwidth=72
set ruler				" show row and column ruler information
set spell spelllang=en_us		" turn spell check on and set to us_en
set spellfile=~/.vim/spell/en.utf-8.add	" add words to personal dictionary
set nocompatible
set dir=~/tmp

" set the color of bad words picked up by spell checker
hi SpellBad cterm=underline ctermfg=red

execute pathogen#infect()

filetype plugin indent on
syntax enable

let g:vimwiki_list = [
  \ {'path': '~/src/notebook/vimwiki', 'syntax': 'markdown', 'ext': '.md'}
  \ ]
let g:vimwiki_global_ext = 0	" do not treat external md files as wiki

