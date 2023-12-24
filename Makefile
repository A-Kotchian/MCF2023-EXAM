OS := $(shell uname)
FILE := requirements.txt

libraries:
ifeq ($(OS),Linux)
	pip install -r $(FILE) --break-system-packages
	@echo "Your libraries are successfully installed on Linux!"
else ifeq ($(OS),Windows_NT)
	pip install -r $(FILE)
	@echo "Your libraries are successfully installed on Windows!"
else
	pip install -r $(FILE)
	@echo "Your libraries are successfully installed!"
endif

