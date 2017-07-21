#!/bin/bash

# Basic script used by Travis and local to verify all tests

function launch_pylint()
{
    $(which pylint) $1 --msg-template='{path}({line}): [{msg_id}{obj}] {msg}' --load-plugins=checkers
}

function launch_unit_tests()
{
    nosetests -v --with-coverage --cover-package=sfcli --cover-inclusive
}

if [[ $1 == "local" ]]
    then
        launch_unit_tests && launch_pylint ./src/sfcli && launch_pylint ./src/checkers
elif [[ $1 == "test" ]]
    then
        launch_unit_tests
elif [[ $PYLINT_TARGET ]]
    then
        launch_pylint $PYLINT_TARGET
fi
