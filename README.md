# DM_Implement
data preprocessing and similarity methods

## data preprocessing
this class is designed to transform the original network  
* Reorder the nodeID 
* Rewrite the label with number
* Save the x.edges xx.nodes in another dirctory
## similarity methods
In this part, this project want to implement some basic similarity mesurement methods in network analysis.  
the input is a dataframe of pandas with two columns:

    index   source  target
    0       2       3
    1       2       4
    .....
    
The implemented methods are listed as follows:  
* common neighbours (CN)  
* adamic-adar index (AA)  
* resource allocation (RA)  
* Resource Allocation Based on Common Neighbor Interactions (RA-CNI)  
* Preferential Attachment Index (PA)  
* accard Coefficient (JC)  
* Salton Index (SA)  
* The Sørensen Index (SO)  
* Hub Promoted Index (HPI)  
* Hub Depressed Index (HDI)  
* Local Leicht-Holme-Newman Index (LLHN)  
