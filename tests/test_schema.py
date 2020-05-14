from openapi_schema_pydantic import (
    OpenAPI,
    Info,
    Contact,
    License,
    Server,
)

def test_open_api():
    open_api = OpenAPI()
    assert open_api is not None

def test_info():
    info_dict = Info.Config.schema_extra['examples'][0]
    info = Info(**info_dict)
    assert info is not None

def test_contact():
    contact_dict = Contact.Config.schema_extra['examples'][0]
    contact = Contact(**contact_dict)
    assert contact is not None

def test_license():
    license_dict = License.Config.schema_extra['examples'][0]
    license = License(**license_dict)
    assert license is not None

def test_server():
    server_dict = Server.Config.schema_extra['examples'][1]
    server = Server(**server_dict)
    assert server is not None