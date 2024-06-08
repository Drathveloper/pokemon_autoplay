import common


if __name__ == "__main__":
    workspace = common.get_workspace_dir()
    common.run_managed_sd(workspace)
    print('showdown instance started successfully')
    exit(0)
