#########
# Copyright (c) 2015 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#  * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  * See the License for the specific language governing permissions and
#  * limitations under the License.

import os
import unittest

from mock import patch

import cloudify_agent.shell.env as env_constants
from cloudify_agent.api import utils
from cloudify_agent.shell.main import get_logger
from cloudify_agent.tests.shell.commands import BaseCommandLineTestCase
from cloudify_agent.tests import get_storage_directory


@patch('cloudify_agent.api.utils.internal.get_storage_directory',
       get_storage_directory)
@patch('cloudify_agent.shell.commands.daemons.DaemonFactory.new')
@patch('cloudify_agent.shell.commands.daemons.DaemonFactory.save')
@patch('cloudify_agent.shell.commands.daemons.DaemonFactory.load')
@patch('cloudify_agent.shell.commands.daemons.DaemonFactory.delete')
@patch('cloudify_agent.shell.commands.daemons.DaemonFactory.load_all')
class TestPatchedDaemonCommandLine(BaseCommandLineTestCase, unittest.TestCase):

    PROCESS_MANAGEMENT = 'init.d'

    def test_create(self, *factory_methods):
        self._run('cfy-agent daemons create --name=name '
                  '--process-management=init.d --user=user '
                  '--queue=queue  --rest-host=127.0.0.1')

        factory_new = factory_methods[4]
        factory_new.assert_called_once_with(
            name='name',
            queue='queue',
            user='user',
            rest_host='127.0.0.1',
            process_management='init.d',
            broker_ip=None,
            workdir=None,
            log_level=None,
            pid_file=None,
            log_dir=None,
            max_workers=None,
            min_workers=None,
            rest_port='80',
            host=None,
            deployment_id=None,
            extra_env_path=None,
            logger=get_logger(),
            broker_user='guest',
            broker_pass='guest',
            broker_vhost='/',
            broker_ssl_cert=None,
            broker_ssl_enabled=False,
            heartbeat=30,
            rest_username=None,
            rest_password=None,
            rest_token=None,
            rest_tenant=None,
            broker_ssl_cert_path=os.environ[
                env_constants.CLOUDIFY_BROKER_SSL_CERT_PATH],
            local_rest_cert_file=os.environ[
                env_constants.CLOUDIFY_LOCAL_REST_CERT_PATH],
            bypass_maintenance_mode=None,
            network=None,
            cluster=None
        )

        daemon = factory_new.return_value
        daemon.create.assert_called_once_with()

    def test_create_with_custom_options(self, *factory_methods):

        self._run('cfy-agent daemons create --name=name --queue=queue '
                  '--rest-host=127.0.0.1 --broker-ip=127.0.0.1 --user=user '
                  '--process-management=init.d --rest-tenant=tenant '
                  '--key=value --complex-key=complex-value')

        factory_new = factory_methods[4]
        factory_new.assert_called_once_with(
            name='name',
            queue='queue',
            user='user',
            rest_host='127.0.0.1',
            process_management='init.d',
            broker_ip='127.0.0.1',
            workdir=None,
            max_workers=None,
            min_workers=None,
            host=None,
            deployment_id=None,
            log_level=None,
            pid_file=None,
            log_dir=None,
            rest_port='80',
            extra_env_path=None,
            logger=get_logger(),
            key='value',
            complex_key='complex-value',
            broker_user='guest',
            broker_pass='guest',
            broker_vhost='/',
            broker_ssl_cert=None,
            broker_ssl_enabled=False,
            heartbeat=30,
            broker_ssl_cert_path=os.environ[
                env_constants.CLOUDIFY_BROKER_SSL_CERT_PATH],
            rest_username=None,
            rest_password=None,
            rest_token=None,
            rest_tenant='tenant',
            local_rest_cert_file=os.environ[
                env_constants.CLOUDIFY_LOCAL_REST_CERT_PATH],
            bypass_maintenance_mode=None,
            network=None,
            cluster=None
        )

    def test_configure(self, *factory_methods):
        self._run('cfy-agent daemons configure --name=name ')

        factory_load = factory_methods[2]
        factory_load.assert_called_once_with('name',
                                             logger=get_logger())

        daemon = factory_load.return_value
        daemon.configure.assert_called_once_with()

        factory_save = factory_methods[3]
        factory_save.assert_called_once_with(daemon)

    def test_start(self, *factory_methods):
        self._run('cfy-agent daemons start --name=name '
                  '--interval 5 --timeout 20 --no-delete-amqp-queue')

        factory_load = factory_methods[2]
        factory_load.assert_called_once_with('name',
                                             logger=get_logger())

        daemon = factory_load.return_value
        daemon.start.assert_called_once_with(
            interval=5,
            timeout=20,
            delete_amqp_queue=True,
        )

    def test_stop(self, *factory_methods):
        self._run('cfy-agent daemons stop --name=name '
                  '--interval 5 --timeout 20')

        factory_load = factory_methods[2]
        factory_load.assert_called_once_with('name',
                                             logger=get_logger())

        daemon = factory_load.return_value
        daemon.stop.assert_called_once_with(
            interval=5,
            timeout=20
        )

    def test_delete(self, *factory_methods):
        self._run('cfy-agent daemons delete --name=name')

        factory_load = factory_methods[2]
        factory_load.assert_called_once_with('name',
                                             logger=get_logger())

        daemon = factory_load.return_value
        daemon.delete.assert_called_once_with()

    def test_restart(self, *factory_methods):
        self._run('cfy-agent daemons restart --name=name')

        factory_load = factory_methods[2]
        factory_load.assert_called_once_with('name',
                                             logger=get_logger())

        daemon = factory_load.return_value
        daemon.restart.assert_called_once_with()

    @patch('cloudify_agent.shell.commands.daemons.api_utils'
           '.internal.daemon_to_dict')
    def test_inspect(self, daemon_to_dict, *factory_methods):

        daemon_to_dict.return_value = {}

        name = utils.internal.generate_agent_name()
        self._run('cfy-agent daemons inspect --name={0}'.format(name))

        factory_load = factory_methods[2]
        factory_load.assert_called_once_with(name, logger=get_logger())
        daemon = factory_load.return_value

        daemon_to_dict.assert_called_once_with(daemon)

    def test_status(self, *factory_methods):
        name = utils.internal.generate_agent_name()
        self._run('cfy-agent daemons status --name={0}'.format(name))
        factory_load = factory_methods[2]
        daemon = factory_load.return_value
        daemon.status.assert_called_once_with()

    def test_required(self, *_):
        self._run('cfy-agent daemons create --rest-host=manager '
                  '--broker-ip=manager '
                  '--process-management=init.d', raise_system_exit=True)


@patch('cloudify_agent.api.utils.internal.get_storage_directory',
       get_storage_directory)
class TestDaemonCommandLine(BaseCommandLineTestCase, unittest.TestCase):

    def test_inspect_non_existing_agent(self):
        try:
            self._run('cfy-agent daemons inspect --name=non-existing',
                      raise_system_exit=True)
        except SystemExit as e:
            self.assertEqual(e.code, 203)

    def test_list(self):
        self._run('cfy-agent daemons create '
                  '--process-management=init.d '
                  '--queue=queue --name=test-name --rest-host=127.0.0.1 '
                  '--broker-ip=127.0.0.1 --user=user ')
        self._run('cfy-agent daemons create '
                  '--process-management=init.d '
                  '--queue=queue --name=test-name2 --rest-host=127.0.0.1 '
                  '--broker-ip=127.0.0.1 --user=user ')
        self._run('cfy-agent daemons list')
