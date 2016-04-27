#!/bin/bash
cd /web/storm/project
source ../env/bin/activate
/web/storm/env/bin/gunicorn application:app