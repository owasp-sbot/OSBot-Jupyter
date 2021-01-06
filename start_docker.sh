#!/usr/bin/env bash

docker run -it --rm -p 8888:8888                                \
    -v `pwd`/osbot_jupyter:/home/jovyan/osbot_jupyter           \
    -v `pwd`/notebooks:/home/jovyan/local                       \
    -v "$HOME/.aws":/home/jovyan/.aws                           \
    311800962295.dkr.ecr.eu-west-1.amazonaws.com/osbot-jupyter  \
    jupyter notebook --allow-root --debug
