# -*-coding:utf-8-*-

import os

import networkx as nx
import pandas as pd


class NodeReNumber(object):
    """
    this class is designed to transform the original network
        1) Reorder the nodeID
        2) Rewrite the label with number
        3) Save the x.edges xx.nodes in another dirctory
    """

    def __init__(self, edge_file_name, node_label_filename, save_prefix):
        self.edgeName = edge_file_name
        self.nodeName = node_label_filename

        self.saveEdge = save_prefix + '.edges'
        self.saveNode = save_prefix + '.nodes'

        save_dir = os.path.join('transformed_dataset', save_prefix)

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        self.saveDir = save_dir

    def get_node_map_dict(self):
        df_edge = pd.read_csv(self.edgeName, names=['source', 'target'], delim_whitespace=True, low_memory=False)
        df_node = pd.read_csv(self.nodeName, header=None, delim_whitespace=True, low_memory=False)

        col_num = df_node.shape[1]
        names = ['nodeID'] + ['f_%d' % i for i in range(col_num - 2)] + ['label']
        df_node = pd.read_csv(self.nodeName, names=names, delim_whitespace=True, low_memory=False)
        df_node = df_node[['nodeID', 'label']]

        labels = set(df_node['label'].tolist())
        nodes_list = df_node['nodeID'].tolist()

        nodes_list_1 = df_edge['source'].tolist()
        nodes_list_2 = df_edge['target'].tolist()

        nodes_list = nodes_list + nodes_list_1 + nodes_list_2
        nodes_list = list(set(nodes_list))

        self.nodeName2ID = {}
        for i, tName in enumerate(nodes_list):
            self.nodeName2ID[tName] = i

        self.label2num = {}
        for i, label in enumerate(labels):
            self.label2num[label] = i

    def transform_edge_new(self):

        df = pd.read_csv(self.edgeName, names=['source', 'target'], delim_whitespace=True, low_memory=False)
        G = nx.from_pandas_edgelist(df, source='source', target='target')

        # 最大联通子图
        largest_cc = max(nx.connected_component_subgraphs(G), key=len)

        df_new_edges = nx.to_pandas_edgelist(largest_cc)

        df_new_edges['source'] = df_new_edges['source'].map(lambda x: self.nodeName2ID[x])
        df_new_edges['target'] = df_new_edges['target'].map(lambda x: self.nodeName2ID[x])

        df_new_edges.to_csv(self.saveDir + '/' + self.saveEdge, index=False, sep=' ')

    def transform_edge(self):

        df = pd.read_csv(self.edgeName, names=['source', 'target'], delim_whitespace=True, low_memory=False)

        df['source'] = df['source'].map(lambda x: self.nodeName2ID[x])
        df['target'] = df['target'].map(lambda x: self.nodeName2ID[x])

        df.to_csv(self.saveDir + '/' + self.saveEdge, index=False, sep=' ')

    def transform_node(self):

        df = pd.read_csv(self.nodeName, header=None, delim_whitespace=True, low_memory=False)
        col_num = df.shape[1]
        names = ['nodeID'] + ['f_%d' % i for i in range(col_num - 2)] + ['label']
        df = pd.read_csv(self.nodeName, names=names, delim_whitespace=True, low_memory=False)
        df_new = df[['nodeID', 'label']].copy()
        df_new['nodeID'] = df_new['nodeID'].map(lambda x: self.nodeName2ID[x])
        df_new['label'] = df_new['label'].map(lambda x: self.label2num[x])

        df_new.to_csv(self.saveDir + '/' + self.saveNode, index=False, sep=' ')

    def transform(self):
        self.get_node_map_dict()
        self.transform_edge_new()
        self.transform_node()


if __name__ == '__main__':
    citeEdges = 'dataset/citeseer/citeseer.cites'
    citeNodes = 'dataset/citeseer/citeseer.content'
    test = NodeReNumber(citeEdges, citeNodes, 'citeseer')
    test.transform()
