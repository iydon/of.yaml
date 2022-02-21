POETRY = poetry
PYTHON = $(POETRY) run python


.PHONY: help demo shell test

help:          ## 打印帮助信息
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

demo:          ## 运行示例程序
	$(PYTHON) foam conv tutorials/incompressible/simpleFoam/airFoil2D.yaml

dependencies:  ## 以树状形式列出依赖关系
	@$(POETRY) show --no-dev --tree

shell:         ## 在虚拟环境中生成 shell
	@$(POETRY) shell

test:          ## 运行测试程序
	for version in 7 ; do \
		$(PYTHON) foam conv tutorials --directory test --version $$version --exist-ok ; \
		$(PYTHON) foam test           --directory test --version $$version ; \
	done
