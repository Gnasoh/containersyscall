#!/bin/bash
#
# This is a useful test to run occasionally, to see which syscalls are
# causing trinity to segfault.

. scripts/paths.sh
. scripts/privs.sh
. scripts/taint.sh

DESTINATION=kataworker@192.168.122.109

while [ 1 ]
do
for syscall in $($TRINITY_PATH/trinity -L | grep entrypoint | grep -v AVOID | awk '{ print $3 }' | sort -u)
do
        pushd $TRINITY_TMP

        if [ ! -f $TRINITY_PATH/trinity ]; then
                echo lost!
                pwd
                exit
        fi
        ssh $DESTINATION "echo 1 > /sys/kernel/debug/tracing/tracing_on"
        MALLOC_CHECK_=2 $TRINITY_PATH/trinity -q -c $syscall -N 1000 -l off -C 1 $DROPPRIVS -x execve
        ssh $DESTINATION "echo 0 > /sys/kernel/debug/tracing/tracing_on"

        chmod 755 $TRINITY_TMP
        popd

        check_tainted
        echo
        echo
done
check_tainted
done