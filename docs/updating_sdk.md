# Updating Service Fabric Python SDK

The Service Fabric CLI uses the underlying Azure Python SDK generated from
Azure Service Fabric swagger specifications.

The latest swagger specification can be found
[in the Azure GitHub repo](https://github.com/Azure/azure-rest-api-specs/blob/current/specification/servicefabric/data-plane/Microsoft.ServiceFabric/5.6/servicefabric.json).
For contributing guidelines see the repository documentation.

The corresponding python SDK can be found
[in a different Azure GitHub repo](https://github.com/Azure/azure-sdk-for-python/tree/master/azure-mgmt-servicefabric).

After changes have been made to both repos and a new Python SDK package has
been published, modify the following section in `src\setup.py`:

```python
install_requires=[
    'azure-servicefabric==5.6.130',
],
```

The new version should replace the `5.6.130` string. After making this change,
be sure to re-run the `pip install -e .\src` command as the new package
will need to be installed.
