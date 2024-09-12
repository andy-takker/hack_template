from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.plugins import (
    RapidocRenderPlugin,
    ScalarRenderPlugin,
)

from hack_template.presentors.rest.config import RestConfig


def get_openapi_config(config: RestConfig) -> OpenAPIConfig:
    return OpenAPIConfig(
        title=config.app.title,
        description=config.app.description,
        version=config.app.version,
        path="/docs",
        render_plugins=[
            RapidocRenderPlugin(),
            ScalarRenderPlugin(),
        ],
    )
