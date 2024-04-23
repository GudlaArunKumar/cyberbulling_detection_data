from cybulldetection.utils.utils import run_shell_command, get_logger
from pathlib import Path
from subprocess import CalledProcessError

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


def initialize_dvc_storage(dvc_remote_name: str, dvc_remote_url: str) -> None:
    if not run_shell_command("dvc remote list"):
        DATA_UTILS_LOGGER.info("Initializing DVC storage...")
        run_shell_command(f"dvc remote add -d {dvc_remote_name} {dvc_remote_url}")
        run_shell_command("git add .dvc/config")
        run_shell_command(f"git commit -nm 'Configured remote storage at: {dvc_remote_url}'")
    else:
        DATA_UTILS_LOGGER.info("DVC storage is already initialized...")


def commit_to_dvc(dvc_raw_folder_data: str, dvc_remote_name: str) -> None:
    """
    function to update the verison of data in dvc and also in git
    """

    current_version = run_shell_command("git tag --list | sort -t v -k 2 -g | tail -1 | sed 's/v//'").strip()
    if not current_version: # if there is no version of the data
        current_version = "0"
    next_version = f"v{int(current_version)+1}"
    run_shell_command(f"dvc add {dvc_raw_folder_data}")
    run_shell_command("git add .")
    run_shell_command(f"git commit -nm 'Updated version of the data from v{current_version} to {next_version}'")
    run_shell_command(f"git tag -a {next_version} -m 'Data version {next_version}'")
    run_shell_command(f"dvc push {dvc_raw_folder_data}.dvc --remote {dvc_remote_name}")
    run_shell_command("git push --follow-tags")
    run_shell_command("git push -f --tags")



def make_new_data_version(dvc_raw_folder_data: str, dvc_remote_name: str) -> None:
    """
    function to check if there is any new update to the data and update it's version
    """

    try: # try block is used for the first time commit when dvc status is called
        status = run_shell_command(f"dvc status {dvc_raw_folder_data}.dvc")
        if status == "Data and pipelines are up to date.\n":
            DATA_UTILS_LOGGER.info("Data and pipelines are up to date.")
            return
        commit_to_dvc(dvc_raw_folder_data, dvc_remote_name)
    except CalledProcessError:
        commit_to_dvc(dvc_raw_folder_data, dvc_remote_name)
