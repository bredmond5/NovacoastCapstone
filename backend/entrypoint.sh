#!/bin/bash

flask db upgrade \
    && "$@"