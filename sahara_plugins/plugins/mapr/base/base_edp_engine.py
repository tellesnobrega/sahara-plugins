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


import os

from sahara.plugins import context
from sahara.service.edp.job_binaries import manager as jb_manager
from sahara.plugins import edp
import sahara_plugins.plugins.mapr.util.maprfs_helper as mfs
import sahara_plugins.plugins.mapr.versions.version_handler_factory as vhf


class MapROozieJobEngine(edp.PluginsOozieJobEngine):
    def __init__(self, cluster):
        super(MapROozieJobEngine, self).__init__(cluster)
        self.cluster_context = self._get_cluster_context(self.cluster)

    hdfs_user = 'mapr'

    def get_hdfs_user(self):
        return MapROozieJobEngine.hdfs_user

    def create_hdfs_dir(self, remote, dir_name):
        mfs.create_maprfs4_dir(remote, dir_name, self.get_hdfs_user())

    def _upload_workflow_file(self, where, job_dir, wf_xml, hdfs_user):
        f_name = 'workflow.xml'
        with where.remote() as r:
            mfs.put_file_to_maprfs(r, wf_xml, f_name, job_dir, hdfs_user)
        return os.path.join(job_dir, f_name)

    def _upload_job_files_to_hdfs(self, where, job_dir, job, configs,
                                  proxy_configs=None):
        mains = job.mains or []
        libs = job.libs or []
        builtin_libs = edp.get_builtin_binaries(job, configs)
        uploaded_paths = []
        hdfs_user = self.get_hdfs_user()
        lib_dir = job_dir + '/lib'

        with where.remote() as r:
            for m in mains:
                path = jb_manager.JOB_BINARIES. \
                    get_job_binary_by_url(m.url). \
                    copy_binary_to_cluster(m, proxy_configs=proxy_configs,
                                           remote=r, context=context.ctx())
                target = os.path.join(job_dir, m.name)
                mfs.copy_from_local(r, path, target, hdfs_user)
                uploaded_paths.append(target)
            if len(libs) > 0:
                self.create_hdfs_dir(r, lib_dir)
            for l in libs:
                path = jb_manager.JOB_BINARIES. \
                    get_job_binary_by_url(l.url). \
                    copy_binary_to_cluster(l, proxy_configs=proxy_configs,
                                           remote=r, context=context.ctx())
                target = os.path.join(lib_dir, l.name)
                mfs.copy_from_local(r, path, target, hdfs_user)
                uploaded_paths.append(target)
            for lib in builtin_libs:
                mfs.put_file_to_maprfs(r, lib['raw'], lib['name'], lib_dir,
                                       hdfs_user)
                uploaded_paths.append(lib_dir + '/' + lib['name'])
        return uploaded_paths

    def get_name_node_uri(self, cluster):
        return self.cluster_context.name_node_uri

    def get_oozie_server_uri(self, cluster):
        return self.cluster_context.oozie_server_uri

    def get_oozie_server(self, cluster):
        return self.cluster_context.oozie_server

    def get_resource_manager_uri(self, cluster):
        return self.cluster_context.resource_manager_uri

    def _get_cluster_context(self, cluster):
        h_version = cluster.hadoop_version
        v_handler = vhf.VersionHandlerFactory.get().get_handler(h_version)
        return v_handler.get_context(cluster)
