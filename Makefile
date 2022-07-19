
repo=localhost
user=pypiadmin
password=pypiadmin

install:
	python -m pip install -U pip
	pip install -i http://$(repo):8036 --trusted-host $(repo) -U --pre cloudshell_traffic
	pip install -i http://$(repo):8036 --trusted-host $(repo) -U --pre shellfoundry_traffic
	pip install -U -r requirements-dev.txt

.PHONY: build
build:
	shellfoundry install

download:
	pip download -i http://$(repo):8036 --trusted-host $(repo) --pre -r requirements-dev.txt -d dist/downloads
