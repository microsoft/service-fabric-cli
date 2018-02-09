#!/bin/bash

# Basic script used by Travis and local to verify all tests

function launch_pylint()
{
    $(which pylint) $1 --msg-template='{path}({line}): [{msg_id}{obj}] {msg}' --load-plugins=checkers
}

function launch_unit_tests()
{
    nosetests -v --with-coverage --cover-package=sfctl --cover-inclusive
}

if [[ $1 == "local" ]]
    then
        launch_unit_tests && launch_pylint ./src/sfctl && launch_pylint ./src/checkers
elif [[ $1 == "test" ]]
    then
        launch_unit_tests
elif [[ $1 == "lint" ]]
    then
        echo "Linting CLI..."
        launch_pylint ./src/sfctl
        r1=$?
        echo "Linting Checker..."
        launch_pylint ./src/checkers
        r2=$?
        echo $((r1 + r2))
fi

# On windows, uncomment out the following line to prevent the popup window from closing
$SHELL
