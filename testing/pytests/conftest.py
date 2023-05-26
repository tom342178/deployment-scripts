import pytest
import support

<<<<<<< HEAD
=======
# my_params = {
#     "conn": "178.79.143.174:32349",
#     "auth": (),
#     "timeout": 30,
#     "destination": "network"
# }

>>>>>>> 092473e91cf7a7f8cfcc7fb5f108be000a111fc7

def pytest_addoption(parser):
    """
    Pytest additional arguments
    :custom options:
        --conn           REST connection information (ex. ${USER}:${PASSWORD]@${IP}:${PORT})
        --timeout       REST timeout
        --destination   node(s) to query against
    """
    parser.addoption("--conn", type=support.validate_conn_pattern, action="store", default=None,
                     help="REST connection information (ex. ${USER}:${PASSWORD]@${IP}:${PORT})")
    parser.addoption("--timeout", type=int, action="store", default=30, help="REST timeout")
    parser.addoption("--destination", type=str, action="store", default='network', help="node(s) to query against")


@pytest.fixture(autouse=True)
def pass_parameters(request):
    if request.config.getoption('--conn') is None:
        pytest.exit("Missing REST connection information")
    setattr(request.cls, "conn", request.config.getoption('--conn'))
    setattr(request.cls, "auth", ())
    if '@' in request.config.getoption('--conn'):
        setattr(request.cls, "conn", request.config.getoption('--conn').split('@')[-1])
        setattr(request.cls, "auth", tuple(request.config.getoption('--conn').split('@')[0].split(':')))
    setattr(request.cls, "timeout", request.config.getoption('--timeout'))
    setattr(request.cls, "destination", request.config.getoption('--destination'))


