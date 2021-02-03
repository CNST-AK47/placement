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

from oslo_policy import policy

RULE_ADMIN_API = 'rule:admin_api'
# NOTE(lbragstad): We might consider converting these generic checks into
# RuleDefaults or DocumentedRuleDefaults, but we need to thoroughly vet the
# approach in oslo.policy and consume a new version. Until we have that done,
# let's continue using generic check strings.
SYSTEM_ADMIN = 'role:admin and system_scope:all'
SYSTEM_READER = 'role:reader and system_scope:all'
PROJECT_READER = 'role:reader and project_id:%(project_id)s'
PROJECT_READER_OR_SYSTEM_READER = f'({SYSTEM_READER}) or ({PROJECT_READER})'

rules = [
    policy.RuleDefault(
        "admin_api",
        "role:admin",
        description="Default rule for most placement APIs.",
        scope_types=['system']),
]


def list_rules():
    return rules
