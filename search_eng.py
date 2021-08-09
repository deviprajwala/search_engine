#implementation of vector space model and page rank algorithm for search engine

import pandas
#module to read the contents of the file from a csv file

from contextlib import redirect_stdout
#module to redirect the output to a text file

import math
#module to perform mathematical functions

terms = []
#list to store the terms present in the documents

keys = []
#list to store the names of the documents 

vec_dic = {}
#dictionary to store the name of the document and the weight as list

dicti = {}
#dictionary to store the name of the document and the terms present in it as a vector

dummy_list = []
#list for performing some operations and clearing them  

term_freq ={}
#dictionary to store the term and the number of times of its occurence in the documents
 
idf = {}
#dictionary to store the term and the inverse document frequency

weight = {}
#dictionary to store the term and the weight which is the product of term frequency and inverse document frequency

threshold = 5
#to get the top 5 releveant documents using vector space model, this threshold can be adjusted based on the requirement

wlink = [[0 for x in range (11)] for y in range(11)]
#a two dimentional array to store the connection between the nodes

nodes=[]
#list to store the nodes

outlinks = {}
#dictionary to store the node and the number of outlinks associated to it

inlinks = {}
#dictionary to store the node and the number of inlinks associated to it

rank_weight = {}
#dictionary to store the node and the weight associated to it

in_connecters = {}
#dictionary to store the node and the name of other nodes pointing towards it

out_connecters = {}
#dictionary to store the node and the name of other nodes pointing away from it

def filter( documents, rows, cols ):
    '''function to read and separate the name of the documents and the terms present in it to a separate list  from the data frame and also create a dictionary which 
    has the name of the document as key and the terms present in it as the list of strings  which is the value of the key'''
    
    for i in range( rows ):
        for j in range( cols ):
            #traversal through the data frame

            if( j == 0 ):
                #first column has the name of the document in the csv file
                keys.append( documents.loc[i].iat[j] )
            else:
                dummy_list.append( documents.loc[i].iat[j] )
                #dummy list to update the terms in the dictionary

                if documents.loc[i].iat[j] not in terms:
                    #add the terms to the list if it is not present else continue
                    terms.append( documents.loc[i].iat[j] )

                
        copy = dummy_list.copy()
        #copying the the dummy list to a different list

        dicti.update( { documents.loc[i].iat[0]:copy } )
        #adding the key value pair to a dictionary

        dummy_list.clear()
        #clearing the dummy list


def compute_weight( doc_count, cols ):
    '''Function to compute the weight for each of the terms in the document. Here the weight is calculated with the help of term frequency and 
    inverse document frequency'''

    for i in terms:
        #initially adding all the elements into the dictionary and initialising the values as zero
        if i not in term_freq:
            term_freq.update( { i : 0 } )
    
    for key, value in dicti.items():
        #to get the number of occurence of each terms
        for k in value:
            if k in term_freq:
                term_freq[k] += 1
                #value incremented by one if the term is found in the documents
  
    
    idf = term_freq.copy()
    #copying the term frequency dictionary to a dictionary named idf which is further neede for computation

    for i in term_freq:
        term_freq[i] =  term_freq[i]/cols
        #term frequency is number of occurence divivded by total number of documents
    
    for i in idf:
        if idf[i] != doc_count:
            idf[i] = math.log2( cols/ idf[i])
            #inverse document frequency log of total number of documents divided by number of occurence of the terms
        else:
            idf[i] = 0
            #this is to avoid the zero division error

    for i in idf:
        weight.update({i : idf[i]*term_freq[i]})
        #weight is the product of term frequency and the inverse document frequency

    for i in dicti:
        for j in dicti[i]:
            dummy_list.append(weight[j])
              
        copy = dummy_list.copy()
        vec_dic.update({i:copy})
        dummy_list.clear()
        #above operations performed to get the dictionary of weighted vector for each of the documents

def  get_weight_for_query(query):
    '''function to get the weight for each terms present in the query, here we consider the term frequency as the weight of the terms'''

    query_freq = {}
    #initialisation of the dictionary with query terms as key and its weight as the values
     
    for i in terms:
        #initially adding all the elements into the dictionary and initialising the values as zero
        if i not in query_freq:
            query_freq.update( { i : 0 } )
    
    for val in query:
        #to get the number of occurence of each terms
        if val in query_freq:
                query_freq[val] += 1
                 #value incremented by one if the term is found in the documents
   
    for i in query_freq:
        query_freq[i] =  query_freq[i]/ len(query)
        #term frequency obtained by dividing the number of occurence of terms by total number of terms in the query
    
    return query_freq
    #return the dictionary in which the key is the term and the value is the weight        

def similarity_computation(query_weight):
    ''' Function to calculate the similarity measure in which the weight of the query and the document is multiplied in the numerator and the 
    the weight is squared and squareroot is taken the weights of the query and document'''

    numerator = 0
    denomi1 = 0
    denomi2 = 0
    #initialisation of the variables with zero which is needed for computation

    similarity ={}
    #initialisation of dictionary which has the name of document as key and the similarity measure as value

    for document in dicti:
        for terms in dicti[document]:
            #cosine similarity is calculated

            numerator += weight[terms] * query_weight[terms]
            denomi1 += weight[terms] * weight[terms]
            denomi2 += query_weight[terms] * query_weight[terms]
            #the summation values of the weight is calculated and later they are divided

        if denomi1 !=0  and denomi2 != 0:
            #to avoid the zero division error

            simi = numerator / (math.sqrt(denomi1) * math.sqrt(denomi2))
            similarity.update({document : simi})
            #dictionary is updated

            numerator = 0
            denomi2 = 0
            denomi1 = 0
            #reinitialisation of the variables to zero

    return (similarity)
    #the dictionary containing similarity measure as the value
   

def prediction(similarity,doc_count):
    '''Function to predict the document which is relevant to the query '''

    print("5 most relevant documents\n")
    for i in range(threshold):
    #to print the name of the document which is most relevant    
            
        ans = max( similarity, key = similarity.get)
        #get the document with the highest similarity measure

        print(ans)
        nodes.append(int(ans[-2:]))
        #to print the document name and append it to the list

        similarity.pop(ans)
        #answer is poped from dictionary

def read_weblink_graph():
    ''' function to read the bits which is redirected by a input file and store it in the matrix'''
    #print("Enter the number of rows in a matrix\n")
    n = int(input())
    #n is the number of documents present in the corpus

    for i in range (1,n+1):
        for j in range(1,n+1):
            wlink[i][j]=int(input())
            #input is read and stored in the array


def rank_graph():
    ''' function to calculate the necessary parameters required to rank the documents by considering thier inlinks and outlinks, here the weights associated with each of the page is updated,along
    with that we even find the number of inlinks and outlinks associated with it and update the connection of nodes in the dictionaries named out_connecters
    and in connectors'''
    
    out_count = 0
    in_count = 0
    #initializing the variables to zero

    val = 1.00/len(nodes)
    #initial weight for the nodes is the 1 divided by the number of nodes

    out_connect = []
    in_connect = []
    #declaring the the lists for future operations

    for i in (nodes):
        for j in range(1,11):
            #since there are 10 documents in the corpus

            if( wlink[int(i)][j] == 1 and i!=j ):
                #if there is a outlink (connection from the node to other node) update the necessary parameters
                if( j in nodes):
                    out_count += 1
                    #update the variable outcount
                    out_connect.append(j)
                    #update the dictionary with the name of the node

            if( wlink[j][int(i)] == 1 and i!=j ):
                 #if there is a inlink (connection to the node from other node) update the necessary parameters
                if( j in nodes):
                    in_count += 1
                    #update the variable incount
                    in_connect.append(j)
                    #update the dictionary with the name of the node

        dummy = out_connect.copy()
        #copy the list to a dummy list

        out_connecters.update({i:dummy})
        #update the outconnect list in the dictionary

        out_connect.clear()
        #clear the list
             
        dummy = in_connect.copy()
        #copy the list to a dummy list

        in_connecters.update({i:dummy})
        #update the inconnect list in the dictionary

        in_connect.clear()
        #clear the list
       
        outlinks.update({i:out_count})
        #update the dictionary with the number of outlinks

        inlinks.update({i:in_count})
        #update the dictionary with the number of inlinks
        
        rank_weight.update({i:val})
        #initialise the dictionary with the weights of each of the documents 
        
        out_count = 0
        in_count = 0
        #reinitialise the variables to zero
        
    #print(outlinks)
    #print(inlinks)
    #print(out_connecters)
    #print(rank_weight)
    
def rank_updation():
    '''function to perform the computations which are corresponding to the updation of weights, here the weights of each of the nodes are calculated 
    based on the inlinks and outlinks associated with the documents which are represented as nodes'''

    new_rank = {}
    #initialising a dictionary which is required to perform the operation
    
    iterations = 10
    #a variable required to specify the the of iterations required in rank updation , here we have considered it as 10

    for l in range(iterations):    
        for i in rank_weight:
            #for each of the node present in the dictionary

            val = 0
            #initialising a variable to zero
             
            if( inlinks.get(i) != 0 ):
                #if the node has inlinks connected to it, proceed with the below computations

                for k in in_connecters.get(i):
                    #for each of the nodes pointing towards the node i, calculate the weight

                    val += rank_weight.get(k)/outlinks.get(k)
                    #weight contributed by the other node to node i

                new_rank.update({i:val}) 
                #update the dictionary with the weights of each of the documents      

                val = 0
                #reinitialising a variable to zero

        for i in new_rank:
            rank_weight.update({i:new_rank.get(i)})
            #update the dictionary with the weights of each of the documents afer finishing each of the iteration   
              
        #print(rank_weight,"\n")
    
    ans = max( rank_weight, key = rank_weight.get)
    #obtain the document with the highest rank , and display it to the user

    print("document",ans, "is the most revelevant document")
    #display the most relevant page

def main():
    corpus = pandas.read_csv(r'corpus.csv')
    #to read the data from the csv file as a dataframe

    rows = len( corpus )
    #to get the number of rows

    cols = len( corpus.columns ) 
    #to get the number of columns

    filter( corpus, rows, cols )
    #function call to read and separate the name of the documents and the terms present in it to a separate list  from the data frame and also create a dictionary which 
    #has the name of the document as key and the terms present in it as the list of strings  which is the value of the key

    compute_weight(rows, cols )  
    #Function to compute the weight for each of the terms in the document. Here the weight is calculated with the help of term frequency and 
    #inverse document frequency

    #print("Enter the query")
    query = input()
    #to get the query input from the user, the below input is given for obtaining the output as in output.txt file
    #one three three

    query=query.split(' ')
    #spliting the query as a list of strings
    

    query_weight = get_weight_for_query(query)
    #function call to get the weight for each terms present in the query, here we consider the term frequency as the weight of the terms'''
    
    similarity = similarity_computation(query_weight)
    #Function call to calculate the similarity measure in which the weight of the query and the document is multiplied in the numerator and the 
    #the weight is squared and squareroot is taken the weights of the query and document

    prediction(similarity, rows)
    #Function call to predict the document which is relevant to the query, the top 5 most relevant documents is written to a text file
    
    read_weblink_graph()
    #function call to read the bits which is redirected by a input file and store it in the matrix
    
    rank_graph()
    #function call to calculate the necessary parameters required to rank the documents by considering thier inlinks and outlinks, here the weights associated with each of the page is updated,along
    #with that we even find the number of inlinks and outlinks associated with it and update the connection of nodes in the dictionaries named out_connecters
    #and in connectors

    rank_updation()
    #function call to perform the computations which are corresponding to the updation of weights, here the weights of each of the nodes are calculated 
    #based on the inlinks and outlinks associated with the documents which are represented as nodes


main()
