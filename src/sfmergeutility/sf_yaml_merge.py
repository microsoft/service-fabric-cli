# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import yaml

class ArgumentException(Exception):
    def __init__(self, expression, message):
        super(ArgumentException, self).__init__(message)
        self.expression = expression
        self.message = message

class PartialDocument(object):
    def __init__(self, document, name):
        self.document = document
        self.name = name

class PartialYamlObject(object):
    def __init__(self, name, node):
        self.name = name
        self.node = node

class YamlMerge(object):
    TAG_MAP = 'tag:yaml.org,2002:map'
    TAG_STR = 'tag:yaml.org,2002:str'
    TAG_SEQ = 'tag:yaml.org,2002:seq'
    YAML_ERR_DOCUMENT_NO_OBJECT = 'Document does not contain object'
    YAML_ERR_OBJECT_PRIMARY_KEY_NOT_SCALAR = 'Object primary key passed is not a scalar node'
    YAML_ERR_OBJECT_DOES_NOT_HAVE_PRIMARY_KEY = 'Object does not have primary key associated'
    YAML_ERR_OBJECT_PRIMARY_KEY_DIFFERENT = 'Object primary keys are different'
    YAML_ERR_SRC_AND_DEST_NODE_DIFFERENT = 'Source and destination nodes are of different types'
    YAML_ERR_UNSUPPORTED_NODE_TYPE = 'Node type is not supported'

    @staticmethod
    def Merge(partialDocuments, objectIdentifier, objectPrimaryKey):
        # Nothing to merge
        if not partialDocuments:
            return

        partialNodes = []

        for doc in partialDocuments:
            if isinstance(doc.document, yaml.MappingNode):
                if len(doc.document.value) != 1:
                    raise ArgumentException(YamlMerge.YAML_ERR_DOCUMENT_NO_OBJECT, doc.name)

                childKeyNode, childValNode = doc.document.value[0]

                if childKeyNode.value != objectIdentifier and not isinstance(childValNode, yaml.MappingNode):
                    raise ArgumentException(YamlMerge.YAML_ERR_DOCUMENT_NO_OBJECT, doc.name)

                partialNode = PartialYamlObject(doc.name, childValNode)
                partialNodes.append(partialNode)
            else:
                raise ArgumentException(YamlMerge.YAML_ERR_DOCUMENT_NO_OBJECT, doc.name)

        mergedNode = YamlMerge.MergePartialNodes(partialNodes, objectPrimaryKey)
        mergedRootNode = yaml.MappingNode(YamlMerge.TAG_MAP,
                                          [(yaml.ScalarNode(YamlMerge.TAG_STR, objectIdentifier), mergedNode)])

        return mergedRootNode

    @staticmethod
    def EnsureSameObjectPrimaryKey(partialNodes, objectPrimaryKey):
        primaryKeyValue = None
        for partialNode in partialNodes:
            key_found_flag = False
            for nodeChildKey, nodeChildVal in partialNode.node.value:
                if nodeChildKey.value == objectPrimaryKey:
                    key_found_flag = True

                    if not isinstance(nodeChildKey, yaml.ScalarNode):
                        raise ArgumentException(YamlMerge.YAML_ERR_OBJECT_PRIMARY_KEY_NOT_SCALAR,
                                                partialNode.name)

                    if not primaryKeyValue:
                        primaryKeyValue = nodeChildVal.value
                    else:
                        if primaryKeyValue != nodeChildVal.value:
                            raise ArgumentException(YamlMerge.YAML_ERR_OBJECT_PRIMARY_KEY_DIFFERENT,
                                                    partialNode.name)

            if not key_found_flag:
                raise ArgumentException(YamlMerge.YAML_ERR_OBJECT_DOES_NOT_HAVE_PRIMARY_KEY,
                                        partialNode.name)


    @staticmethod
    def MergePartialNodes(partialNodes, objectPrimaryKey):
        if objectPrimaryKey:
            YamlMerge.EnsureSameObjectPrimaryKey(partialNodes, objectPrimaryKey)

        destNode = YamlMerge.CreateDestNode(yaml.MappingNode('', None), "")
        for node in partialNodes:
            YamlMerge.MergeMappingNodes(destNode, node.node, node.name, objectPrimaryKey)

        return destNode

    @staticmethod
    def GetChildNode(parent, key):
        for k, v in parent.value:
            if k.value == key:
                return v

    @staticmethod
    def GetChildFromSeqNode(node, key):
        for childnode in node.value:
            # if mapping node's scalar node's value is key
            if childnode.value[0].value == key:
                return childnode

    @staticmethod
    def MergeMappingNodes(destNode, srcNode, srcIdentifier, objectPrimaryKey):
        destKeySet = set(map(lambda x: x[0].value, destNode.value))
        for keyNode, valNode in srcNode.value:
            if keyNode.value not in destKeySet:
                destChildNode = YamlMerge.CreateDestNode(valNode, srcIdentifier)
                destNode.value.append((yaml.ScalarNode(YamlMerge.TAG_STR, keyNode.value), destChildNode))
            else:
                destChildNode = YamlMerge.GetChildNode(destNode, keyNode.value)
            YamlMerge.MergeNodes(destChildNode, valNode, srcIdentifier, objectPrimaryKey)

    @staticmethod
    def MergeNodes(dest, src, srcIdentifier, objectPrimaryKey):
        destType = type(dest)
        srcType = type(src)
        if destType != srcType:
            raise ArgumentException(YamlMerge.YAML_ERR_SRC_AND_DEST_NODE_DIFFERENT,
                                    srcIdentifier)

        if isinstance(src, yaml.ScalarNode):
            YamlMerge.MergeScalarNodes(dest, src)
        elif isinstance(src, yaml.SequenceNode):
            YamlMerge.MergeSequenceNodes(dest, src, srcIdentifier, objectPrimaryKey)
        elif isinstance(src, yaml.MappingNode):
            YamlMerge.MergeMappingNodes(dest, src, srcIdentifier, objectPrimaryKey)
        else:
            raise ArgumentException(YamlMerge.YAML_ERR_UNSUPPORTED_NODE_TYPE,
                                    srcIdentifier)

    @staticmethod
    def MergeScalarNodes(dest, src):
        dest.value = src.value

    @staticmethod
    def SeqNodeContains(node, key):
        keys = set(map(lambda x: x.value[0].value, node.value))
        return key in keys

    @staticmethod
    def MergeSequenceNodes(dest, src, srcIdentifier, objectPrimaryKey):
        if isinstance(src.value[0], yaml.MappingNode) and not objectPrimaryKey:
            # add it to the list of mapping nodes
            for srcChildNode in src.value:
                srcChildKey = srcChildNode.value
                if YamlMerge.SeqNodeContains(dest, srcChildKey):
                    destChildNode = YamlMerge.CreateDestNode(srcChildNode, srcIdentifier)
                    dest.value.append(destChildNode)
                else:
                    destChildNode = YamlMerge.GetChildFromSeqNode(dest, srcChildKey)
                YamlMerge.MergeNodes(destChildNode, srcChildNode, srcIdentifier, objectPrimaryKey)
        else:
            # just combine the sequence
            for srcChildNode in src.value:
                destChildNode = YamlMerge.CreateDestNode(srcChildNode, srcIdentifier)
                dest.value.append(destChildNode)
                YamlMerge.MergeNodes(destChildNode, srcChildNode, srcIdentifier, objectPrimaryKey)

    @staticmethod
    def CreateDestNode(srcNode, srcIdentifier):
        if isinstance(srcNode, yaml.ScalarNode):
            return yaml.ScalarNode(YamlMerge.TAG_STR, '')
        elif isinstance(srcNode, yaml.MappingNode):
            return yaml.MappingNode(YamlMerge.TAG_MAP, [])
        elif isinstance(srcNode, yaml.SequenceNode):
            return yaml.SequenceNode(YamlMerge.TAG_SEQ, [])
        else:
            raise ArgumentException(YamlMerge.YAML_ERR_UNSUPPORTED_NODE_TYPE,
                                    srcIdentifier)

    @staticmethod
    def Test_YamlMerge():
        filesample = '../samples/Input/counterApp-sfbd.yaml'
        filesample2 = '../samples/Input/service.yaml'

        with open(filesample, 'r') as f:
            text = f.read()

        with open(filesample2, 'r') as f:
            text2 = f.read()

        pds = []
        pds.append(PartialDocument(yaml.compose(text), "counterApp-sfbd.yaml"))
        pds.append(PartialDocument(yaml.compose(text2), "service.yaml"))

        return YamlMerge.Merge(pds, "application", "name")
