# -*-coding:utf8 -*-
import math

import pandas as pd


class LocalMethods(object):
    """
    some tips:
    In this part, we want to implement some basic similarity mesurement methods in network analysis
    the input is a dataframe of pandas with two columns:

    index   source  target
    0       2       3
    1       2       4
    .....

    The implemented methods are listed as follows:
    1) common neighbours (CN)
    2) adamic-adar index (AA)
    3) resource allocation (RA)
    4) Resource Allocation Based on Common Neighbor Interactions (RA-CNI)
    5) Preferential Attachment Index (PA)
    6) Jaccard Coefficient (JC)
    7) Salton Index (SA)
    8) The Sørensen Index (SO)
    9) Hub Promoted Index (HPI)
    10) Hub Depressed Index (HDI)
    11) Local Leicht-Holme-Newman Index (LLHN)

    """

    def __init__(self, df_edge_list):
        self.df_edge_list = df_edge_list

    def cal_CN(self):
        """
        this method is implemented for CN
        input: self.edge_list ---->    the edge list of a graph

        return : df_common_neighbor_count ----> the CN list
            source     target   similarity
            1          2        18
            ....

        """

        df_edge_list_reverse = pd.DataFrame()
        df_edge_list_reverse['source'] = self.df_edge_list['target']
        df_edge_list_reverse['target'] = self.df_edge_list['source']

        df_all_nodes_pair = pd.concat([df_edge_list_reverse, self.df_edge_list])

        """
        get common neighbours
        """

        df_common_neighbor = pd.merge(df_all_nodes_pair, df_all_nodes_pair, on=['target'], how='left').dropna()
        df_common_neighbor = df_common_neighbor[df_common_neighbor['source_x'] != df_common_neighbor['source_y']]
        df_common_neighbor_count = df_common_neighbor.groupby(['source_x', 'source_y']).count()
        df_common_neighbor_count = df_common_neighbor_count.reset_index()

        df_common_neighbor_count.rename(columns={'target': 'similarity'}, inplace=True)
        df_common_neighbor_count.rename(columns={'source_x': 'source', 'source_y': 'target'}, inplace=True)
        return df_common_neighbor_count

    def cal_AA(self):
        """
        this method is implementation for Adamic-Adar index
        input: self.edge_list ---->    the edge list of a graph

        return : df_AA_list ----> the AA list
            source     target   similarity
            1          2        18
            ....

        """

        df_edge_list_reverse = pd.DataFrame()
        df_edge_list_reverse['source'] = self.df_edge_list['target']
        df_edge_list_reverse['target'] = self.df_edge_list['source']

        df_all_nodes_pair = pd.concat([df_edge_list_reverse, self.df_edge_list])
        df_neighbor_count = df_all_nodes_pair.groupby(['source']).count()

        df_neighbor_count = df_neighbor_count.reset_index()
        df_neighbor_count.rename(columns={'target': 'count'}, inplace=True)
        """
        get common neighbours
        """

        df_common_neighbor = pd.merge(df_all_nodes_pair, df_all_nodes_pair, on=['target'], how='left').dropna()
        df_common_neighbor = df_common_neighbor[df_common_neighbor['source_x'] != df_common_neighbor['source_y']]

        df_common_neighbor = pd.merge(df_common_neighbor, df_neighbor_count, left_on=['target'], right_on=['source'],
                                      how='left').dropna()

        df_common_neighbor = df_common_neighbor[['source_x', 'source_y', 'count']]
        df_common_neighbor['count'] = df_common_neighbor['count'].map(lambda x: 1.0 / math.log(x))

        df_AA_list = df_common_neighbor.groupby(['source_x', 'source_y']).sum()
        df_AA_list = df_AA_list.reset_index()

        df_AA_list.rename(columns={'count': 'similarity'}, inplace=True)
        df_AA_list.rename(columns={'source_x': 'source', 'source_y': 'target'}, inplace=True)
        return df_AA_list


def test_similarity():
    edge_file_name = 'transformed_dataset/citeseer/citeseer.edges'
    df_edge_list = pd.read_csv(edge_file_name, delim_whitespace=True, low_memory=False)
    # df_edge_list = pd.DataFrame({'source': [1, 1, 2], 'target': [2, 3, 3]})

    test_local = LocalMethods(df_edge_list)
    test_local.cal_AA()


if __name__ == '__main__':
    test_similarity()
