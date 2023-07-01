#!/bin/bash
#
# This is a useful test to run occasionally, to see which syscalls are
# causing trinity to segfault.

. scripts/paths.sh
. scripts/privs.sh
. scripts/taint.sh

DESTINATION=kataworker@192.168.122.109
PASSWORD=1234
XLIST=()

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
        for i in ${array[@]}
        do
                if[$syscall != $i]
                then
                        sshpass -p $PASSWORD ssh -t $DESTINATION "echo > /sys/kernel/debug/tracing/trace; echo 1 > /sys/kernel/debug/tracing/tracing_on"
                        MALLOC_CHECK_=2 $TRINITY_PATH/trinity -a 64 -c $syscall -C 1 -N 1000 $DROPPRIVS
                        sshpass -p $PASSWORD ssh -t $DESTINATION "echo 0 > /sys/kernel/debug/tracing/tracing_on; cat /sys/kernel/debug/tracing/trace | grep pool > /home/kataworker/ftraceresult/${syscall}.txt;"
                        sshpass -p $PASSWORD scp /program/${syscall}.txt $DESTINATION:/home/kataworker/trinityresult            
                fi
        done

        chmod 755 $TRINITY_TMP
        popd

        check_tainted
        echo
        echo
done
check_tainted
done
