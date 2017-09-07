# Command help

Each command and command group should have help documentation specified
inside a file under `src/sfctl/helps`. The help documentation can be viewed
by calling a command or command group with the `-h` parameter.

## Authoring help

Help documentation is specified in the `src/sfctl/helps` folder. Help files
are imported at the beginning of the command file. For example, this is the
documetnation for application command help:

```python
import sfctl.helps.app # pylint: disable=unused-import
```

These imports appear unused, but each help file modifies the global dictionary
`helps`. This dictionary is used by the CLI.

Each key in the `helps` dictionary corersponds to a complete command. For
example, take a look at the `sfctl compose create` command help string:

```python
helps['compose create'] = """
    type: command
    short-summary: Creates a Service Fabric application from a Compose file
    parameters:
        - name: --repo-pass
          type: string
          short-summary: Encrypted contain repository password
"""
```

Here the help is a YAML string with summaries. For more information on each
property, see the following sections.

### Summaries

Commands, command groups and parameters can all contain `short-summary`
properties. Parameter short summaries are displayed alongside parameters when
requesting command help. Command short summaries are displayed when request
command group help.

Furthermore, commands can contain a `long-summary` property that is shown
when help is requested for the specific command. A long summary is a more
detailed description.

### Parameters

Parameters should include a `type` to specify the type of the parameter. They
should also be referenced by their full name. A command can have multiple
parameters, specified by a YAML list.

## Knack documentation

For more information, take a look at the
[CLI module documentation](https://github.com/Microsoft/knack/blob/master/docs/help.md).
