#!/bin/sh

BINPATH=`dirname $0`
cd $BINPATH/..

WORKERS=1
HOST='0.0.0.0:3000'
APP='app'

if [ ! -z ${GUNICORN_WORKERS} ]; then WORKERS=${GUNICORN_WORKERS}; fi

if [ "$1" = "--reload" ]
then
    echo "--reload option enabled"
    gunicorn -w ${WORKERS} -b ${HOST} -t ${GUNICORN_WORKER_TIMEOUT} ${APP} --reload
else
    gunicorn -w ${WORKERS} -b ${HOST} -t ${GUNICORN_WORKER_TIMEOUT} ${APP}
fi
