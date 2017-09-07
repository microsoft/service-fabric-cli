# Handling arguments

By default all commands will pass arguments as strings. That means the mapped
Python functions will be called with string arguments. To parse objects or
convert the string arguments to other type, add CLI arguments to the associated
commands.

Any type conversion will be performed to modify the command line arguments
into different Python types.

## Argument scope

All arguments are specified in the `src/sfctl/params.py` file. Each argument
is specified inside an argument context.

For example, the timeout argument, or `-t` is defined with a global context:

```python
with ArgumentsContext(self, '') as arg_context:
    arg_context.argument('timeout', type=int, default=60,
                         options_list=('-t', '--timeout'),
                         help='Server timeout in seconds')
```

Here, the 2nd argument to the `ArgumentsContext` is the command that will
have an argument associated with it.

## Complex types

Take a look at how `service create` specifies int arguments.

```python
with ArgumentsContext(self, 'service create') as arg_context:
    arg_context.argument('instance_count', type=int)
```

Here, the command `sfctl service create` will have the argument
`--instance-count` modified by calling `int` on the string argument
prior to invoking the mapped Python function.

### Custom types

The argument to `type` can be any function that takes a string as the single
argument, and then returns the parsed object. This is useful if you want to
perform additional modification to an argument prior to invoking the 
mapped python function.

## Optional arguments

Optional arguments can be specified in one of two ways. They can be either a
custom argument, or as an optional argument in the Python function definition.

If specifying an optional custom argument simply specify the optional
`default` argument when calling `argument` from the `ArgumentsContext`.

Otherwise, specify the default value inside the Python function definition.

## Knack documentation

For more information, take a look at the
[CLI package documentation](https://github.com/Microsoft/knack/blob/master/docs/arguments.md).
