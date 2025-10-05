#!/bin/bash

usage="Syntax: $(basename "$0") [-h|--help] [COMPONENTS...] -- will set up the project environment,

where:
    -h | --help     Print this help
    COMPONENTS...   Specify component to set up

Valid COMPONENTS:
    all: set up all components (container will be pulled, not built)
    cont_[pull|build]: pull the singularity container or build it
    data: pull data"

if [[ $# -eq 0 ]] || [[ "$@" =~ "--help" ]] || [[ "$@" =~ "-h" ]];then
    echo "$usage"
    exit 0
fi

CONT_NAME="psiturk.sif"

# container setup
if [[ "$1" =~ "cont_pull" ]] || [[ "$1" =~ "all" ]];then
    echo_blue "Pulling singularity container..."
    wget --no-check-certificate "https://yaleedu-my.sharepoint.com/:u:/g/personal/aalap_shah_yale_edu/ETzZVxrXDUdIowJYnXZ2FrEBos3uQJ5xIsJByNvt5FW2tQ?e=M1vhRu&download=1" -O "$CONT_NAME"
elif [[ "$1" =~ "cont_build" ]];then
    echo_blue "Building apptainer container..."
    remove "${ENV[cont_main]}"
    sudo -E apptainer build "${ENV[cont_main]}" "${ENV[cont_def]}"
else
    echo_green "Not touching container"
fi


# download stimulus set
if [[ "$@" =~ "data" ]] || [[ "$@" =~ "all" ]];then
    echo "Pulling data..."
    wget "https://yaleedu-my.sharepoint.com/:u:/g/personal/aalap_shah_yale_edu/EXNoP4NxxsBKvtbfYteBH2MBeAoE5UyOQUP1J5Hn1Un-hg?e=wiV5OL&download=1" -O "stimuli_videos.zip"
    chmod +777 stimuli_videos.zip
    unzip stimuli_videos.zip
    mv stimuli_videos/* psiturk/static/stimuli_videos/
    rm -rf stimuli_videos
    rm -rf stimuli_videos.zip
else
    echo "Not pulling any data"
fi

