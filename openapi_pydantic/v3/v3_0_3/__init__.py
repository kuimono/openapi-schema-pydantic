"""
OpenAPI v3.0.3 schema types, created according to the specification:
https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md

The type orders are according to the contents of the specification:
https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#table-of-contents
"""

from .open_api import OpenAPI as OpenAPI
from .info import Info as Info
from .contact import Contact as Contact
from .license import License as License
from .server import Server as Server
from .server_variable import ServerVariable as ServerVariable
from .components import Components as Components
from .paths import Paths as Paths
from .path_item import PathItem as PathItem
from .operation import Operation as Operation
from .external_documentation import ExternalDocumentation as ExternalDocumentation
from .parameter import Parameter as Parameter, ParameterLocation as ParameterLocation
from .request_body import RequestBody as RequestBody
from .media_type import MediaType as MediaType
from .encoding import Encoding as Encoding
from .responses import Responses as Responses
from .response import Response as Response
from .callback import Callback as Callback
from .example import Example as Example
from .link import Link as Link
from .header import Header as Header
from .tag import Tag as Tag
from .reference import Reference as Reference
from .schema import Schema as Schema
from .discriminator import Discriminator as Discriminator
from .xml import XML as XML
from .security_scheme import SecurityScheme as SecurityScheme
from .oauth_flows import OAuthFlows as OAuthFlows
from .oauth_flow import OAuthFlow as OAuthFlow
from .security_requirement import SecurityRequirement as SecurityRequirement


# resolve forward references
Encoding.update_forward_refs(Header=Header)
Schema.update_forward_refs()
