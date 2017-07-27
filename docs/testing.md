# Testing

Tests for the Service Fabric CLI are broken down into three catagories,
unit tests, scenario tests, and live scenario tests.

In most cases when modifying code only unit tests are required. However,
sometimes if functional or integration tests are needed, then scenario
tests can be used.

## Unit tests

These tests should always be run, and can be run in under 10 seconds.
To run these tests, from the root of the repo run the following script:

```bash
./scripts/verify.sh local
```

This will also run PyLint to check code style.

Unit tests should never depend on external connections or local resources such
as file I/O.

## Scenario tests

Scenario tests are designed to be repeatable functional tests. These tests
take advantage of recording thanks to `vcrpy` in the `knack` CLI framework.

For examples of these tests, take a look at `scenario_test.py` in the `tests`
module.

These tests can be run from recordings, or against live Azure Service Fabric
clusters. By default these tests are disabled. To run these more intensive
tests, environment variables must specify a Service Fabric cluster endpoint
to connect to. The expected variable name is as follows:

```bash
EXPORT SF_TEST_ENDPOINT=http://test.azure.com:19080
```

Here, the endpoint should be the HTTP gateway URI of a Service Fabric cluster.

## Live scenario tests

Even more complicated tests cannot be recorded, these must only be run locally
and not as part of automation. Run these to validate complex workflows such as
application life cycle or cluster upgrade.

Specific live tests are documented below:

### Application life cycle (`application_lifecycle_test`)

This tests the basic application life cycle, excluding application upgrade.
Note, this test may result in altered Service Fabric cluster state, be sure
to clean up any state if the test fails before subsequent runs.

#### Enable

Enable this test by specifying a path to a Service Fabric application package:

```bash
EXPORT SF_TEST_APP_PATH=/Users/test/Downloads/sample_apps/CalcApp/
```