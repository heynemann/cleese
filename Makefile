# Copyright Bernardo Heynemann <heynemann@gmail.com>

# Licensed under the Open Software License ("OSL") v. 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.opensource.org/licenses/osl-3.0.php

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Makefile for cleese
SHELL := /bin/bash

root_dir=.
build_dir=${root_dir}/build
src_dir=${root_dir}/cleese

tests_dir=${root_dir}/tests
unit_tests_dir=${tests_dir}/unit
functional_tests_dir=${tests_dir}/functional

all: compile test

compile:
	@echo "Compiling source code..."
	@rm -f -r ${src_dir}/*.pyc >> /dev/null
	@python -m compileall ${src_dir}

test: compile
	@echo "Running unit tests..."
	@nosetests -s --verbose --with-coverage --cover-package=cleese ${unit_tests_dir} ${functional_tests_dir}

deb:
	mv .git /tmp/cleese_git
	python -c 'import os;os.system("debuild")'
	mv /tmp/cleese_git .git
