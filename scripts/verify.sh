#!/bin/bash

# Basic script used by Travis and local to verify all tests

function launch_pylint()
{
    $(which pylint) $1 --msg-template='{path}({line}): [{msg_id}{obj}] {msg}' --load-plugins=checkers
}

function launch_unit_tests()
{
<<<<<<< HEAD
    nosetests -v --with-coverage --cover-package=sfctl --cover-inclusive
=======
    nosetests -v --with-coverage --cover-package=sfcli --cover-inclusive
>>>>>>> master
}

if [[ $1 == "local" ]]
    then
<<<<<<< HEAD
        launch_unit_tests && launch_pylint ./src/sfctl && launch_pylint ./src/checkers
=======
        launch_unit_tests && launch_pylint ./src/sfcli && launch_pylint ./src/checkers
>>>>>>> master
elif [[ $1 == "test" ]]
    then
        launch_unit_tests
elif [[ $1 == "lint" ]]
    then
        echo "Linting CLI..."
<<<<<<< HEAD
        launch_pylint ./src/sfctl
=======
        launch_pylint ./src/sfcli
>>>>>>> master
        r1=$?
        echo "Linting Checker..."
        launch_pylint ./src/checkers
        r2=$?
        exit $((r1 + r2))
fi
