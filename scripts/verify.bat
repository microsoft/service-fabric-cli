:: Note: this script does not return an error code because it's meant for manual use only.
@echo off

SETLOCAL

IF %1 == local CALL :lint_func & CALL :test_func

IF %1 == lint CALL :lint_func

IF %1 == test CALL :test_func

EXIT /B 0

:: define function to run linter
:lint_func
echo linting
pylint ./src/sfctl --msg-template="{path}({line}): [{msg_id}{obj}] {msg}" --load-plugins=checkers
pylint ./src/checkers --msg-template="{path}({line}): [{msg_id}{obj}] {msg}" --load-plugins=checkers
EXIT /B 0

:: define function to launch tests
:test_func
echo testing
nose2 -v --with-coverage --coverage sfctl
EXIT /B 0

ENDLOCAL

@echo on



