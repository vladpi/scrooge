"""
Use this module to register required services.
Services registered inside a `rodi.Container` are automatically injected into request
handlers.

For more information and documentation, see `rodi` Wiki and examples:
    https://github.com/Neoteroi/rodi/wiki
    https://github.com/Neoteroi/rodi/tree/main/examples
"""
from typing import Tuple

from rodi import Container

from app.settings import Settings
from data.sql.services import register_sql_services
from domain.services import register_services


def configure_services(
    settings: Settings,
) -> Tuple[Container, Settings]:
    container = Container()

    container.add_instance(settings)

    register_sql_services(container)
    register_services(container)

    return container, settings
