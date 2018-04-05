#!/bin/bash

# Basic script used by Travis and local to verify all tests

function launch_pylint()
{
    $(which pylint) $1 --msg-template='{path}({line}): [{msg_id}{obj}] {msg}' --load-plugins=checkers
}

function launch_unit_tests()
{
    nose2 -v --with-coverage --coverage sfctl
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
        exit $((r1 + r2))
fi
