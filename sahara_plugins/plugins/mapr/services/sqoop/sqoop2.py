# Copyright (c) 2015, MapR Technologies
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


import sahara_plugins.plugins.mapr.domain.node_process as np
import sahara_plugins.plugins.mapr.domain.service as s
import sahara_plugins.plugins.mapr.util.validation_utils as vu


SQOOP_2_SERVER = np.NodeProcess(
    name='sqoop2',
    ui_name='Sqoop2-Server',
    package='mapr-sqoop2-server',
    open_ports=[12000]
)
SQOOP_2_CLIENT = np.NodeProcess(
    name='sqoop-client',
    ui_name='Sqoop2-Client',
    package='mapr-sqoop2-client'
)


class Sqoop2(s.Service):
    def __init__(self):
        super(Sqoop2, self).__init__()
        self._name = 'sqoop'
        self._ui_name = 'Sqoop2'
        self._version = '2.0.0'
        self._node_processes = [SQOOP_2_CLIENT, SQOOP_2_SERVER]
        self._validation_rules = [
            vu.exactly(1, SQOOP_2_SERVER),
        ]

    def post_install(self, cluster_context, instances):
        self._set_service_dir_owner(cluster_context, instances)
