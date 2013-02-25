PROJECT_NAME=yaproject
MANAGE=cd $(PROJECT_NAME) && python manage.py
APP=vcard


test:
	@echo Start tests for $(PROJECT_NAME) ...
	$(MANAGE) test $(APP)

test_coverage:
	@echo Start test test_coverage for $(PROJECT_NAME) ...
	$(MANAGE) test_coverage $(APP)
