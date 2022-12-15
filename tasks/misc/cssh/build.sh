#!/bin/bash

TASK_DIRS=$(ls | grep -v cssh | grep -v build.sh)

for task_dir in $TASK_DIRS; do
  for dir in $(ls $task_dir | grep stage); do
    cd "$task_dir/$dir"
    task_n=$(echo $dir | sed 's/stage//g')
    task_name="$task_dir$task_n"
    echo "$task_name"
    docker build -t $task_name .
    cd -
  done
done
