#!/bin/bash
watchmedo shell-command --pattern='*.py' \
	--recursive \
	--command=tox \
	-i '*.egg-info;.tox;.cache' \
        -w \
        annex tests
