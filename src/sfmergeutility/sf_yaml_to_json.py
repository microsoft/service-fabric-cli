# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import json
import re
from collections import OrderedDict
import yaml

class YamlToJson(object):

    @staticmethod
    def ToOrderedDict(yamlNode, outputPropertyFilter, primitiveProperties):
        ordered_dict = YamlToJson.Serialize(yamlNode)

        if primitiveProperties:
            YamlToJson.FixProperties(ordered_dict, primitiveProperties)

        if outputPropertyFilter:
            descNode = ordered_dict['description']
            for k in descNode:
                if k == outputPropertyFilter:
                    ordered_dict['description'] = descNode[k]
                    break

        return ordered_dict

    @staticmethod
    def ToJson(yamlNode, outputPropertyFilter, primitiveProperties):
        ordered_dict = YamlToJson.ToOrderedDict(yamlNode, outputPropertyFilter, primitiveProperties)

        return json.dumps(ordered_dict, indent=4)

    @staticmethod
    def Serialize(yamlNode):

        if isinstance(yamlNode, yaml.MappingNode):
            writer_dict = OrderedDict()
            writer_dict = YamlToJson.SerializeMappingNode(yamlNode)
            return writer_dict
        elif isinstance(yamlNode, yaml.SequenceNode):
            writer_dict = OrderedDict()
            writer_dict = YamlToJson.SerializeSequenceNode(yamlNode)
            return writer_dict
        elif isinstance(yamlNode, yaml.ScalarNode):
            return YamlToJson.SerializeScalarNode(yamlNode)

    @staticmethod
    def SerializeMappingNode(yamlNode):
        writer_dict = OrderedDict()

        for yaml_node_val in yamlNode.value:
            writer_dict[yaml_node_val[0].value] = YamlToJson.Serialize(yaml_node_val[1])

        return writer_dict

    @staticmethod
    def SerializeSequenceNode(yamlNode):
        writer_dict = []

        for yaml_node_val in yamlNode.value:
            writer_dict.append(YamlToJson.Serialize(yaml_node_val))

        return writer_dict

    @staticmethod
    def SerializeScalarNode(yamlNode):
        return yamlNode.value

    @staticmethod
    def FixProperties(jsonDict, primitiveProperties):
        for primitiveProperty in primitiveProperties:
            pathComponents = list(filter(None, re.split("[\\/]+", primitiveProperty['path'])))
            if pathComponents:
                YamlToJson.FindRootAndFixProperty(jsonDict, pathComponents, primitiveProperty['type'], 0)

    @staticmethod
    def FindRootAndFixProperty(jsonDict, pathComponents, primitiveType, level):
        pathHead = pathComponents[0]
        if isinstance(jsonDict, list):
            for k in jsonDict:
                YamlToJson.FindRootAndFixProperty(k, pathComponents, primitiveType, level)
        elif isinstance(jsonDict, OrderedDict):
            for k in jsonDict:
                if k == pathHead:
                    # root found
                    YamlToJson.FixProperty(jsonDict, pathComponents, primitiveType, level)
                else:
                    YamlToJson.FindRootAndFixProperty(jsonDict[k], pathComponents, primitiveType, level)

    @staticmethod
    def FixProperty(jsonDict, pathComponents, primitiveType, level):
        remaining = len(pathComponents) - level
        if remaining == 0:
            return
        elif remaining == 1:
            YamlToJson.FixPropertyAtLeaf(jsonDict, pathComponents[level], primitiveType)
        else:
            if isinstance(jsonDict, list):
                for k in jsonDict:
                    YamlToJson.FixProperty(k, pathComponents, primitiveType, level)
            elif isinstance(jsonDict, OrderedDict):
                for k in jsonDict:
                    pathComponent = pathComponents[level]
                    if k == pathComponent:
                        YamlToJson.FixProperty(jsonDict[k], pathComponents, primitiveType, level+1)

    @staticmethod
    def FixPropertyAtLeaf(jsonDict, propertyName, primitiveType):
        if isinstance(jsonDict, list):
            for n in jsonDict:
                YamlToJson.FixPropertyAtLeaf(n, propertyName, primitiveType)
        for k in jsonDict:
            if k == propertyName:
                if primitiveType == 'Integer':
                    jsonDict[k] = int(jsonDict[k])
                elif primitiveType == 'Boolean':
                    jsonDict[k] = (jsonDict[k] == 'true' or jsonDict[k] == 'True')
                elif primitiveType == 'Double':
                    jsonDict[k] = float(jsonDict[k])
                break
                    