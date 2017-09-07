# Defining custom commands

Custom commands are one type of Service Fabric command. Custom commands tend
to require more operations, such as file I/O or HTTP request modification. This
is often the case for commands that cannot be easily specified in Swagger. For
example, the `application upload` command is a good example of a custom
command since it sends multiple requests and performs client file I/O.

For more information about the differences between custom and standard
commands, see the [related documentation](docs/command_logic.md).

## Custom command files

All custom commands are located in the `src/sfctl` folder and are in files
prefixed by `custom_`. The commands are split across files that roughly
correspond to their command group.

The mappings between command line syntax and python command line is stored
in the `src/commands.py` file, similar to standard commands.

Tests for custom commands are in their corresponding file under
`src/sfctl/tests`.

## Function

First, define the function that performs the command logic in Python. This
should be done in the `custom_<target>.py` file. Here, `<target>` refers
to the command group name.

For the function signature be sure to include `client` as the first argument,
as the client factory will pass this into your function upon invocation. For
example, here is the function signature for `sfctl compose create`:

```python
def create_compose_application(client, compose_file, application_id,
                               repo_user=None, encrypted=False,
                               repo_pass=None, timeout=60):

    [...]

    client.create_compose_application(model, timeout)
```

Here `[...]` refers to the actual code logic in python.

## Mapping

Once the function has been defined, add an additional `command` under the
command group corresponding to your function. For example, here is the mapping
for `sfctl compose create`. Mappings are inside the `commands.py` file:

```python
with CommandSuperGroup(__name__, self, 'sfctl.custom_app#{}',
                       client_factory=client_create) as super_group:
    with super_group.group('compose') as group:
        group.command('create', 'create_compose_application')
```

Be sure to check the function namespace, in this case `sfctl.custom_app`. Also,
check if you need to have an API client or not by specifying the
`client_factory` argument.

## Test

Once the command has a mapping, be sure to include Nose test cases for the
command logic. The tests should be added as functions that include the
phrase `test` at the end of the function name.

All of the unit tests are under the `src/sfctl/tests` folder.
