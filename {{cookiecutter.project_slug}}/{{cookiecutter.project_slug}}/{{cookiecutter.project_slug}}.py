#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: {{cookiecutter.project_slug}}.py
{% if cookiecutter.license == "MIT" -%}
#
# Copyright {{ cookiecutter.year }} {{ cookiecutter.full_name }}
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
#
{% elif cookiecutter.license == "BSD-3" -%}
#
# Copyright {{ cookiecutter.year }} {{ cookiecutter.full_name }}
#
# Redistribution and use in source and binary forms, with or without modification,
#  are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#  this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#  this list of conditions and the following disclaimer in the documentation and/or
#  other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#  may be used to endorse or promote products derived from this software without
#  specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
#  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
#  INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
#  BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
#  OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
#  ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
{% elif cookiecutter.license == "GNU GPL v3.0" -%}
#
# Copyright (C) {{ cookiecutter.year }} {{ cookiecutter.full_name }}
#
# This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
{% elif cookiecutter.license == "Apache Software License 2.0" -%}
#
# Copyright {{ cookiecutter.year }} {{ cookiecutter.full_name }}
#
# Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
{% endif %}
"""
Main code for {{cookiecutter.project_slug}}.

.. _Google Python Style Guide:
   https://google.github.io/styleguide/pyguide.html

"""

import logging
{%- if cookiecutter.project_type == "cli" %}
import logging.config
import json
import argparse
import coloredlogs
{% endif %}

__author__ = '''{{cookiecutter.full_name}} <{{cookiecutter.email}}>'''
__docformat__ = '''google'''
__date__ = '''{{cookiecutter.release_date}}'''
__copyright__ = '''Copyright {{ cookiecutter.year }}, {{ cookiecutter.full_name }}'''
__credits__ = ["{{cookiecutter.full_name}}"]
__license__ = '''{{cookiecutter.license}}'''
__maintainer__ = '''{{cookiecutter.full_name}}'''
__email__ = '''<{{cookiecutter.email}}>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".


# This is the main prefix used for logging
LOGGER_BASENAME = '''{{cookiecutter.project_slug}}'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())
{%- if cookiecutter.project_type == "cli" %}


def get_arguments():
    """
    Gets us the cli arguments.

    Returns the args as parsed from the argsparser.
    """
    # https://docs.python.org/3/library/argparse.html
    parser = argparse.ArgumentParser(description='''{{cookiecutter.project_short_description}}''')
    parser.add_argument('--log-config',
                        '-l',
                        action='store',
                        dest='logger_config',
                        help='The location of the logging config json file',
                        default='')
    parser.add_argument('--log-level',
                        '-L',
                        help='Provide the log level. Defaults to info.',
                        dest='log_level',
                        action='store',
                        default='info',
                        choices=['debug',
                                 'info',
                                 'warning',
                                 'error',
                                 'critical'])

    # examples:
    parser.add_argument('--long', '-s',
                        choices=['a', 'b'],
                        dest='parameter_long',
                        action='store',
                        help='Describe the parameter here',
                        default='a',
                        type=str,
                        required=True)
    parser.add_argument('--feature',
                        dest='feature',
                        action='store_true')
    parser.add_argument('--no-feature',
                        dest='feature',
                        action='store_false')
    args = parser.parse_args()
    return args


def setup_logging(level, config_file=None):
    """
    Sets up the logging.

    Needs the args to get the log level supplied

    Args:
        level: At which level do we log
        config_file: Configuration to use

    """
    # This will configure the logging, if the user has set a config file.
    # If there's no config file, logging will default to stdout.
    if config_file:
        # Get the config for the logger. Of course this needs exception
        # catching in case the file is not there and everything. Proper IO
        # handling is not shown here.
        try:
            with open(config_file) as conf_file:
                configuration = json.loads(conf_file.read())
                # Configure the logger
                logging.config.dictConfig(configuration)
        except ValueError:
            print(f'File "{config_file}" is not valid json, cannot continue.')
            raise SystemExit(1)
    else:
        coloredlogs.install(level=level.upper())


def main():
    """
    Main method.

    This method holds what you want to execute when
    the script is run on command line.
    """
    args = get_arguments()
    setup_logging(args.log_level, args.logger_config)
    # Main code goes here


if __name__ == '__main__':
    main(){% endif %}
