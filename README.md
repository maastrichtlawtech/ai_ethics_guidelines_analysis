# ai_ethics_guidelines_analysis
This project aims to investigate if features such as the type of issuing organization, the type of funding, the authors' affiliations etc. impact what AI ethical guidelines are written. The long-term plan was to use topic modelling on these documents in order to gain a better idea of what the content of the guidelines are., and to cross-reference that with the types of information mentionned here above. 

Explanation of the current state of the repository: 
1. Our dataset is based on 4 types of objects; documents, organisations, funders and people. In the data folder, one can find :
- the pdf of all AI ethical guidelines documents retrieved 
- the excel files corresponding to the different data tables that have been encoded for these documents. 
    - Documents with columns ['File name (Rx)', 'Original Title','Organization', 'Year', 'Authors','Document funding sources', 'URL','Citation']
    - Organisations : ['name', 'category','country','funder','founder']
    - Funders: ['name','category']
    - People with columns : ['name', 'author_bool', 'founder_bool', 'current_affiliation', 'past_affiliation']
    
 2. The create_dataset.py script was used to create a dataset of the texts from reading the set of pdfs. It creates both a 'raw text' dataset, as well as a lemmatized version of the same documents. 
 
 3. The notebook 'Document_Analysis' aims to give a good overview of the research possibilites offered by this dataset. It makes a first analysis of the different tables, and answers a few possible research questions on how funding categories and author affiliations are distributed in our dataset. 
 
 4. The notebook 'Topic Modelling' contains all the topic modelling methods that we tried on our set of documents. 
