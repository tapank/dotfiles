set number
set wrap linebreak nolist
set showmatch
set visualbell
set hlsearch ignorecase incsearch
set autoindent
set shiftwidth=8
set softtabstop=8
set textwidth=72
set ruler
set spellfile=~/.vim/spell/en.utf-8.add
filetype plugin indent on
syntax on
imap jk <esc>

" vim-go plugin installation and setup:
" (based on tutorial at:
" https://medium.com/pragmatic-programmers/configuring-vim-to-develop-go-programs-e839641da4ac)
"
" step 1: add these two lines to .vimrc to support file type detection and syntax highlighting:
"	syntax on
"	filetype plugin indent on
" step 2: install vim-go plugin by cloning its repository into ~/.vim/pack/plugins/start :
"	git clone https://github.com/fatih/vim-go.git ~/.vim/pack/plugins/start/vim-go
" step 3: master branch is a development branch and things could break. check out the latest tagged version:
"	cd ~/.vim/pack/plugins/start/vim-go
"	git checkout $(git tag -l --sort version:refname | grep -v rc | tail -1)
" step 4: once the plugin is installed, configure the help system as follows:
"	vim -c ":helptags ALL" -c ":q"
" step 5: finally, install the required Go utilities:
"	$ vim -c ":GoInstallBinaries" -c ":q"

" set leader to /
let mapleader = "\\"

" Common Go commands
au FileType go nmap <leader>r <Plug>(go-run)
au FileType go nmap <leader>b <Plug>(go-build)
au FileType go nmap <leader>t <Plug>(go-test)
au FileType go nmap <leader>c <Plug>(go-coverage-toggle)
au FileType go nmap <Leader>e <Plug>(go-rename)
au FileType go nmap <Leader>s <Plug>(go-implements)
au FileType go nmap <Leader>i <Plug>(go-info)
