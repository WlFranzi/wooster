VENV_DIR=./venv
VENV_ACTIVATE_SCRIPT=$(VENV_DIR)/bin/activate
LOGFILE=eval.log

default: ask-wooster

venv:
ifeq ("","$(wildcard "$(VENV_ACTIVATE_SCRIPT)")")
	@virtualenv $(VENV_DIR)
	@\
		. "$(VENV_ACTIVATE_SCRIPT)"; \
		pip install pip==8.1.1; \
		pip install pip-tools
endif

requirements.txt: venv requirements.in
	@. $(VENV_ACTIVATE_SCRIPT); pip-compile

deps: requirements.txt
	@echo "Dependencies compiled and up to date"

install: venv requirements.txt
	@echo "Synching dependencies..."
	@. $(VENV_ACTIVATE_SCRIPT); pip-sync

reinstall:
	@rm -rf $(VENV_DIR)
	@make install

lint: install 
	@echo "Running pep8..."; . $(VENV_ACTIVATE_SCRIPT); pep8 src/ && echo "OK!"
	@echo "Running flake8..."; . $(VENV_ACTIVATE_SCRIPT); flake8 src/ && echo "OK!"

clean:
	@find src/ -iname "*.pyc" -exec rm {} \;

console: install
	@. $(VENV_ACTIVATE_SCRIPT); cd src; ipython

test: install
	@. $(VENV_ACTIVATE_SCRIPT); nosetests tests/

.PHONY: default deps install reinstall lint clean console test

ask-wooster: install src/*.py
	@. $(VENV_ACTIVATE_SCRIPT); cd src;\
	 python cli.py ../resources/question.txt ../resources/_preprocessed ../resources/answer.txt

check-wooster: install
	@cd resources; perl eval.pl pattern.txt answer.txt > $(LOGFILE)
	@cd resources; tail -n 2 $(LOGFILE)

test-wooster: install
	@. $(VENV_ACTIVATE_SCRIPT); cd src;\
	 python cli.py ../resources/question_test.txt ../resources/_preprocessed_test ../resources/answer_test.txt

preprocess: install
	@rm -rf resources/_preprocessed; mkdir resources/_preprocessed
	@source $(VENV_ACTIVATE_SCRIPT); cd src;\
	 python preprocess.py ../resources/doc_dev ../resources/_preprocessed

preprocess-test: install
	@rm -rf resources/_preprocessed_test; mkdir resources/_preprocessed_test
	@source $(VENV_ACTIVATE_SCRIPT); cd src;\
	 python preprocess.py ../resources/doc_test ../resources/_preprocessed_test

.PHONY: ask-wooster check-wooster test-wooster preprocess preprocess-test
