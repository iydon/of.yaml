POETRY = poetry
PYTHON = $(POETRY) run python


.PHONY: help demo dependencies init shell test-cli standalone preview docs uncache publish copyright mypy

help:                  ## Print the usage
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e "s/\\$$//" | sed -e "s/##//"

demo:                  ## Run the demo code
	$(PYTHON) -m foam conv tutorials/incompressible/simpleFoam/airFoil2D.yaml

dependencies:          ## List the dependencies as a tree
	@$(POETRY) show --no-dev --tree

init:                  ## Set environment variables, etc.
	@echo export PYTHONPYCACHEPREFIX="$$HOME/.cache/cpython/"

shell:                 ## Activate the virtual environment
	@$(POETRY) shell

test-cli:              ## Run cli test
	for version in 7 ; do \
		$(PYTHON) -m foam cnv extra/tutorial/tutorials/$$version --directory test/cli --version $$version --exist-ok ; \
		$(PYTHON) -m foam run                                    --directory test/cli --version $$version ; \
	done

standalone:            ## Convert Python package into a single file
	@cp script/$@.py .
	@$(PYTHON) $@.py
	@rm $@.py

preview:               ## Run the builtin development server
	$(PYTHON) -m mkdocs serve

docs:                  ## Build the MkDocs documentation
	$(PYTHON) -m mkdocs Build

uncache:               ## Remove __pycache__ directories
	# https://stackoverflow.com/questions/28991015/python3-project-remove-pycache-folders-and-pyc-files
	find . -type d -name  "__pycache__" -exec rm -r {} +

publish:               ## Build and upload the package to a remote repository
	$(POETRY) build
	$(POETRY) publish

copyright: standalone  ## http://www.gov.cn/zhengce/2020-12/26/content_5574414.htm
	@cp script/$@.py .
	@$(PYTHON) $@.py
	@rm $@.py

mypy:                  ## Check static type for Python
	@$(PYTHON) script/$@.py

foam.py: script/standalone.py
	make standalone
