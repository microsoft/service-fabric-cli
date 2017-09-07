# Defining standard commands

Standard commands can be specified entirely by their swagger definition. The
swagger definition can be used to generate the python function. It is
sufficient to add just a mapping for the command syntax for a standard
command.

For more information about the differences between standard and custom
commands, see the [related documentation](docs/command_logic.md).

## Standard command files

All standard commands are located in the `src/sfctl/commands.py` file.

Tests for custom commands are in their corresponding file under
`src/sfctl/tests`.

## Mapping

To define a new standard command, add an additional `command` under the
command group corresponding to your command. For example, here is the mapping
for `sfctl cluster health`. Mappings are inside the `commands.py` file:

```python
with CommandSuperGroup(__name__, self, client_func_path,
                       client_factory=client_create) as super_group:
    with super_group.group('cluster') as group:
        group.command('health', 'get_cluster_health')
```

Here, the Python SDK client contains a function called `get_cluster_health`
which will get mapped to the CLI syntax `sfctl cluster health`.

## Test

Once the command has a mapping, be sure to include Nose test cases for the
command logic. The tests should be added as functions that include the
phrase `test` at the end of the function name.

All of the unit tests are under the `src/sfctl/tests` folder.
