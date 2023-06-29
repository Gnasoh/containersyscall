#!/bin/bash

echo > /sys/kernel/debug/tracing/trace

echo 1 > /sys/kernel/debug/tracing/tracing_on