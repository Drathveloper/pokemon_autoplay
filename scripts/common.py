import os
import shutil
import subprocess
import sys

workspace_env_key = 'POKEMON_WORKSPACE'

default_workspace = os.environ['WORKSPACE_ENV']


def setup_dir(ws):
    if not os.path.isdir(ws):
        os.mkdir(ws)


def setup_sd(ws):
    sd_dir = ws + '/pokemon-showdown'
    if not os.path.isdir(sd_dir) or not os.path.isdir(sd_dir + '/.git'):
        p = subprocess.Popen([
            '/usr/bin/git',
            'clone',
            'https://github.com/smogon/pokemon-showdown',
            ws + '/pokemon-showdown'])
        p.wait()
        shutil.copy(sd_dir + '/config/config-example.js', sd_dir + '/config/config.js')
        with open(sd_dir + '/Dockerfile', "w") as dockerfile:
            dockerfile.write("""
            FROM node:latest
            RUN mkdir -p /opt/app/node_modules && chown -R node:node /opt/app
            WORKDIR /opt/app
            COPY ./ ./
            USER node
            COPY --chown=node:node . .
            EXPOSE 8000
            CMD ["node", "pokemon-showdown", "start", "--no-security"]
            """)


def run_managed_sd(ws):
    p = _run_sd(ws)
    p.wait()


def run_unmanaged_sd(ws):
    _run_sd(ws)


def _run_sd(ws):
    sd_dir = ws + '/pokemon-showdown'
    if not os.path.isdir(sd_dir) or not os.path.isdir(sd_dir + '/.git'):
        setup_sd(ws)
    p = subprocess.Popen([sd_dir + '/pokemon-showdown start --no-security'], shell=True)
    return p


def get_workspace_dir():
    if len(sys.argv) >= 2:
        return sys.argv[1]
    workspace = os.getenv(workspace_env_key)
    if workspace is not None and workspace != "":
        return workspace
    return default_workspace
