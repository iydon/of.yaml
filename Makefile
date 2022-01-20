POETRY = poetry
PYTHON = $(POETRY) run python


.PHONY: test
test:
	for version in 7 ; do \
		$(PYTHON) dictToFoam conv tutorials --directory test --version $$version --exist-ok ; \
		$(PYTHON) dictToFoam test           --directory test --version $$version ; \
	done
