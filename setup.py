# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os
import subprocess

from setuptools import setup, find_packages
from setuptools.command.sdist import sdist
from sphinx.setup_command import BuildDoc

from nova.utils import parse_mailmap, str_dict_replace

NOVA_VERSION = ['2011', '1']

VERSIONFILE_DEFAULT_VCS_VERSION = """
version_info = {"branch_nick": "LOCALBRANCH", "revision_id": "LOCALREVISION"}
"""

VERSIONFILE_DATA = """
# below this line automatically generated by setup.py

YEAR = %r
COUNT = %r
""" % (NOVA_VERSION[0], NOVA_VERSION[1])


VERSIONFILE_DATA += """

def string():
    return '.'.join([YEAR, COUNT])


def vcs_version_string():
    return "%s:%s" % (version_info['branch_nick'], version_info['revision_id'])


def string_with_vcs():
    return "%s-%s" % (string(), vcs_version_string())
"""

with open("nova/version.py", 'w') as version_file:
    if os.path.isdir('.bzr'):
        vcs_cmd = subprocess.Popen(["bzr", "version-info", "--python"],
                                   stdout=subprocess.PIPE)
        vcsversion = vcs_cmd.communicate()[0]
        version_file.write(vcsversion)
    else:
        version_file.write(VERSIONFILE_DEFAULT_VCS_VERSION)
    version_file.write(VERSIONFILE_DATA)


class local_BuildDoc(BuildDoc):
    def run(self):
        for builder in ['html', 'man']:
            self.builder = builder
            self.finalize_options()
            BuildDoc.run(self)

class local_sdist(sdist):
    """Customized sdist hook - builds the ChangeLog file from VC first"""

    def run(self):
        if os.path.isdir('.bzr'):
            # We're in a bzr branch
            env = os.environ.copy()
            env['BZR_PLUGIN_PATH'] = os.path.abspath('./bzrplugins')
            log_cmd = subprocess.Popen(["bzr", "log", "--novalog"],
                                       stdout=subprocess.PIPE, env=env)
            changelog = log_cmd.communicate()[0]
            mailmap = parse_mailmap()
            with open("ChangeLog", "w") as changelog_file:
                changelog_file.write(str_dict_replace(changelog, mailmap))
        sdist.run(self)

setup(name='nova',
      version='2011.1',
      description='cloud computing fabric controller',
      author='OpenStack',
      author_email='nova@lists.launchpad.net',
      url='http://www.openstack.org/',
      cmdclass={ 'sdist': local_sdist,
                 'build_sphinx' : local_BuildDoc },
      packages=find_packages(exclude=['bin', 'smoketests']),
      include_package_data=True,
      test_suite='nose.collector',
      scripts=['bin/nova-api',
               'bin/nova-compute',
               'bin/nova-dhcpbridge',
               'bin/nova-import-canonical-imagestore',
               'bin/nova-instancemonitor',
               'bin/nova-logspool',
               'bin/nova-manage',
               'bin/nova-network',
               'bin/nova-objectstore',
               'bin/nova-scheduler',
               'bin/nova-spoolsentry',
               'bin/nova-volume',
               'tools/nova-debug'])
