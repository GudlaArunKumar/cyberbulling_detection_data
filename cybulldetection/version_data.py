
from cybulldetection.config_schemas.config_schema import Config 
from cybulldetection.utils.config_utils import get_config
from cybulldetection.utils.data_utils import initialize_dvc
from cybulldetection.utils.utils import get_logger


@get_config(config_path="../configs", config_name="config")
def version_data(config: Config) -> None:

    initialize_dvc()


if __name__ == "__main__":
    version_data()