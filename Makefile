install:
	@echo "Installing Dependencies"
	pip3 install -r requirements.txt
	@echo "Dependencies Installed"


run-client:
	@echo "Running Client"
	@echo "---------------------"
	python3 ui.py

run-server:
	@echo "Running Server"
	@echo "---------------------"
	python3 server.py
