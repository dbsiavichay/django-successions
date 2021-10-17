# Makefile generated with pymakefile
help:
	@grep -E '^[A-Za-z0-9_.-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "[36m%-30s[0m %s\n", $$1, $$2}'

prettify:  ## Fix code to pep8 standards
	./scripts/pre-push.sh

supersuser: # Create django superuser
	python3 manage.py createsuperuser

