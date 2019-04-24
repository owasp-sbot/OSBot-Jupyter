#!/usr/bin/env bash

docker run -it -p 8888:8888                                     \
    -v `pwd`/osbot_jupyter:/home/jovyan/osbot_jupyter           \
    -v `pwd`/notebooks:/home/jovyan/                            \
    244560807427.dkr.ecr.eu-west-2.amazonaws.com/osbot-jupyter  \
    jupyter notebook --allow-root
