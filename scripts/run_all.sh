#!/bin/bash
set -e

make up
make backend
make frontend
make ai
make pipeline 