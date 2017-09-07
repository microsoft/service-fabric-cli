# CLI commands

The Service Fabric CLI commands can be thought of a dictionary, where keys
are strings corresponding to user syntax and the values are python functions.

This means that for every command available to the user, there needs to be
a python function and an entry in this dictionary.

## Command groups

To simplify the mapping, the domain of user syntax strings is further split
into smaller groups. Because the CLI follows a common syntax of:

```bash
sfctl <object> <action>
```

The objects are always command groups, and the actions are individual
commands. For example, `sfctl node start` is the command `start` inside
the command group `node`.

Command groups have unique help strings as specified by their help file
inside the `src\helps` folder.

## Command mappings

Each command group is specified in a `with` statement as a context manager.
Inside the command group, each command is specified with the `command` method.

Take a look at the following example:

```python
client_func_path = 'azure.servicefabric#ServiceFabricClientAPIs.{}'
with CommandSuperGroup(__name__, self, client_func_path,
                       client_factory=client_create) as super_group:
    with super_group.group('cluster') as group:
        group.command('health', 'get_cluster_health')
```

This code will create the following command mapping:

```txt
sfctl cluster health -> azure.servicefabric#ServiceFabricClientAPIs.get_cluster_health
```

The python namespace is specified when creating a `CommandSuperGroup`. In
the previous example, this is `azure.servicefabric#ServiceFabricClientAPIs.{}`,
with the `{}` being used as a format specifier. When specifying the command,
the second argument is the function name in that namespace. In the previous
example this is `get_cluster_health`. Note, the string must be a full namespace
string that is valid in the given Python environment.

The command line syntax is based on the `group` specification and the first
argument to `command`. In this case, there is a group called `cluster`
that contains the command `health`. The `sfctl` prefix is automatically added,
and therefore the full command line syntax becomes `sfctl cluster health`.

## Knack documentation

For more information, take a look at the
[CLI package](https://github.com/Microsoft/knack) used by the Service Fabric
CLI

## Command types

Generally speaking there are two types of commands. Standard commands are
defined by a direct mapping to the python SDK. Custom commands require
additional logic that is implemented in the CLI prior to invoking a REST
API.

### Standard commands

The previously used `sfctl cluster health` command is an example of a
standard command. The command itself is mapped to the Service Fabric Python
SDK directly, the target being
`azure.servicefabric#ServiceFabricClientAPIs.get_cluster_health`. Standard
commands have the following properties:

- Do not require local system access such as file I/O
- Map directly into the Python SDK
- Do not have complex object types as arguments

This means that effectively, the command is fully specified in Swagger, and
the python SDK API can be generated precisely from the swagger.

### Custom commands

A custom command is a command that does not fit the standard command
definition. For example, the `sfctl application upload` command is an example
of a custom command. Custom commands have fewer restrictions. They can be any
python function since they do not neatly fit into the Python SDK.

All custom commands that are defined by the CLI have a target python namespace
of `sfctl`, since they are defined in the same package. For example, custom
application commands use a target namespace of `sfctl.custom_app#{}`.

## Next steps

- [Adding a new custom command]()
- [Adding a new standard command]()
- [Adding non-string command parameters]()
- [Adding command group or command help]()
