from litestar.config.cors import CORSConfig

from hack_template.presentors.rest.config import RestConfig


def get_cors_config(config: RestConfig) -> CORSConfig:
    return CORSConfig(allow_origins=["*"])
