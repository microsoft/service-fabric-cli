$(which pylint) ./src/sfcli --msg-template='{path}({line}): [{msg_id}{obj}] {msg}' --load-plugins=checkers
