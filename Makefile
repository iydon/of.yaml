POETRY = poetry
PYTHON = $(POETRY) run python


.PHONY: help demo dependencies shell test standalone preview docs uncache

help:          ## Print the usage
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

demo:          ## Run the demo code
	$(PYTHON) -m foam conv tutorials/incompressible/simpleFoam/airFoil2D.yaml

dependencies:  ## List the dependencies as a tree
	@$(POETRY) show --no-dev --tree

shell:         ## Activate the virtual environment
	@$(POETRY) shell

test:          ## Run unit tests
	for version in 7 ; do \
		$(PYTHON) -m foam conv tutorials --directory test --version $$version --exist-ok ; \
		$(PYTHON) -m foam test           --directory test --version $$version ; \
	done

standalone:    ## Convert Python package into a single file
	@cp script/standalone.py .
	@$(PYTHON) standalone.py
	@rm standalone.py

preview:       ## Run the builtin development server
	$(PYTHON) -m mkdocs serve

docs:          ## Build the MkDocs documentation
	$(PYTHON) -m mkdocs Build

uncache:       ## Remove __pycache__ directories
	# https://stackoverflow.com/questions/28991015/python3-project-remove-pycache-folders-and-pyc-files
	find . -type d -name  "__pycache__" -exec rm -r {} +
