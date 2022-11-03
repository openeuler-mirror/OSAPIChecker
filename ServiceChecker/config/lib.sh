#!/bin/echo

function log_info()
{
    echo -e "[`date +%Y-%m-%d\ %T`]  INFO: $@"
}

function log_warn()
{
    echo -e "\033[33m"[`date +%Y-%m-%d\ %T`]  WARNING: $@" \033[0m"
}

function log_error()
{
    echo -e "\033[31m"[`date +%Y-%m-%d\ %T`]  ERROR: $@" \033[0m"
    exit 1
}

function log_debug()
{
    [ "$DEBUG" == "yes" ] && echo "[`date +%Y-%m-%d\ %T`]  DEBUG: $@"
    echo -n ""
}