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

def test_can_clone_a_git_repository_and_show_log():
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
    
