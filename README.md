# search_engine

This repositary consists of the implementation of the search engine, initially we obtain the 5 most relevant documents by making use of the vector space model later by making use of 
the weblinks we apply the page rank algorithm and decide the most important page by making use of the ranks.

The repositary consists of the python program named search_eng.py, the input and output text files which contains the input which is redirected to the program and output obtained 
from the program.It also contains the graph of original weblinks and also of top 5 most relevant documents in the png format.The csv file which is given as the corpus to the program,
it contains the document name and the index terms present in it.

Information retrieval (IR) is finding material (usually documents) of an unstructured nature, that satisfies an information need from within large collections.The retrieval in this 
type of model is accomplished by assigning non-binary weights to index terms in queries and documents .These term weights are ultimately used to compute the degree of similarity 
between each document stored in the system and the user query.

The query and the documents are represented in the form of vectors and the similarity is calculated based on the cosine of angle between these two vectors.Tf-idf schemes is used for 
the weight calculation which term frequency and inverse document frequency.Here the term frequency means the ratio number of times the particular term occurs in the document to the 
maximum occurrence of the term, and the inverse document frequency is the log of ratio of total number of documents to the documents containing the particular term.the weight 
calculated is the product of the term frequency and inverse document frequency.

Initially we read and separate the name of the documents and the terms present in it to a separate list from the data frame and also create a dictionary which has the name of the 
document as key and the terms present in it as the list of strings which is the value of the key ,later we compute the weight for each of the terms in the document. Here the weight 
is calculated with the help of term frequency and inverse document frequency. Once we get the query input from the user, we split the query as a list of strings and get the weight 
for each terms present in the query, here we consider the term frequency as the weight of the terms and then we calculate the similarity measure in which the weight of the query and 
the document is multiplied in the numerator and the weight is squared and squareroot is taken the weights of the query and document. Finally prediction is made regarding the document 
which is relevant.

The program is concerned with the calculation of page rank values for each of the page and then updating them.Initially the input for the program is the matrix which consists of the 
link between the nodes.Finally we obtain the page which is most important with help of the ranks which are assigned to them.The concept behind the implementation is as follows.
Intuitively, we can think of PageRank as a kind of “ﬂuid” that circulates through the network, passing from node to node across edges, and pooling at the nodes that are the most 
important. Speciﬁcally, PageRank is computed as follows.

• In a network with n nodes, we assign all nodes the same initial PageRank, set to be 1/n. • We choose a number of steps k. 
• We then perform a sequence of k updates to the PageRank values, using the following rule for each update:

Basic PageRank Update Rule: Each page divides its current PageRank equally across its out-going links, and passes these equal shares to the pages it points to. (If a page has no out-
going links, it passes all its current PageRank to itself.) Each page updates its new PageRank to be the sum of the shares it receives.

Reference:
Modern information retrieval by Ricardo Baeza-Yates, Berthier Ribeiro-Neto
Networks, Crowds, and Markets Reasoning About a Highly Connected World by David Easley, Jon Kleinberg
