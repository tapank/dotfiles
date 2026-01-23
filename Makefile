.PHONY: sync

all: sync

sync:
	@echo ">>> add and commit changes..."
	-git add -A
	-git commit -m "changes to dotfiles"
	@echo ">>> push changes to github..."
	git push
	@echo ">>> All tasks completed."
