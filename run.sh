#!/usr/bin/env bash

owner=$1
repo=$2

poetry run python src/main.py $owner $repo