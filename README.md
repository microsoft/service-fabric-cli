# Service Fabric CLI (sfctl)

Command-line interface for interacting with Azure Service Fabric clusters and
their related entities.

## Installation

```bash
pip install sfctl
```

### Launching

```bash
sfctl <command>
```

For more information, specify the `-h` flag:

```bash
sfctl -h
```

## Guides and How-To

Follow these tips and instructions when contributing to this repository.

### Development cycle

- [Developer setup](docs/dev_setup.md)
- [Detailed testing guide](docs/testing.md)
- [Contributing guidelines](docs/coding_requirements.md)

### Working on commands

- [Updating Service Fabric Python SDK](docs/updating_sdk.md)
- [Command mappings and logic](/docs/command_logic.md)
- [Adding a new custom command](/docs/custom_commands.md)
- [Adding a new standard command](/docs/standard_commands.md)
- [Adding non-string command arguments](/docs/params.md)
- [Adding command group or command help](/docs/command_helps.md)g

## Contributing

This project has adopted the
[Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information, see the
[Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any
additional questions or comments.
