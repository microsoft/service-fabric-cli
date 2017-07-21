 python $(which pylint) ./src/checkers --msg-template='{path}({line}): [{msg_id}{obj}] {msg}' --load-plugins=checkers
 