from typing import ContextManager
import pytest
from contextlib import nullcontext as does_not_raise
from pydantic import Extra, ValidationError

from openapi_schema_pydantic import OpenAPI, Operation, PathItem, Info
from openapi_schema_pydantic.v3.v3_1_0._config import DefaultConfig


@pytest.mark.parametrize(
    "cm,extra",
    [
        (pytest.raises(AttributeError), Extra.ignore),
        (pytest.raises(ValidationError), Extra.forbid),
        (does_not_raise(), Extra.allow),
    ],
)
def test_dumb_key(
    monkeypatch: pytest.MonkeyPatch,
    cm: ContextManager,
    extra: Extra,
):
    with monkeypatch.context() as m:
        m.setattr(DefaultConfig, "extra", extra)
        with cm:
            api = OpenAPI(
                info=Info(
                    title="dumb test",
                    version="3",
                ),
                dumb="DUMB",
            )
            assert api.dumb == "DUMB"

@pytest.mark.parametrize(
    "cm,extra",
    [
        (pytest.raises(AttributeError), Extra.ignore),
        (pytest.raises(ValidationError), Extra.forbid),
        (does_not_raise(), Extra.allow),
    ],
)
def test_dumb_key_manual_assignment_of_config_value(
    monkeypatch: pytest.MonkeyPatch,
    cm: ContextManager,
    extra: Extra,
):
    with monkeypatch.context() as m:
        DefaultConfig.extra = extra
        #m.setattr(DefaultConfig, "extra", extra)
        with cm:
            api = OpenAPI(
                info=Info(
                    title="dumb test",
                    version="3",
                ),
                dumb="DUMB",
            )
            assert api.dumb == "DUMB"
