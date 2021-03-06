# Copyright (c) 2016 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from oslo_serialization import jsonutils as json

from sahara.plugins import utils
from sahara_plugins.tests.unit import base
from sahara_plugins.tests.unit.plugins.cdh import utils as ctu


json_files = [
    'hdfs-service.json',
    'hdfs-namenode.json',
    'hdfs-datanode.json',
    'hdfs-secondarynamenode.json',
    'hdfs-gateway.json',
    'hdfs-journalnode.json',
    'yarn-service.json',
    'yarn-resourcemanager.json',
    'yarn-nodemanager.json',
    'yarn-jobhistory.json',
    'yarn-gateway.json',
    'oozie-service.json',
    'oozie-oozie_server.json',
    'hive-service.json',
    'hive-hivemetastore.json',
    'hive-hiveserver2.json',
    'hive-webhcat.json',
    'hue-service.json',
    'hue-hue_server.json',
    'spark-service.json',
    'spark-spark_yarn_history_server.json',
    'zookeeper-service.json',
    'zookeeper-server.json',
    'hbase-service.json',
    'hbase-master.json',
    'hbase-regionserver.json',
    'flume-service.json',
    'flume-agent.json',
    'sentry-service.json',
    'sentry-sentry_server.json',
    'solr-service.json',
    'solr-solr_server.json',
    'sqoop-service.json',
    'sqoop-sqoop_server.json',
    'ks_indexer-service.json',
    'ks_indexer-hbase_indexer.json',
    'impala-service.json',
    'impala-catalogserver.json',
    'impala-impalad.json',
    'impala-statestore.json',
    'kms-service.json',
    'kms-kms.json',
    'kafka-kafka_broker.json',
    'kafka-kafka_mirror_maker.json',
    'kafka-service.json'
]


class TestConfigHelper(base.SaharaTestCase):

    def setUp(self):
        super(TestConfigHelper, self).setUp()
        self.path_to_config = None
        self.c_h = None

    def test_get_ng_plugin_configs(self):
        actual_configs = self.c_h._get_ng_plugin_configs()

        expected_configs = []
        for json_file in json_files:
            expected_configs += json.loads(
                utils.get_file_text(self.path_to_config + json_file,
                                    'sahara_plugins'))

        # compare names
        expected_names = set(i['name'] for i in expected_configs)
        actual_names = set(i.to_dict()['name'] for i in actual_configs)
        self.assertEqual(expected_names, actual_names)

    def test_get_cdh5_repo_url(self):
        cluster = ctu.get_fake_cluster(cluster_configs={})
        self.assertEqual(self.c_h.CDH5_REPO_URL.default_value,
                         self.c_h.get_cdh5_repo_url(cluster))

        cluster = ctu.get_fake_cluster(
            cluster_configs={
                'general': {self.c_h.CDH5_REPO_URL.name: 'spam'}})
        self.assertEqual('spam', self.c_h.get_cdh5_repo_url(cluster))

    def test_get_cdh5_key_url(self):
        cluster = ctu.get_fake_cluster(cluster_configs={})
        self.assertEqual(self.c_h.CDH5_REPO_KEY_URL.default_value,
                         self.c_h.get_cdh5_key_url(cluster))

        cluster = ctu.get_fake_cluster(
            cluster_configs={
                'general': {self.c_h.CDH5_REPO_KEY_URL.name: 'spam'}})
        self.assertEqual('spam', self.c_h.get_cdh5_key_url(cluster))

    def test_get_cm5_repo_url(self):
        cluster = ctu.get_fake_cluster(cluster_configs={})
        self.assertEqual(self.c_h.CM5_REPO_URL.default_value,
                         self.c_h.get_cm5_repo_url(cluster))

        cluster = ctu.get_fake_cluster(
            cluster_configs={
                'general': {self.c_h.CM5_REPO_URL.name: 'spam'}})
        self.assertEqual('spam', self.c_h.get_cm5_repo_url(cluster))

    def test_get_cm5_key_url(self):
        cluster = ctu.get_fake_cluster(cluster_configs={})
        self.assertEqual(self.c_h.CM5_REPO_KEY_URL.default_value,
                         self.c_h.get_cm5_key_url(cluster))

        cluster = ctu.get_fake_cluster(
            cluster_configs={
                'general': {self.c_h.CM5_REPO_KEY_URL.name: 'spam'}})
        self.assertEqual('spam', self.c_h.get_cm5_key_url(cluster))

    def test_is_swift_enabled(self):
        cluster = ctu.get_fake_cluster(cluster_configs={})
        self.assertTrue(self.c_h.is_swift_enabled(cluster))

        cluster = ctu.get_fake_cluster(
            cluster_configs={
                'general': {self.c_h.ENABLE_SWIFT.name: False}})
        self.assertFalse(self.c_h.is_swift_enabled(cluster))

    def test_get_swift_lib_url(self):
        cluster = ctu.get_fake_cluster(cluster_configs={})
        self.assertEqual(self.c_h.DEFAULT_SWIFT_LIB_URL,
                         self.c_h.get_swift_lib_url(cluster))

        cluster = ctu.get_fake_cluster(
            cluster_configs={
                'general': {self.c_h.SWIFT_LIB_URL.name: 'spam'}})
        self.assertEqual('spam', self.c_h.get_swift_lib_url(cluster))

    def test_is_hbase_common_lib_enabled(self):
        cluster = ctu.get_fake_cluster(cluster_configs={})
        self.assertTrue(self.c_h.is_hbase_common_lib_enabled(cluster))

        cluster = ctu.get_fake_cluster(
            cluster_configs={
                'general': {self.c_h.ENABLE_HBASE_COMMON_LIB.name: False}})
        self.assertFalse(self.c_h.is_hbase_common_lib_enabled(cluster))

    def test_get_extjs_lib_url(self):
        cluster = ctu.get_fake_cluster(cluster_configs={})
        self.assertEqual(self.c_h.DEFAULT_EXTJS_LIB_URL,
                         self.c_h.get_extjs_lib_url(cluster))

        cluster = ctu.get_fake_cluster(
            cluster_configs={
                'general': {self.c_h.EXTJS_LIB_URL.name: 'spam'}})
        self.assertEqual('spam', self.c_h.get_extjs_lib_url(cluster))

    def test_get_kms_key_url(self):
        cluster = ctu.get_fake_cluster(cluster_configs={})
        self.assertEqual(self.c_h.KMS_REPO_KEY_URL.default_value,
                         self.c_h.get_kms_key_url(cluster))

        cluster = ctu.get_fake_cluster(
            cluster_configs={
                'general': {self.c_h.KMS_REPO_KEY_URL.name: 'spam'}})
        self.assertEqual('spam', self.c_h.get_kms_key_url(cluster))

    def test_get_required_anti_affinity(self):
        cluster = ctu.get_fake_cluster(cluster_configs={})
        self.assertTrue(self.c_h.get_required_anti_affinity(cluster))

        cluster = ctu.get_fake_cluster(
            cluster_configs={
                'general': {self.c_h.REQUIRE_ANTI_AFFINITY.name: False}})
        self.assertFalse(self.c_h.get_required_anti_affinity(cluster))
