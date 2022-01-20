POETRY = poetry
PYTHON = $(POETRY) run python


.PHONY: demo
demo:
	$(PYTHON) dictToFoam conv tutorials/incompressible/simpleFoam/airFoil2D.yaml

.PHONY: test
test:
	for version in 7 ; do \
		$(PYTHON) dictToFoam conv tutorials --directory test --version $$version --exist-ok ; \
		$(PYTHON) dictToFoam test           --directory test --version $$version ; \
	done
