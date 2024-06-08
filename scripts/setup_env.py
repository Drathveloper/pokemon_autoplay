import common


if __name__ == "__main__":
    workspace = common.get_workspace_dir()
    common.setup_dir(workspace)
    common.setup_sd(workspace)
    print('environment setup successfully')
    exit(0)
