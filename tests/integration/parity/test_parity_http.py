import os
import pytest
import random

from tests.integration.parity.utils import (
    wait_for_http,
)
from web3 import Web3
from web3.utils.module_testing import (
    NetModuleTest,
    VersionModuleTest,
)

from .common import (
    ParityEthModuleTest,
    ParityPersonalModuleTest,
    ParityWeb3ModuleTest,
)


@pytest.fixture(scope="module")
def rpc_port():
    return random.choice(range(8000, 9000))


@pytest.fixture(scope="module")
def endpoint_uri(rpc_port):
    return 'http://localhost:{}'.format(rpc_port)


@pytest.fixture(scope="module")
def parity_command_arguments(
    parity_import_blocks_process,
    parity_binary,
    datadir,
    passwordfile,
    author,
    rpc_port
):
    return (
        parity_binary,
        '--chain', os.path.join(datadir, 'chain_config.json'),
        '--base-path', datadir,
        '--unlock', author,
        '--password', passwordfile,
        '--jsonrpc-port', str(rpc_port),
        '--no-ipc',
        '--no-ws',
    )


@pytest.fixture(scope="module")
def parity_import_blocks_command(parity_binary, rpc_port, datadir, passwordfile):
    return (
        parity_binary,
        'import', os.path.join(datadir, 'blocks_export.rlp'),
        '--chain', os.path.join(datadir, 'chain_config.json'),
        '--base-path', datadir,
        '--password', passwordfile,
        '--jsonrpc-port', str(rpc_port),
        '--no-ipc',
        '--no-ws',
    )


@pytest.fixture(scope="module")  # noqa: F811
def web3(parity_process, endpoint_uri):
    wait_for_http(endpoint_uri)
    _web3 = Web3(Web3.HTTPProvider(endpoint_uri))
    return _web3


class TestParityWeb3ModuleTest(ParityWeb3ModuleTest):
    pass


class TestParityEthModuleTest(ParityEthModuleTest):
    pass


class TestParityVersionModule(VersionModuleTest):
    pass


class TestParityNetModule(NetModuleTest):
    pass


class TestParityPersonalModuleTest(ParityPersonalModuleTest):
    pass