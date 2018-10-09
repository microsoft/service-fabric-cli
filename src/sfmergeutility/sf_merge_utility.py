# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import json
import os
import re
import yaml
from azext_mesh.sfmergeutility.constants import Constants
from azext_mesh.sfmergeutility.schema import Schema
from azext_mesh.sfmergeutility.sf_yaml_merge import YamlMerge, PartialDocument
from azext_mesh.sfmergeutility.sf_yaml_to_json import YamlToJson
from azext_mesh.sfmergeutility.arm_document_creator import ArmDocumentGenerator

# pylint: disable=line-too-long

class SFMergeUtility(object):

    resourceCreationOrder = [
        Constants.Secret,
        Constants.SecretValue,
        Constants.Volume,
        Constants.Network,
        Constants.Gateway,
        Constants.Application
    ]

    @staticmethod
    def SFMergeUtility(inputList, outputFormat, parameterFile=None, outputDir=None, prefix="merged-", region="westus"):

        if(not outputDir or not outputDir.strip()):
            outputDir = os.getcwd()
        if not os.path.exists(outputDir):
            os.makedirs(outputDir)

        #Read the settings.json file
        dir_path = os.path.dirname(os.path.realpath(__file__))
        settingsFile = os.path.join(dir_path, "settings.json")
        primitivesList = {}
        with open(settingsFile) as fp_settings:
            settings_data = json.load(fp_settings, encoding='utf-8')
            primitivesList = settings_data.get("primitiveProperties")

        mergedResourceDocuments = SFMergeUtility.LoadAndMergePartialDocuments(inputList)

        # read parametes file and replace params
        parameters = SFMergeUtility.GetParameters(parameterFile)
        if parameters and parameters.keys:
            for mergedresourcedoc in mergedResourceDocuments:
                mergedResourceDocuments[mergedresourcedoc] = SFMergeUtility.ReplaceParameterValues(mergedResourceDocuments[mergedresourcedoc], parameters)

        if outputFormat.upper() == "SF_SBZ_YAML":
            # for mode generate yaml
            SFMergeUtility.SaveAllMergedDocuments(mergedResourceDocuments, prefix, outputDir, "yaml", None)
        elif outputFormat.upper() == "SF_SBZ_JSON":
            # for mode generate JSON
            # call yaml to json
            SFMergeUtility.SaveAllMergedDocuments(mergedResourceDocuments, prefix, outputDir, "json", primitivesList)
        elif outputFormat.upper() == "SF_SBZ_RP_JSON":
            # for mode generate ARMDocument
            # call arm document generator
            merged_jsons = {}
            for resourceIter in mergedResourceDocuments:
                resource_json = YamlToJson.ToOrderedDict(mergedResourceDocuments[resourceIter], None, primitivesList)
                merged_jsons[resourceIter] = resource_json

            ArmDocumentGenerator.generate(merged_jsons, region, os.path.join(outputDir, prefix + "arm_rp.json"))

    @staticmethod
    def GetParameters(parameterFile):
        paramsList = None
        json_object = None
        if parameterFile:
            extension = os.path.splitext(parameterFile)[1]
            if extension.lower() == ".yaml":
                # load yaml
                yaml_file = yaml.compose(open(parameterFile))
                json_object = YamlToJson.ToOrderedDict(yaml_file, None, None)
            elif extension.lower() == ".json":
                # load json
                with open(parameterFile, 'r') as parameterFile_fp:
                    json_object = json.load(parameterFile_fp)

            paramsList = {}
            for obj in json_object:
                paramsList[obj] = json_object[obj]

        return paramsList

    @staticmethod
    def ReplaceParameterValues(mergedResourceDocuments, parametersToReplace):
        yaml_string = yaml.serialize(mergedResourceDocuments)

        for parameterIter in parametersToReplace:
            if yaml_string.find("'[parameters(''{0}'')]'".format(parameterIter)) >= 0:
                yaml_string = yaml_string.replace("'[parameters(''{0}'')]'".format(parameterIter), parametersToReplace[parameterIter])

        yaml_dict = yaml.compose(yaml_string)
        return yaml_dict

    @staticmethod
    def SaveMergedDocumentsAsYaml(mergedDocument, outputdir, fileName):
        final_yaml = yaml.serialize(mergedDocument)
        output_file_path = os.path.join(outputdir, fileName + ".yaml")
        with open(output_file_path, 'w+') as f:
            f.write(final_yaml)

    @staticmethod
    def SaveMergedDocumentsAsJson(mergedDocument, kind, outputdir, fileName, primitivesList):
        final_json = YamlToJson.ToJson(mergedDocument, kind, primitivesList)
        output_file_path = os.path.join(outputdir, fileName + ".json")
        with open(output_file_path, 'w+') as f:
            f.write(final_json)

    @staticmethod
    def SaveAllMergedDocuments(resourceMergedDocumentMap, fileNamePrefix, outputdir, yaml_json_switch, primitivesList):
        count = 1
        for kind in SFMergeUtility.resourceCreationOrder:
            items = [key for key in resourceMergedDocumentMap if key[0] == kind]
            for item in items:
                mappingNode = resourceMergedDocumentMap[item]
                keyNode = mappingNode.value[0][0]
                valueNode = mappingNode.value[0][1]
                selectedNameNode = YamlMerge.GetChildNode(valueNode, Constants.PrimaryPropertyName)
                selectedSchemaVersionNode = YamlMerge.GetChildNode(valueNode, Constants.SchemaVersion)

                resourceKind = keyNode.value
                resourceName = selectedNameNode.value
                schemaVersion = selectedSchemaVersionNode.value

                fullyQualifiedResourceName = resourceName

                if Constants.FullyQualifiedResourceNameSeparator in resourceName:
                    resourceName = resourceName[(resourceName.index(Constants.FullyQualifiedResourceNameSeparator) + 1):]

                selectedNameNode.value = resourceName

                fileName = "%s%s_%s_%s"%(fileNamePrefix, str(count).zfill(4), resourceKind, fullyQualifiedResourceName)
                fileName = re.sub(r'[^\w\-_\. ]', '_', fileName)
                fileName = re.sub(r'/', '_', fileName)

                rootN = yaml.MappingNode(YamlMerge.TAG_MAP, [])
                rootN.value.append((yaml.ScalarNode(YamlMerge.TAG_STR, 'type'), yaml.ScalarNode(YamlMerge.TAG_STR, resourceKind)))
                rootN.value.append((yaml.ScalarNode(YamlMerge.TAG_STR, 'name'), yaml.ScalarNode(YamlMerge.TAG_STR, resourceName)))
                rootN.value.append((yaml.ScalarNode(YamlMerge.TAG_STR, 'api-version'), yaml.ScalarNode(YamlMerge.TAG_STR, Schema.SchemaVersionFabricApiVersionMap[schemaVersion])))
                rootN.value.append((yaml.ScalarNode(YamlMerge.TAG_STR, 'fullyQualifiedResourceName'), yaml.ScalarNode(YamlMerge.TAG_STR, fullyQualifiedResourceName)))
                rootN.value.append((yaml.ScalarNode(YamlMerge.TAG_STR, 'description'), mappingNode))

                if yaml_json_switch == 'yaml':
                    SFMergeUtility.SaveMergedDocumentsAsYaml(rootN, outputdir, fileName)
                elif yaml_json_switch == 'json':
                    SFMergeUtility.SaveMergedDocumentsAsJson(rootN, resourceKind, outputdir, fileName, primitivesList)

                count += 1

    @staticmethod
    def LoadAndMergePartialDocuments(inputList):
        # load all yamls inputs
        partialResourceDocumentMap = {}
        for s in inputList:
            my_dict = yaml.load(open(s))
            mappingNode = yaml.compose(open(s))

            kind = list(my_dict.keys())[0]
            name = my_dict.get(kind).get(Constants.PrimaryPropertyName)
            key = (kind, name)

            yamlDocument = PartialDocument(mappingNode, s)

            # create a map inputs, group by kind and name
            if key in partialResourceDocumentMap:
                partialResourceDocumentMap[key].append(yamlDocument)
            else:
                tempList = []
                tempList.append(yamlDocument)
                partialResourceDocumentMap[key] = tempList

        mergedDocumentMap = {}
        for key in partialResourceDocumentMap:
            mergedDocument = YamlMerge.Merge(partialResourceDocumentMap[key], key[0], Constants.PrimaryPropertyName)
            mergedDocumentMap[key] = mergedDocument

        return mergedDocumentMap
