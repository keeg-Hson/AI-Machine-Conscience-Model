# Symbolic Index
#-----PURPOSE:-----#

#Deals with the handling of symbolic tagging system of memory entries
#enables associated retrieval based off of symbolic tags
##EX: "mirror" could be a symbolic tag, which would be associated with all entries that contain the word "mirror"
###"mirror", "sunset", "ocean", "rebirth", "ideal" - All bare similar relevance here, all of these posing as symbolic tag hypotheticals to work with for testing and debugging purposes
#to also support future ontologically based semantic expression

#-----FUNCTIONS:-----#
#1.1 Symbolic indexing
#to act as a sort of temporary memory based mapping mechanism
#will act as a sort of 'lookup table' for later reference
##ex: {symbol->list of entry_ids}

#1.2 LOOKUP TABLE FUNCTIONALITY:
SYMBOLIC_INDEX={} #EXAMPLE OUTPUT: {'ideal': ['entry_id_1', 'entry_id_2'], 'mirror': ['entry_id_3', 'entry_id_4']}


#2. entry tagging
def tag_entry(entry_id:str, symbols:list):
    """
    Appends associated symbolic tags to each entry ID to our index
    -to be called by out *vault_core* when a new entry is recorded/created

    -EXAMPLE-
    for symbol in symbols:
        if symbol not in inedx:
            create an empty list  
            append given entry_id into this list

    -OPTIONAL-
    -could also be used to remove tags from entries (REMOVAL OF DUPLICATES) **THIS IS ACTUALLY CRUCIAL!!!*** (WITH URGENT LOVE OBV)

    """


#3. SYMBOLIC EXTRACTION LOGIC

def find_symbolic_associations(text:str) -> list:
    """
    PURPOSE:
    -----------

    -Analysis of given input text (in form of 'str' variable valulation atm) 
    and returns a list of associated symbols/symbolic tags

    -will utilize basis keyword matching for now
    --FUTURE RENDITION: ontology/embedding model would be highly ideal for this use case!

    -----------

    """
    extracted_symbols=[] #list of extracted symbols: will pose as our customizable empty list to be added to as per users needs


    """
    -----------
    ADDITIONAL:
    -----------
    -check for known keywords/imagery within given user entry in question, 
    which will then be mapped out further into symbolic representations

    -EXAMPLES:-
    -----------
    'mirror' -> ['reflection', 'self-discovery']
    'sunset' -> ['endings', 'transitions']
    'ocean' -> ['depth', 'vastness']
    'childhood' -> ['innocence', 'nostalgia', 'inner child']
    -----------

    
    """
    return extracted_symbols #returns list of symbolic tags associated with given user input

#--------OPTIONAL--------#
#Step 4: retrieval of entries by symbolic valuation
def get_entries_by_symbol(symbol:str, max_results:int=5) -> list:
    """
    -to return entry IDs that are associated with a given keyword (Symbolic tag? TBD)
    -can be utilized by either vault_core.py og exteranally if desired

    
    """
    if symbol in SYMBOLIC_INDEX():
        return SYMBOLIC_INDEX[symbol][:max_results]
    #else: #idk if this will be necessary considering the given functionality at play here but whatever
        return [] #nonreachable, "ELSE" here might be necessary? idek
    