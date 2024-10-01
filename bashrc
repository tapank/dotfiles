#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

[ -r /usr/share/bash-completion/bash_completion ] && . /usr/share/bash-completion/bash_completion

# Change the window title of X terminals
case ${TERM} in
	xterm*|rxvt*|Eterm*|aterm|kterm|gnome*|interix|konsole*)
		PROMPT_COMMAND='echo -ne "\033]0;${USER}@${HOSTNAME%%.*}:${PWD/#$HOME/\~}\007"'
		;;
	screen*)
		PROMPT_COMMAND='echo -ne "\033_${USER}@${HOSTNAME%%.*}:${PWD/#$HOME/\~}\033\\"'
		;;
esac

use_color=true

# Set colorful PS1 only on colorful terminals.
# dircolors --print-database uses its own built-in database
# instead of using /etc/DIR_COLORS.  Try to use the external file
# first to take advantage of user additions.  Use internal bash
# globbing instead of external grep binary.
safe_term=${TERM//[^[:alnum:]]/?}   # sanitize TERM
match_lhs=""
[[ -f ~/.dir_colors   ]] && match_lhs="${match_lhs}$(<~/.dir_colors)"
[[ -f /etc/DIR_COLORS ]] && match_lhs="${match_lhs}$(</etc/DIR_COLORS)"
[[ -z ${match_lhs}    ]] \
	&& type -P dircolors >/dev/null \
	&& match_lhs=$(dircolors --print-database)
[[ $'\n'${match_lhs} == *$'\n'"TERM "${safe_term}* ]] && use_color=true

if ${use_color} ; then
	# Enable colors for ls, etc.  Prefer ~/.dir_colors #64489
	if type -P dircolors >/dev/null ; then
		if [[ -f ~/.dir_colors ]] ; then
			eval $(dircolors -b ~/.dir_colors)
		elif [[ -f /etc/DIR_COLORS ]] ; then
			eval $(dircolors -b /etc/DIR_COLORS)
		fi
	fi

	if [[ ${EUID} == 0 ]] ; then
		PS1='\[\033[01;31m\][\h\[\033[01;34m\] \W\[\033[01;31m\]]\$\[\033[00m\] '
	else
		# git related configs are explained well at https://mjswensen.com/blog/git-status-prompt-options/
		source /usr/share/git/completion/git-prompt.sh
		export GIT_PS1_SHOWSTASHSTATE=true
		export GIT_PS1_SHOWDIRTYSTATE=true
		export GIT_PS1_SHOWUNTRACKEDFILES=true
		export GIT_PS1_SHOWUPSTREAM="auto"
		PS1='\[\033[01;32m\][\u@\h\[\033[01;34m\] \w\[\033[01;32m\]\[\e[91m\]$(__git_ps1)\[\e[00m\]\[\033[01;32m\]]\$\[\033[00m\] '
	fi

	alias ls='ls -F --group-directories-first --color=auto'
	alias grep='grep --colour=auto'
	alias egrep='egrep --colour=auto'
	alias fgrep='fgrep --colour=auto'
	alias tree='tree -C'
else
	if [[ ${EUID} == 0 ]] ; then
		# show root@ when we don't have colors
		PS1='\u@\h \W \$ '
	else
		PS1='\u@\h \w \$ '
	fi
fi

unset use_color safe_term match_lhs sh


xhost +local:root > /dev/null 2>&1

# Bash won't get SIGWINCH if another process is in the foreground.
# Enable checkwinsize so that bash will check the terminal size when
# it regains control.  #65623
# http://cnswww.cns.cwru.edu/~chet/bash/FAQ (E11)
shopt -s checkwinsize
shopt -s expand_aliases

# export QT_SELECT=4

# History settings
HISTCONTROL=ignoredups:erasedups
shopt -s histappend
PROMPT_COMMAND="history -n; history -w; history -c; history -r; $PROMPT_COMMAND"

# exports
export PATH=$PATH:/usr/local/go/bin:/home/tapan/bin:/home/tapan/go/bin:.
export CDPATH=$CDPATH:~:~/src/karecha.com:~/src:~/Desktop

alias cp="cp -i"		# confirm before overwriting something
alias d="clear;dict -d gcide"		# lookup English language dictionary
alias c="clear;dict -d foldoc"	# lookup computer terms dictionary
set -o vi			# use vi as default editing mode
set -o ignoreeof		# prevent Bash from quitting on EOF
export EDITOR=vim		# use vim for editing commands instead of vi
export HISTTIMEFORMAT="%y/%m/%d %T "	# time stamp format for bash history entries

# source exercism autocomplete if available
if [ -f ~/.config/exercism/exercism_completion.bash ]; then
  source ~/.config/exercism/exercism_completion.bash
fi

banner(){
	screenfetch
	acpi -ba
	echo `date`

	echo
	echo xfce keyboard shortcuts:
	echo ctrl + alt + F[ile manager]
	echo ctrl + alt + T[erminal]
	echo ctrl + alt + W[eb browser]
	echo ctrl + alt + C[alibre]
	echo ctrl + alt + L[iferea]
	echo
}

banner

