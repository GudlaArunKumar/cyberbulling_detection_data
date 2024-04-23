# this is the important file where config store is instantiated

from hydra.core.config_store import ConfigStore 
from pydantic.dataclasses import dataclass 


@dataclass
class Config:
    dvc_remote_name: str = "gcs-storage"
    dvc_remote_url: str = "gs://cybull_detection/data/raw"
    dvc_raw_folder_data: str = "./data/raw"


def setup_config() -> None:
    cs = ConfigStore.instance()
    cs.store(name="config_schema", node=Config)