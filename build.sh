#!/usr/bin/env bash

CONTAINER_IMAGE="sd2e/xplan_to_sbol:1.0"

docker build -t ${CONTAINER_IMAGE} .