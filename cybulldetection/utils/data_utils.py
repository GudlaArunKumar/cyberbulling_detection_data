from cybulldetection.utils.utils import run_shell_command, get_logger
from pathlib import Path


DATA_UTILS_LOGGER = get_logger(Path(__file__).name)

def is_dvc_initialized() -> bool:
    # to check whether current working directory has .dvc file or not  
    return (Path().cwd() / ".dvc").exists()



def initialize_dvc() -> None:
    if is_dvc_initialized():
        DATA_UTILS_LOGGER.info("DVC is already initialized")
        return 
    
    DATA_UTILS_LOGGER.info("Initialized DVC")
    run_shell_command("dvc init")
    run_shell_command("dvc config core.analytics false")
    run_shell_command("dvc config core.autostage true")
    run_shell_command("git add .dvc") # to add dvc tracking file to the git
    run_shell_command("git commit -nm 'Initialized DVC'")
