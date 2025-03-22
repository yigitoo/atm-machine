install:
	@echo "Installing Dependencies"
	pip3 install -r requirements.txt
	@echo "Dependencies Installed"

install-win:
	@echo "Installing Windows Dependencies"
	pip3 install -r requirements.txt
	@echo "Windows Dependencies Installed"

install-linux:
	@echo "Installing Linux Dependencies"
	pip3 install -r requirements.txt
	@echo "Linux Dependencies Installed"

run-client:
	@echo "Running Client"
	python3 atm_machine/client/ui.py

run-server:
	@echo "Running Server"
	python3 atm_machine/server/server.py
