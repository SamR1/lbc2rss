include Makefile.config
-include Makefile.custom.config
.SILENT:


check-all: lint type-check test

make-p:
	# Launch all P targets in parallel and exit as soon as one exits.
	set -m; (for p in $(P); do ($(MAKE) $$p || kill 0)& done; wait)

clean:
	rm -rf $(VENV)
	rm -rf .eggs
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf pip-wheel-metadata/

install: venv
	$(PIP) install -e .

install-dev: venv
	$(PIP) install -e .[test]

lint:
	$(PYTEST) --flake8 --isort --mypy -m "flake8 or isort or mypy" $(FLASK_APP)

lint-fix:
	$(BLACK) $(FLASK_APP)

run:
	echo 'running server on http://$(HOST):$(PORT)'
	cd $(FLASK_APP) && $(GUNICORN) -b $(HOST):$(PORT) "$(FLASK_APP):create_app()" --error-logfile ../gunicorn-error.log

serve:
	$(FLASK) run --with-threads -h $(HOST) -p $(PORT)

test:
	$(PYTEST) $(FLASK_APP)/tests --cov $(FLASK_APP) --cov-report term-missing $(PYTEST_ARGS)

type-check:
	$(MYPY) $(FLASK_APP)

venv:
	test -d $(VENV) || $(PYTHON_VERSION) -m venv $(VENV)
