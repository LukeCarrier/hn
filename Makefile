#
# HyperNova server management framework
#
# Makefile wrapper for build actions
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

BUILD_ROOT_DIR := $(CURDIR)
BUILD_TEMP_DIR := $(shell mktemp -d)

ELEVATOR_VERSION     := 0.1.0
ELEVATOR_SOURCE_DIR  := $(BUILD_ROOT_DIR)/deps/elevator
ELEVATOR_RPM_PREFIX  := /usr/local/hypernova
ELEVATOR_VENV_PREFIX := $(BUILD_ROOT_DIR)/chroot

HYPERNOVA_CHROOT_DIR := $(BUILD_ROOT_DIR)/chroot
HYPERNOVA_RPM_PREFIX := /usr/local/hypernova
HYPERNOVA_SOURCE_DIR := $(BUILD_ROOT_DIR)/src
HYPERNOVA_VENV_DIR   := $(BUILD_ROOT_DIR)/chroot
HYPERNOVA_VERSION    := 0.1.0

PYTHON_VERSION               := 3.2.3
PYTHON_SOURCE_URL            := http://python.org/ftp/python/$(PYTHON_VERSION)/Python-$(PYTHON_VERSION).tar.bz2
PYTHON_SOURCE_DIR            := $(BUILD_ROOT_DIR)/deps/python
PYTHON_RPM_PREFIX            := /usr/local/hypernova
PYTHON_VENV_PREFIX           := $(BUILD_ROOT_DIR)/chroot
PYTHON_VENV_BINARY           := $(BUILD_ROOT_DIR)/chroot/bin/python3.2
PYTHON_VENV_LIBRARY_DIR      := $(PYTHON_VENV_PREFIX)/lib/python3.2
PYTHON_VENV_SITEPACKAGES_DIR := $(PYTHON_VENV_LIBRARY_DIR)/site-packages

PYTHON_DISTRIBUTE_VERSION    := 0.6.28
PYTHON_DISTRIBUTE_SOURCE_DIR := $(BUILD_ROOT_DIR)/deps/python-distribute
PYTHON_DISTRIBUTE_SOURCE_URL := http://pypi.python.org/packages/source/d/distribute/distribute-$(PYTHON_DISTRIBUTE_VERSION).tar.gz
PYTHON_DISTRIBUTE_RPM_PREFIX := /usr/local/hypernova

PYTHON_GNUPG_VERSION    := 0.3.0
PYTHON_GNUPG_SOURCE_DIR := $(BUILD_ROOT_DIR)/deps/python-gnupg
PYTHON_GNUPG_RPM_PREFIX := /usr/local/hypernova

PYTHON_OURSQL_VERSION    := 0.9.2
PYTHON_OURSQL_SOURCE_DIR := $(BUILD_ROOT_DIR)/deps/python-oursql
PYTHON_OURSQL_RPM_PREFIX := /usr/local/hypernova

PYTHON_PEXPECT_VERSION    := 2.3
PYTHON_PEXPECT_SOURCE_DIR := $(BUILD_ROOT_DIR)/deps/python-pexpect
PYTHON_PEXPECT_RPM_PREFIX := /usr/local/hypernova

PHING_DEPLOY_VERSION     := 1.0.0
PHING_DEPLOY_SOURCE_DIR  := $(BUILD_ROOT_DIR)/deps/oss-build-system/
PHING_DEPLOY_RPM_PREFIX  := /usr/local/hypernova
PHING_DEPLOY_VENV_PREFIX := $(BUILD_ROOT_DIR)/chroot

RPM_BUILD_DIR  := $(BUILD_ROOT_DIR)/build/rpm
RPM_OUTPUT_DIR := $(BUILD_ROOT_DIR)/dist/rpm
RPM_SPEC_DIR   := $(BUILD_ROOT_DIR)/build

all:
	@echo HyperNova
	@echo =========
	@echo
	@echo Primary targets
	@echo ---------------
	@echo
	@echo '+-------------------------+----------------------------------------+'
	@echo '| Target                  | Description                            |'
	@echo '+-------------------------+----------------------------------------+'
	@echo '| build                   | build HyperNova and all dependencies   |'
	@echo '| clean                   | clean all build artefacts              |'
	@echo '| rpm                     | generate RPM packages of HyperNova and |'
	@echo '|                         | dependencies                           |'
	@echo '| venv                    | build the tree and install it to a     |'
	@echo '|                         | virtualenv                             |'
	@echo '+-------------------------+----------------------------------------+'
	@echo
	@echo Specific targets
	@echo ----------------
	@echo
	@echo '+-------------------------+----------------------------------------+'
	@echo '| Target                  | Description                            |'
	@echo '+-------------------------+----------------------------------------+'
	@echo '| build-elevator          | build just Elevator                    |'
	@echo '| build-hypernova         | build just HyperNova                   |'
	@echo '| build-python            | build just Python                      |'
	@echo '| build-python-distribute | build just Python Distribute module    |'
	@echo '| build-python-gnupg      | build just Python GnuPG module         |'
	@echo '| build-python-oursql     | build just Python OurSQL module        |'
	@echo '| build-python-pexpect    | build just Python pexpect module       |'
	@echo '| build-phing-deploy      | build just Phing                       |'
	@echo '| clean-elevator          | clean just Elevator build artefacts    |'
	@echo '| clean-hypernova         | clean just HyperNova build artefacts   |'
	@echo '| clean-python            | clean just Python build artefacts      |'
	@echo '| clean-python-distribute | clean just Python Distribute module    |'
	@echo '|                         | build artefacts                        |'
	@echo '| clean-python-gnupg      | clean just Python GnuPG module build   |'
	@echo '|                         | artefacts                              |'
	@echo '| clean-python-oursql     | clean just Python OurSQL module build  |'
	@echo '|                         | artefacts                              |'
	@echo '| clean-python-pexpect    | clean just Python pexpect module build |'
	@echo '|                         | artefacts                              |'
	@echo '| clean-phing-deploy      | clean just Phing                       |'
	@echo '| rpm-elevator            | generate RPM packages of just Elevator |'
	@echo '| rpm-hypernova           | generate RPM packages of just          |'
	@echo '|                         | HyperNova                              |'
	@echo '| rpm-python              | generate RPM packages of just Python   |'
	@echo '| rpm-python-distribute   | generate RPM packages of just Python   |'
	@echo '|                         | Distribute module                      |'
	@echo '| rpm-python-gnupg        | generate RPM packages of just Python   |'
	@echo '|                         | GnuPG module                           |'
	@echo '| rpm-python-oursql       | generate RPM packages of just Python   |'
	@echo '|                         | OurSQL module                          |'
	@echo '| rpm-python-pexpect      | generate RPM packages of just Python   |'
	@echo '|                         | pexpect module                         |'
	@echo '| venv-elevator           | build and install just Elevator        |'
	@echo '| venv-hypernova          | build and install just HyperNova       |'
	@echo '| venv-python             | build and install just Python          |'
	@echo '| venv-python-distribute  | build and install just Python          |'
	@echo '|                         | Distribute module                      |'
	@echo '| venv-python-gnupg       | build and install just Python GnuPG    |'
	@echo '|                         | module                                 |'
	@echo '| venv-python-oursql      | build and install just Python OurSQL   |'
	@echo '|                         | module                                 |'
	@echo '| venv-python-pexpect     | build and install just Python pexpect  |'
	@echo '|                         | module                                 |'
	@echo '+-------------------------+----------------------------------------+'

.PHONY: all build                   clean                   rpm                   venv
.PHONY:     build-elevator          clean-elevator          rpm-elevator          venv-elevator
.PHONY:     build-hypernova         clean-hypernova         rpm-hypernova         venv-hypernova
.PHONY:     build-python            clean-python            rpm-python            venv-python
.PHONY:     build-python-distribute clean-python-distribute rpm-python-distribute venv-python-distribute
.PHONY:     build-python-gnupg      clean-python-gnupg      rpm-python-gnupg      venv-python-gnupg
.PHONY:     build-python-oursql     clean-python-oursql     rpm-python-oursql     venv-python-oursql
.PHONY:     build-python-pexpect    clean-python-pexpect    rpm-python-pexpect    venv-python-pexpect
.PHONY:     build-phing-deploy      clean-phing-deploy      rpm-phing-deploy      venv-phing-deploy

build: build-elevator build-hypernova build-python build-python-distribute build-python-gnupg build-python-oursql build-python-pexpect build-phing-deploy

build-elevator:
	$(BUILD_ROOT_DIR)/build/build-elevator.sh \
		--elevator-source-dir $(ELEVATOR_SOURCE_DIR)

build-hypernova: venv-python-distribute
	$(BUILD_ROOT_DIR)/build/build-python-module.sh \
		--python-binary $(PYTHON_VENV_BINARY) \
		--python-module-name "hypernova" \
		--python-module-source-dir $(HYPERNOVA_SOURCE_DIR)

build-python:
	$(BUILD_ROOT_DIR)/build/build-python.sh \
		--build-temp-dir $(BUILD_TEMP_DIR) \
		--python-source-url $(PYTHON_SOURCE_URL) \
		--python-source-dir $(PYTHON_SOURCE_DIR)

build-python-distribute:
	$(BUILD_ROOT_DIR)/build/build-python-module.sh \
		--build-temp-dir $(BUILD_TEMP_DIR) \
		--python-binary $(PYTHON_VENV_BINARY) \
		--python-module-name "distribute" \
		--python-module-source-dir $(PYTHON_DISTRIBUTE_SOURCE_DIR) \
		--python-module-source-url $(PYTHON_DISTRIBUTE_SOURCE_URL)

build-python-gnupg: venv-python-distribute
	$(BUILD_ROOT_DIR)/build/build-python-module.sh \
		--python-binary $(PYTHON_VENV_BINARY) \
		--python-module-name "gnupg" \
		--python-module-source-dir $(PYTHON_GNUPG_SOURCE_DIR) \
		--python-module-version $(PYTHON_GNUPG_VERSION)

build-python-oursql: venv-python-distribute
	$(BUILD_ROOT_DIR)/build/build-python-module.sh \
		--python-binary $(PYTHON_VENV_BINARY) \
		--python-module-name "oursql" \
		--python-module-source-dir $(PYTHON_OURSQL_SOURCE_DIR) \
		--python-module-version $(PYTHON_OURSQL_VERSION)

build-python-pexpect: venv-python-distribute
	$(BUILD_ROOT_DIR)/build/build-python-module.sh \
		--python-binary $(PYTHON_VENV_BINARY) \
		--python-module-name "pexpect" \
		--python-module-source-dir $(PYTHON_PEXPECT_SOURCE_DIR) \
		--python-module-version $(PYTHON_PEXPECT_VERSION)


build-phing-deploy:
	$(BUILD_ROOT_DIR)/build/build-phing-deploy.sh \
			--source-dir $(PHING_DEPLOY_SOURCE_DIR)

clean: clean-elevator clean-hypernova clean-python clean-python-distribute clean-python-gnupg clean-python-oursql clean-python-pexpect clean-phing-deploy

clean-elevator:
	$(BUILD_ROOT_DIR)/build/clean-elevator.sh \
		--elevator-source-dir $(ELEVATOR_SOURCE_DIR) \
		--rpm-output-dir $(RPM_OUTPUT_DIR)

clean-hypernova:
	$(BUILD_ROOT_DIR)/build/clean-hypernova.sh \
		--hypernova-source-dir $(HYPERNOVA_SOURCE_DIR) \
		--rpm-output-dir $(RPM_OUTPUT_DIR)

clean-python:
	$(BUILD_ROOT_DIR)/build/clean-python.sh \
		--python-source-dir $(PYTHON_SOURCE_DIR) \
		--rpm-output-dir $(RPM_OUTPUT_DIR)

clean-python-distribute:
	$(BUILD_ROOT_DIR)/build/clean-python-module.sh \
		--python-module-name "distribute" \
		--python-module-source-dir $(PYTHON_DISTRIBUTE_SOURCE_DIR) \
		--rpm-output-dir $(RPM_OUTPUT_DIR)

clean-python-gnupg:
	$(BUILD_ROOT_DIR)/build/clean-python-module.sh \
		--is-local-submodule \
		--python-module-name "gnupg" \
		--python-module-source-dir $(PYTHON_GNUPG_SOURCE_DIR) \
		--rpm-output-dir $(RPM_OUTPUT_DIR)

clean-python-oursql:
	$(BUILD_ROOT_DIR)/build/clean-python-module.sh \
		--is-local-submodule \
		--python-module-name "oursql" \
		--python-module-source-dir $(PYTHON_OURSQL_SOURCE_DIR) \
		--rpm-output-dir $(RPM_OUTPUT_DIR)

clean-python-pexpect:
	$(BUILD_ROOT_DIR)/build/clean-python-module.sh \
		--is-local-submodule \
		--python-module-name "pexpect" \
		--python-module-source-dir $(PYTHON_PEXPECT_SOURCE_DIR) \
		--rpm-output-dir $(RPM_OUTPUT_DIR)

clean-phing-deploy:
	$(BUILD_ROOT_DIR)/build/clean-phing-deploy.sh \
		--source-dir $(PHING_DEPLOY_SOURCE_DIR) \
		--rpm-output-dir $(RPM_OUTPUT_DIR)


dep-rhel:
	yum -y install \
		gcc git make wget \
		{mysql,zlib}-devel

rpm: venv rpm-elevator rpm-hypernova rpm-python rpm-python-distribute rpm-python-gnupg rpm-python-oursql rpm-python-pexpect

rpm-elevator: build-elevator
	$(BUILD_ROOT_DIR)/build/rpm-elevator.sh \
		--elevator-rpm-prefix $(ELEVATOR_RPM_PREFIX) \
		--elevator-source-dir $(ELEVATOR_SOURCE_DIR) \
		--elevator-version $(ELEVATOR_VERSION) \
		--rpm-build-dir $(RPM_BUILD_DIR) \
		--rpm-output-dir $(RPM_OUTPUT_DIR) \
		--rpm-spec-dir $(RPM_SPEC_DIR)

rpm-hypernova: build-hypernova
	$(BUILD_ROOT_DIR)/build/rpm-hypernova.sh \
		--hypernova-rpm-prefix $(HYPERNOVA_RPM_PREFIX) \
		--hypernova-source-dir $(HYPERNOVA_SOURCE_DIR) \
		--hypernova-venv-dir $(HYPERNOVA_VENV_DIR) \
		--hypernova-version $(HYPERNOVA_VERSION) \
		--python-distribute-source-dir $(PYTHON_DISTRIBUTE_SOURCE_DIR) \
		--python-source-dir $(PYTHON_SOURCE_DIR) \
		--rpm-build-dir $(RPM_BUILD_DIR) \
		--rpm-output-dir $(RPM_OUTPUT_DIR) \
		--rpm-spec-dir $(RPM_SPEC_DIR)

rpm-python: build-python
	$(BUILD_ROOT_DIR)/build/rpm-python.sh \
		--python-rpm-prefix $(PYTHON_RPM_PREFIX) \
		--python-source-dir $(PYTHON_SOURCE_DIR) \
		--python-version $(PYTHON_VERSION) \
		--rpm-build-dir $(RPM_BUILD_DIR) \
		--rpm-output-dir $(RPM_OUTPUT_DIR) \
		--rpm-spec-dir $(RPM_SPEC_DIR)

rpm-python-distribute: build-python-distribute
	$(BUILD_ROOT_DIR)/build/rpm-python-module.sh \
		--python-module-name "distribute" \
		--python-module-st-name "distribute" \
		--python-module-rpm-prefix $(PYTHON_DISTRIBUTE_RPM_PREFIX) \
		--python-module-source-dir $(PYTHON_DISTRIBUTE_SOURCE_DIR) \
		--python-module-version $(PYTHON_DISTRIBUTE_VERSION) \
		--python-source-dir $(PYTHON_SOURCE_DIR) \
		--rpm-build-dir $(RPM_BUILD_DIR) \
		--rpm-output-dir $(RPM_OUTPUT_DIR) \
		--rpm-spec-dir $(RPM_SPEC_DIR)

rpm-python-gnupg: build-python-gnupg
	$(BUILD_ROOT_DIR)/build/rpm-python-module.sh \
		--python-distribute-source-dir $(PYTHON_DISTRIBUTE_SOURCE_DIR) \
		--python-module-st-name "python_gnupg" \
		--python-module-name "gnupg" \
		--python-module-rpm-prefix $(PYTHON_GNUPG_RPM_PREFIX) \
		--python-module-source-dir $(PYTHON_GNUPG_SOURCE_DIR) \
		--python-module-version $(PYTHON_GNUPG_VERSION) \
		--python-source-dir $(PYTHON_SOURCE_DIR) \
		--rpm-build-dir $(RPM_BUILD_DIR) \
		--rpm-output-dir $(RPM_OUTPUT_DIR) \
		--rpm-spec-dir $(RPM_SPEC_DIR)

rpm-python-oursql: build-python-oursql
	$(BUILD_ROOT_DIR)/build/rpm-python-module.sh \
		--python-distribute-source-dir $(PYTHON_DISTRIBUTE_SOURCE_DIR) \
		--python-module-st-name "oursql" \
		--python-module-name "oursql" \
		--python-module-rpm-prefix $(PYTHON_OURSQL_RPM_PREFIX) \
		--python-module-source-dir $(PYTHON_OURSQL_SOURCE_DIR) \
		--python-module-version $(PYTHON_OURSQL_VERSION) \
		--python-source-dir $(PYTHON_SOURCE_DIR) \
		--rpm-build-dir $(RPM_BUILD_DIR) \
		--rpm-output-dir $(RPM_OUTPUT_DIR) \
		--rpm-spec-dir $(RPM_SPEC_DIR)

rpm-python-pexpect: build-python-pexpect
	$(BUILD_ROOT_DIR)/build/rpm-python-module.sh \
		--python-distribute-source-dir $(PYTHON_DISTRIBUTE_SOURCE_DIR) \
		--python-module-st-name "pexpect" \
		--python-module-name "pexpect" \
		--python-module-rpm-prefix $(PYTHON_PEXPECT_RPM_PREFIX) \
		--python-module-source-dir $(PYTHON_PEXPECT_SOURCE_DIR) \
		--python-module-version $(PYTHON_PEXPECT_VERSION) \
		--python-source-dir $(PYTHON_SOURCE_DIR) \
		--rpm-build-dir $(RPM_BUILD_DIR) \
		--rpm-output-dir $(RPM_OUTPUT_DIR) \
		--rpm-spec-dir $(RPM_SPEC_DIR)

rpm-phing-deploy: build-phing-deploy
	$(BUILD_ROOT_DIR)/build/rpm-phing-deploy.sh \
		--rpm-prefix $(PHING_DEPLOY_RPM_PREFIX) \
		--source-dir $(PHING_DEPLOY_SOURCE_DIR) \
		--version $(PHING_DEPLOY_VERSION) \
		--rpm-build-dir $(RPM_BUILD_DIR) \
		--rpm-output-dir $(RPM_OUTPUT_DIR) \
		--rpm-spec-dir $(RPM_SPEC_DIR)


venv: venv-elevator venv-python venv-python-distribute venv-python-gnupg venv-python-oursql venv-python-pexpect venv-phing-deploy

venv-elevator: build-elevator
	$(BUILD_ROOT_DIR)/build/venv-elevator.sh \
		--elevator-source-dir $(ELEVATOR_SOURCE_DIR) \
		--elevator-venv-prefix $(ELEVATOR_VENV_PREFIX)

venv-hypernova: build-hypernova venv-python venv-python-distribute
	$(BUILD_ROOT_DIR)/build/venv-python-module.sh \
		--python-binary $(PYTHON_VENV_BINARY) \
		--python-module-st-name "HyperNova" \
		--python-module-source-dir $(HYPERNOVA_SOURCE_DIR) \
		--python-module-version $(HYPERNOVA_VERSION)  \
		--python-sitepackages-dir $(PYTHON_VENV_SITEPACKAGES_DIR)

venv-python: build-python
	$(BUILD_ROOT_DIR)/build/venv-python.sh \
		--python-binary $(PYTHON_VENV_BINARY) \
		--python-source-dir $(PYTHON_SOURCE_DIR) \
		--python-venv-prefix $(PYTHON_VENV_PREFIX)

venv-python-distribute: build-python-distribute venv-python
	$(BUILD_ROOT_DIR)/build/venv-python-module.sh \
		--python-binary $(PYTHON_VENV_BINARY) \
		--python-module-st-name "distribute" \
		--python-module-source-dir $(PYTHON_DISTRIBUTE_SOURCE_DIR) \
		--python-module-version $(PYTHON_DISTRIBUTE_VERSION) \
		--python-sitepackages-dir $(PYTHON_VENV_SITEPACKAGES_DIR)

venv-python-gnupg: build-python-gnupg venv-python venv-python-distribute
	$(BUILD_ROOT_DIR)/build/venv-python-module.sh \
		--python-binary $(PYTHON_VENV_BINARY) \
		--python-module-st-name "python_gnupg" \
		--python-module-source-dir $(PYTHON_GNUPG_SOURCE_DIR) \
		--python-module-version $(PYTHON_GNUPG_VERSION) \
		--python-sitepackages-dir $(PYTHON_VENV_SITEPACKAGES_DIR)

venv-python-oursql: build-python-oursql venv-python venv-python-distribute
	$(BUILD_ROOT_DIR)/build/venv-python-module.sh \
		--python-binary $(PYTHON_VENV_BINARY) \
		--python-module-st-name "oursql" \
		--python-module-source-dir $(PYTHON_OURSQL_SOURCE_DIR) \
		--python-module-version $(PYTHON_OURSQL_VERSION) \
		--python-sitepackages-dir $(PYTHON_VENV_SITEPACKAGES_DIR)

venv-python-pexpect: build-python-pexpect venv-python venv-python-distribute
	$(BUILD_ROOT_DIR)/build/venv-python-module.sh \
		--python-binary $(PYTHON_VENV_BINARY) \
		--python-module-st-name "pexpect" \
		--python-module-source-dir $(PYTHON_PEXPECT_SOURCE_DIR) \
		--python-module-version $(PYTHON_PEXPECT_VERSION) \
		--python-sitepackages-dir $(PYTHON_VENV_SITEPACKAGES_DIR)

venv-phing-deploy: build-phing-deploy
	$(BUILD_ROOT_DIR)/build/venv-phing-deploy.sh \
		--source-dir $(PHING_DEPLOY_SOURCE_DIR) \
		--venv-prefix $(PHING_DEPLOY_VENV_PREFIX)
