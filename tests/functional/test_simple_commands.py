#!/usr/bin/env python
#-*- coding:utf-8 -*-

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

import time

from cleese import Executer, Status

def test_can_perform_ls():
    max_loops = 10
    executer = Executer(command="ls -la")
    executer.execute()
    
    for i in range(max_loops):
        if executer.poll():
            break
        time.sleep(0.1)
    
    assert executer.result.status == Status.success, \
                                "Expected status: %s Got: %s" % \
                                (Status.success, executer.result.status)
    assert executer.result.log
    assert executer.result.exit_code == 0

def test_can_read_output_of_a_running_command():
    max_loops = 30
    executer = Executer(command="ls -la && sleep 4")
    executer.execute()
    
    items_read = 0
    for i in range(max_loops):
        if executer.poll():
            break
        assert executer.result.log, "Expected log to be filled but it was empty."
        items_read += 1
        time.sleep(0.1)

    assert executer.result.status == Status.success, \
                                "Expected status: %s Got: %s" % \
                                (Status.success, executer.result.status)

    assert items_read > 10, "Expected greater than %s, got %s" % (10, items_read)

def test_loop_and_show_log():
    command = "for i in 1 2 3 4 5 6 7 8 9 10; do echo \"Welcome $i times\" && sleep 1; done"
    max_loops = 30
    executer = Executer(command=command)
    executer.execute()
    
    items_read = 0
    for i in range(max_loops):
        if executer.poll():
            break
        print executer.result.log
        assert executer.result.log, "Expected log to be filled but it was empty."
        items_read += 1
        time.sleep(1)

    assert executer.result.status == Status.success, \
                                "Expected status: %s Got: %s" % \
                                (Status.success, executer.result.status)

    assert items_read > 8, "Expected greater than %s, got %s" % (8, items_read)

def __test_can_clone_a_git_repository_and_show_log():
    repo_url = "git://github.com/heynemann/pyccuracy.git"
    executer = Executer(command="rm -rf /tmp/pyccuracy && cd /tmp/ && git clone %s" % repo_url)
    executer.execute()
    
    items_read = 0
    while not executer.poll():
        print "%d %s" % (items_read, executer.result.log)

        if executer.result.log:
            items_read += 1
        time.sleep(0.1)

    print executer.result.log
    assert executer.result.status == Status.success, \
                                "Expected status: %s Got: %s" % \
                                (Status.success, executer.result.status)

    assert items_read > 10, "Expected greater than %s, got %s" % (10, items_read)
    
