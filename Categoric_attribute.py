#!/usr/bin/env python
# coding: utf-8

# In[17]:


import pandas as ps
import numpy as nm
import math as mt
import copy

class Node :
    def __init__( self, attribute_name, data, attribute_values, select_from ) :
        self.attribute_name = attribute_name
        self.data = data 
        self.attribute_values = attribute_values
        self.childrens = []
        self.select_from = select_from
    def add_child( self, child_obj ):
        self.childrens.append( child_obj )   

def value_entropy( lable, att, val, data_u ):
    att_col = ps.Series( data_u[ att ] ).tolist()
    lable_col = ps.Series( data_u[ lable ] ).tolist() 
    count1 = 0
    count = 0
    i = 0
    proT = 0
    proF = 0
    while( i < len( lable_col ) ):#Counting size and number of ones for that(val) value of this attribute
        if( att_col[ i ] == val ) :
            count = count + 1
            if( lable_col[ i ] == 1 ) :
                count1 = count1 + 1 #for numbmer of ones
        i = i + 1         

    proT = count1 / count
    proF = 1 - proT
    if( count1 == count or count1 == 0):
        entropy = 0
    else :    
        entropy = ( proT * mt.log( proT )/mt.log( 2 ) + proF * mt.log( proF )/mt.log( 2 ) ) * ( -1 )
    
    return entropy        

def calc_entropy( curr_data, lable ) :
    lable_col = ps.Series( curr_data[ lable ] )
    count1 = 0
    count = 0
    pro1 = 0 
    pro0 = 0
    
    for val in lable_col :
        if( val == 1 ) :
            count1 = count1 + 1
        count = count + 1
        
    pro1 = count1 / count
    pro0 = 1 - pro1
    if( count1 == count or count1 == 0 ) :
        entropy = 0
    else :    
        entropy = ( pro1 * ( mt.log( pro1 ) / mt.log( 2 ) ) + pro0 * ( mt.log( pro0 ) / mt.log( 2 ) ) ) * ( -1 )
    
    return entropy

def select_attribute( curr_data, select_from, parent_entropy ):
    p_row, p_col = curr_data.shape
    ff = 0
    gain_ratio = -10
    for attribute in select_from :
        att_size = p_row #For first attribute size of attribute will be size of dataset
        val_size = []#to store size of class after split using any particular value of that attribute
        val_ent = []#to store entropy of class after split using any particular value of that attribute
        vals_attribute = curr_data[ attribute ].unique()#getting all unique values of a particular col
        for val in vals_attribute :
            c_row, c_col = curr_data[ curr_data[ attribute ] == val ].shape
            val_size.append( c_row )
            val_ent.append( value_entropy( lable, attribute, val, curr_data ) )

        info = 0
        i = 0
        while( i < len( val_size ) ) :#information calculation
            temp = val_size[ i ] / att_size
            temp = temp * val_ent[ i ]
            info = info + temp
            i = i + 1
        gain = parent_entropy - info# gain calculated

        intrinsic_info = 0
        i = 0
        temp = 0
        while( i < len( val_size ) ) :#intinsic info calculation
            temp = val_size[ i ] / att_size 
            temp = temp * ( mt.log( temp ) / mt.log( 2 ) ) 
            intrinsic_info = intrinsic_info + temp
            i = i + 1 
        if( intrinsic_info == 0 ):
            intrinsic_info = 1
        else:
            intrinsic_info = intrinsic_info * ( -1 )
    
        gr = ( gain / intrinsic_info )

        if( gr > gain_ratio or ff == 0 ) :
            gain_ratio = gr 
            attribute_selected = attribute
            if( ff == 0 ) :
                ff = 1 

    return attribute_selected


# In[18]:


data = ps.read_csv("Training.csv") #here data is DataFrame object
row, col = data.shape
print("Rows ", row, "Columns ", col )
col_names = list( data.columns.values )
lable = "left"

to_be_selected = []
i = 0

while( i < col ) :#Running while loop for each column to filter out categoric attribute
    if( col_names[ i ] != lable and len( data[ col_names[ i ] ].unique() ) <= 10 ):   
        to_be_selected.append( col_names[ i ] )    
    i = i + 1      

Entropy_Def = calc_entropy( data, lable )
#entropy for first attribute
#Entropy of first attribute will be same irrespective of attribute we are selecting for it, 
#as data available for it is the whole dataset

ff = 0 #to make first gain ratio enter correctly
gain_ratio = 0
attribute_selected = select_attribute( data, to_be_selected, Entropy_Def )


to_be_selected.remove( attribute_selected )
root = Node( attribute_selected, data, cat[ attribute_selected ], to_be_selected ) #Creating root node
print( "Root : ", root.attribute_name, "\nValues ", root.attribute_values)

nodes = []

nodes.append( root )

while( len( nodes ) > 0 ) :
    current = nodes.pop( 0 )
    
    attribute = current.attribute_name
    print( "\n\nParent ", attribute )
    curr_data = current.data
    select_from = copy.deepcopy( current.select_from )
    values = current.attribute_values
    curr_entropy = calc_entropy( curr_data, lable )
    if( curr_entropy != 0 and len( select_from ) > 0 ) :
        for val in values :
            node_data = curr_data[ curr_data[ attribute ] == val ]
            attribute_selected = select_attribute( node_data, select_from, curr_entropy )#current data, list of attributes from selection to be made,
                                                                                       #categoric attributes with their all possible values
            node_select_from = copy.deepcopy( select_from )
            node_select_from.remove( attribute_selected )
            child = Node( attribute_selected, node_data, node_data[ attribute_selected ].unique(), node_select_from )
            current.childrens.append( child )
            if( calc_entropy( node_data, lable ) != 0 ):
                nodes.append( child )
            print( "Child ", attribute_selected, "for value ", val )
    current.data.drop( columns = current.data.columns )        


# In[24]:


data = ps.read_csv("train.csv") #here data is DataFrame object
# print( data )


# In[ ]:




