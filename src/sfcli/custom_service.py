# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Commands related to managing Service Fabric services"""

from knack.util import CLIError

def correlation_desc(correlated_service, correlation):
    """Get a service correlation description"""
    from azure.servicefabric.models.service_correlation_description import (
        ServiceCorrelationDescription
    )
    if not any([correlated_service, correlation]):
        return None

    if (any([correlated_service, correlation]) and
            not all([correlated_service, correlation])):
        raise CLIError('Must specify both a correlation service and '
                       'correlation scheme')

    return ServiceCorrelationDescription(correlation, correlated_service)

def parse_load_metrics(formatted_metrics):
    """Parse a service load metric description from a string"""
    from azure.servicefabric.models.service_load_metric_description import (
        ServiceLoadMetricDescription
    )

    s_load_list = None
    if formatted_metrics:
        s_load_list = []
        for l in formatted_metrics:
            l_name = l.get('name', None)
            if l_name is None:
                raise CLIError('Could not find specified load metric name')
            l_weight = l.get('weight', None)
            l_primary = l.get('primary_default_load', None)
            l_secondary = l.get('secondary_default_load', None)
            l_default = l.get('default_load', None)
            l_desc = ServiceLoadMetricDescription(l_name, l_weight, l_primary,
                                                  l_secondary, l_default)
            s_load_list.append(l_desc)

    return s_load_list

def parse_placement_policies(formatted_placement_policies):
    """"Parse a placement policy description from a formatted policy"""
    from azure.servicefabric.models.service_placement_non_partially_place_service_policy_description import ServicePlacementNonPartiallyPlaceServicePolicyDescription # pylint: disable=line-too-long

    from azure.servicefabric.models.service_placement_prefer_primary_domain_policy_description import ServicePlacementPreferPrimaryDomainPolicyDescription #pylint: disable=line-too-long

    from azure.servicefabric.models.service_placement_required_domain_policy_description import ServicePlacementRequiredDomainPolicyDescription #pylint: disable=line-too-long
    from azure.servicefabric.models.service_placement_require_domain_distribution_policy_description import ServicePlacementRequireDomainDistributionPolicyDescription #pylint: disable=line-too-long

    if formatted_placement_policies:
        policy_list = []
        # Not entirely documented but similar to the property names
        for policy in formatted_placement_policies:
            p_type = policy.get("type", None)
            if p_type is None:
                raise CLIError(
                    'Could not determine type of specified placement policy'
                )
            if p_type not in ['NonPartiallyPlaceService',
                              'PreferPrimaryDomain', 'RequireDomain',
                              'RequireDomainDistribution']:
                raise CLIError('Invalid type of placement policy specified')
            p_domain_name = policy.get('domain_name', None)

            if p_domain_name is None and p_type != 'NonPartiallyPlaceService':
                raise CLIError(
                    'Placement policy type requires target domain name'
                )
            if p_type == 'NonPartiallyPlaceService':
                policy_list.append(
                    ServicePlacementNonPartiallyPlaceServicePolicyDescription()
                )
            elif p_type == 'PreferPrimaryDomain':
                policy_list.append(
                    ServicePlacementPreferPrimaryDomainPolicyDescription(
                        p_domain_name
                    )
                )
            elif p_type == 'RequireDomain':
                policy_list.append(
                    ServicePlacementRequiredDomainPolicyDescription(
                        p_domain_name
                    )
                )
            elif p_type == 'RequireDomainDistribution':
                policy_list.append(
                    ServicePlacementRequireDomainDistributionPolicyDescription(
                        p_domain_name
                    )
                )
        return policy_list
    return None


def validate_move_cost(move_cost):
    """Validate move cost argument"""

    if move_cost not in [None, 'Zero', 'Low', 'Medium', 'High']:
        raise CLIError('Invalid move cost specified')


def stateful_flags(rep_restart_wait=None, quorum_loss_wait=None,
                   standby_replica_keep=None):
    """Calculate an integer representation of flag arguments for stateful
    services"""

    f = 0
    if rep_restart_wait is not None:
        f += 1
    if quorum_loss_wait is not None:
        f += 2
    if standby_replica_keep is not None:
        f += 4
    return f

def service_update_flags(
        target_rep_size=None, instance_count=None, rep_restart_wait=None,
        quorum_loss_wait=None, standby_rep_keep=None, min_rep_size=None,
        placement_constraints=None, placement_policy=None, correlation=None,
        metrics=None, move_cost=None):
    """Calculate an integer representation of flag arguments for updating
    stateful services"""

    f = 0
    if (target_rep_size is not None) or (instance_count is not None):
        f += 1
    if rep_restart_wait is not None:
        f += 2
    if quorum_loss_wait is not None:
        f += 4
    if standby_rep_keep is not None:
        f += 8
    if min_rep_size is not None:
        f += 16
    if placement_constraints is not None:
        f += 32
    if placement_policy is not None:
        f += 64
    if correlation is not None:
        f += 128
    if metrics is not None:
        f += 256
    if move_cost is not None:
        f += 512
    return f


def validate_service_create_params(stateful, stateless, singleton_scheme,
                                   int_scheme, named_scheme, instance_count,
                                   target_rep_set_size, min_rep_set_size):
    """Validate service creation arguments"""
    if sum([stateful, stateless]) != 1:
        raise CLIError(
            'Specify either stateful or stateless for the service type'
        )
    if sum([singleton_scheme, named_scheme, int_scheme]) != 1:
        raise CLIError('Specify exactly one partition scheme')
    if stateful and instance_count is not None:
        raise CLIError('Cannot specify instance count for stateful services')
    if stateless and instance_count is None:
        raise CLIError('Must specify instance count for stateless services')
    if stateful and not all([target_rep_set_size, min_rep_set_size]):
        raise CLIError(
            'Must specify minimum and replica set size for stateful services'
        )
    if stateless and any([target_rep_set_size, min_rep_set_size]):
        raise CLIError(
            'Cannot specify replica set sizes for statless services'
        )

def parse_partition_policy(named_scheme, named_scheme_list, int_scheme,
                           int_scheme_low, int_scheme_high, int_scheme_count,
                           singleton_scheme):
    """Create a partition scheme"""
    from azure.servicefabric.models.named_partition_scheme_description import NamedPartitionSchemeDescription #pylint: disable=line-too-long
    from azure.servicefabric.models.singleton_partition_scheme_description import SingletonPartitionSchemeDescription #pylint:disable=line-too-long
    from azure.servicefabric.models.uniform_int64_range_partition_scheme_description import UniformInt64RangePartitionSchemeDescription #pylint:disable=line-too-long

    if named_scheme and not named_scheme_list:
        raise CLIError('When specifying named partition scheme, must include '
                       'list of names')
    if (int_scheme
            and not all([int_scheme_low, int_scheme_high, int_scheme_count])):
        raise CLIError('Must specify the full integer range and partition '
                       'count when using an uniform integer partition scheme')

    if not sum([named_scheme, int_scheme, singleton_scheme]) == 1:
        raise CLIError('Specify exactly one partition scheme')

    if named_scheme:
        return NamedPartitionSchemeDescription(len(named_scheme_list),
                                               named_scheme_list)
    elif int_scheme:
        return UniformInt64RangePartitionSchemeDescription(int_scheme_count,
                                                           int_scheme_low,
                                                           int_scheme_high)
    elif singleton_scheme:
        return SingletonPartitionSchemeDescription()

    return None

def validate_activation_mode(activation_mode):
    """Validate activation mode parameters"""
    if activation_mode not in [None, 'SharedProcess', 'ExclusiveProcess']:
        raise CLIError('Invalid activation mode specified')

def create(  # pylint: disable=too-many-arguments, too-many-locals
        client, app_id, name, service_type, stateful=False, stateless=False,
        singleton_scheme=False, named_scheme=False, int_scheme=False,
        named_scheme_list=None, int_scheme_low=None, int_scheme_high=None,
        int_scheme_count=None, constraints=None, correlated_service=None,
        correlation=None, load_metrics=None, placement_policy_list=None,
        move_cost=None, activation_mode=None, dns_name=None,
        target_replica_set_size=None, min_replica_set_size=None,
        replica_restart_wait=None, quorum_loss_wait=None,
        stand_by_replica_keep=None, no_persisted_state=False,
        instance_count=None, timeout=60):
    """
    Creates the specified Service Fabric service from the description.
    :param str app_id: The identity of the parent application. This is
    typically the full id of the application without the 'fabric:' URI scheme.
    :param str name: Name of the service. This should be a child of the
    application id. This is the full name including the `fabric:` URI.
    For example service `fabric:/A/B` is a child of application
    `fabric:/A`.
    :param str service_type: Name of the service type.
    :param bool stateful: Indicates the service is a stateful service.
    :param bool stateless: Indicates the service is a stateless service.
    :param bool singleton_scheme: Indicates the service should have a single
    partition or be a non-partitioned service.
    :param bool named_scheme: Indicates the service should have multiple named
    partitions.
    :param list of str named_scheme_list: JSON encoded list of names to
    partition the service across, if using the named partition scheme
    :param bool int_scheme: Indicates the service should be uniformly
    partitioned across a range of unsigned integers.
    :param str int_scheme_low: The start of the key integer range, if using an
    uniform integer partition scheme.
    :param str int_scheme_high: The end of the key integer range, if using an
    uniform integer partition scheme.
    :param str int_scheme_count: The number of partitions inside the integer
    key range to create, if using an uniform integer partition scheme.
    :param str constraints: The placement constraints as a string. Placement
    constraints are boolean expressions on node properties and allow for
    restricting a service to particular nodes based on the service
    requirements. For example, to place a service on nodes where NodeType
    is blue specify the following:"NodeColor == blue".
    :param str correlation: Correlate the service with an existing service
    using an alignment affinity. Possible values include: 'Invalid',
    'Affinity', 'AlignedAffinity', 'NonAlignedAffinity'.
    :param str load_metrics: JSON encoded list of metrics used when load
    balancing services across nodes.
    :param str placement_policy_list: JSON encoded list of placement policies
    for the service, and any associated domain names. Policies can be one or
    more of: `NonPartiallyPlaceService`, `PreferPrimaryDomain`,
    `RequireDomain`, `RequireDomainDistribution`.
    :param str correlated_service: Name of the target service to correlate
    with.
    :param str move_cost: Specifies the move cost for the service. Possible
    values are: 'Zero', 'Low', 'Medium', 'High'.
    :param str activation_mode: The activation mode for the service package.
    Possible values include: 'SharedProcess', 'ExclusiveProcess'.
    :param str dns_name: The DNS name of the service to be created. The Service
    Fabric DNS system service must be enabled for this setting.
    :param int target_replica_set_size: The target replica set size as a
    number. This applies to stateful services only.
    :param int min_replica_set_size: The minimum replica set size as a number.
    This applies to stateful services only.
    :param int replica_restart_wait: The duration, in seconds, between when a
    replica goes down and when a new replica is created. This applies to
    stateful services only.
    :param int quorum_loss_wait: The maximum duration, in seconds, for which a
    partition is allowed to be in a state of quorum loss. This applies to
    stateful services only.
    :param int stand_by_replica_keep: The maximum duration, in seconds,  for
    which StandBy replicas will be maintained before being removed. This
    applies to stateful services only.
    :param bool no_persisted_state: If true, this indicates the service has no
    persistent state stored on the local disk, or it only stores state in
    memory.
    :param int instance_count: The instance count. This applies to stateless
    services only.
    """
    from azure.servicefabric.models.stateless_service_description import (
        StatelessServiceDescription
    )
    from azure.servicefabric.models.stateful_service_description import (
        StatefulServiceDescription
    )

    validate_service_create_params(stateful, stateless, singleton_scheme,
                                   int_scheme, named_scheme, instance_count,
                                   target_replica_set_size,
                                   min_replica_set_size)
    partition_desc = parse_partition_policy(named_scheme, named_scheme_list,
                                            int_scheme, int_scheme_low,
                                            int_scheme_high, int_scheme_count,
                                            singleton_scheme)
    cor_desc = correlation_desc(correlated_service, correlation)
    load_list = parse_load_metrics(load_metrics)
    place_policy = parse_placement_policies(placement_policy_list)
    validate_move_cost(move_cost)
    validate_activation_mode(activation_mode)

    if stateless:
        svc_desc = StatelessServiceDescription(name, service_type,
                                               partition_desc, instance_count,
                                               "fabric:/" + app_id,
                                               None, constraints,
                                               cor_desc, load_list,
                                               place_policy, move_cost,
                                               bool(move_cost),
                                               activation_mode,
                                               dns_name)

    if stateful:
        flags = stateful_flags(replica_restart_wait, quorum_loss_wait,
                               stand_by_replica_keep)
        svc_desc = StatefulServiceDescription(name, service_type,
                                              partition_desc,
                                              target_replica_set_size,
                                              min_replica_set_size,
                                              not no_persisted_state,
                                              "fabric:/" + app_id,
                                              None, constraints,
                                              cor_desc, load_list,
                                              place_policy, move_cost,
                                              bool(move_cost), activation_mode,
                                              dns_name, flags,
                                              replica_restart_wait,
                                              quorum_loss_wait,
                                              stand_by_replica_keep)

    client.create_service(app_id, svc_desc, timeout)

def validate_update_service_params(stateless, stateful, target_rep_set_size,
                                   min_rep_set_size, rep_restart_wait,
                                   quorum_loss_wait, stand_by_replica_keep,
                                   instance_count):
    """Validate update service parameters"""

    if sum([stateless, stateful]) != 1:
        raise CLIError('Must specify either stateful or stateless, not both')

    if stateless:
        if target_rep_set_size is not None:
            raise CLIError('Cannot specify target replica set size for '
                           'stateless service')
        if min_rep_set_size is not None:
            raise CLIError('Cannot specify minimum replica set size for '
                           'stateless service')
        if rep_restart_wait is not None:
            raise CLIError('Cannot specify replica restart wait duration '
                           'for stateless service')
        if quorum_loss_wait is not None:
            raise CLIError('Cannot specify quorum loss wait duration for '
                           'stateless service')
        if stand_by_replica_keep is not None:
            raise CLIError('Cannot specify standby replica keep duration for '
                           'stateless service')
    if stateful:
        if instance_count is not None:
            raise CLIError('Cannot specify an instance count for a stateful '
                           'service')

def update(client, service_id, stateless=False, stateful=False, #pylint: disable=too-many-locals
           constraints=None, correlation=None, correlated_service=None,
           load_metrics=None, placement_policy_list=None,
           move_cost=None, instance_count=None, target_replica_set_size=None,
           min_replica_set_size=None, replica_restart_wait=None,
           quorum_loss_wait=None, stand_by_replica_keep=None, timeout=60):
    """
    Updates the specified service using the given update description.
    :param str service_id: Target service to update. This is typically the full
    id of the service without the 'fabric:' URI scheme.
    :param bool stateless: Indicates the target service is a stateless service.
    :param bool stateful: Indicates the target service is a stateful service.
    :param str constraints: The placement constraints as a string. Placement
    constraints are boolean expressions on node properties and allow for
    restricting a service to particular nodes based on the service
    requirements. For example, to place a service on nodes where NodeType is
    blue specify the following: "NodeColor == blue".
    :param str correlation: Correlate the service with an existing service
    using an alignment affinity. Possible values include: 'Invalid',
    'Affinity', 'AlignedAffinity', 'NonAlignedAffinity'.
    :param str correlated_service: Name of the target service to correlate
    with.
    :param str load_metrics: JSON encoded list of metrics
    used when load balancing across nodes.
    :param str placement_policy_list: JSON encoded list of placement policies
    for the service, and any associated domain names. Policies can be one or
    more of: `NonPartiallyPlaceService`, `PreferPrimaryDomain`,
    `RequireDomain`, `RequireDomainDistribution`.
    :param str move_cost: Specifies the move cost for the service. Possible
    values are: 'Zero', 'Low', 'Medium', 'High'.
    :param int instance_count: The instance count. This applies to stateless
    services only.
    :param int target_replica_set_size: The target replica set size as a
    number. This applies to stateful services only.
    :param int min_replica_set_size: The minimum replica set size as a number.
    This applies to stateful services only.
    :param str replica_restart_wait: The duration, in seconds, between when a
    replica goes down and when a new replica is created. This applies to
    stateful services only.
    :param str quorum_loss_wait: The maximum duration, in seconds, for which a
    partition is allowed to be in a state of quorum loss. This applies to
    stateful services only.
    :param str stand_by_replica_keep: The maximum duration, in seconds,  for
    which StandBy replicas will be maintained before being removed. This
    applies to stateful services only.
    """
    from azure.servicefabric.models.stateful_service_update_description import StatefulServiceUpdateDescription #pylint: disable=line-too-long
    from azure.servicefabric.models.stateless_service_update_description import StatelessServiceUpdateDescription #pylint: disable=line-too-long

    validate_update_service_params(stateless, stateful,
                                   target_replica_set_size,
                                   min_replica_set_size, replica_restart_wait,
                                   quorum_loss_wait, stand_by_replica_keep,
                                   instance_count)

    cor_desc = correlation_desc(correlated_service, correlation)
    metric_desc = parse_load_metrics(load_metrics)
    place_desc = parse_placement_policies(placement_policy_list)
    validate_move_cost(move_cost)

    flags = service_update_flags(target_replica_set_size, instance_count,
                                 replica_restart_wait, quorum_loss_wait,
                                 stand_by_replica_keep, min_replica_set_size,
                                 constraints, place_desc, cor_desc,
                                 metric_desc, move_cost)

    update_desc = None
    if stateful:
        update_desc = StatefulServiceUpdateDescription(flags, constraints,
                                                       cor_desc,
                                                       metric_desc,
                                                       place_desc,
                                                       move_cost,
                                                       target_replica_set_size,
                                                       min_replica_set_size,
                                                       replica_restart_wait,
                                                       quorum_loss_wait,
                                                       stand_by_replica_keep)

    if stateless:
        update_desc = StatelessServiceUpdateDescription(flags, constraints,
                                                        cor_desc,
                                                        metric_desc,
                                                        place_desc,
                                                        move_cost,
                                                        instance_count)

    client.update_service(service_id, update_desc, timeout)

def parse_package_sharing_policies(formatted_policies):
    """Parse package sharing policy description from a JSON encoded set of
    policies"""
    from azure.servicefabric.models.package_sharing_policy_info import (
        PackageSharingPolicyInfo
    )
    if not formatted_policies:
        return None

    list_psps = []
    for policy in formatted_policies:
        policy_name = policy.get("name", None)
        if policy_name is None:
            raise CLIError('Could not find name of sharing policy element')
        policy_scope = policy.get("scope", None)
        if policy_scope not in [None, 'All', 'Code', 'Config', 'Data']:
            raise CLIError('Invalid policy scope specified')
        list_psps.append(PackageSharingPolicyInfo(policy_name, policy_scope))
    return list_psps


def package_upload(client, node_name, service_manifest_name, app_type_name,
                   app_type_version, share_policy=None, timeout=60):
    """
    Downloads packages associated with specified service manifest to the image
    cache on specified node.
    :param str node_name: The name of the node.
    :param str service_manifest_name: The name of service manifest associated
    with the packages that will be downloaded.
    :param str app_type_name: The name of the application manifest for
    the corresponding requested service manifest.
    :param str app_type_version: The version of the application
    manifest for the corresponding requested service manifest.
    :param str share_policy: JSON encoded list of sharing policies. Each
    sharing policy element is composed of a 'name' and 'scope'. The name
    corresponds to the name of the code, configuration, or data package that
    is to be shared. The scope can either 'None', 'All', 'Code', 'Config' or
    'Data'.
    """
    from azure.servicefabric.models.deploy_service_package_to_node_description import DeployServicePackageToNodeDescription #pylint: disable=line-too-long

    list_psps = parse_package_sharing_policies(share_policy)

    desc = DeployServicePackageToNodeDescription(service_manifest_name,
                                                 app_type_name,
                                                 app_type_version,
                                                 node_name, list_psps)
    client.deployed_service_package_to_node(node_name, desc, timeout)
