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
set textwidth=80
set ruler				" show row and column ruler information
set spell spelllang=en_us		" turn spell check on and set to us_en
set spellfile=~/.vim/spell/en.utf-8.add	" add words to personal dictionary

filetype plugin indent on
syntax enable
set background=dark
colorscheme solarized

imap jk <esc>

