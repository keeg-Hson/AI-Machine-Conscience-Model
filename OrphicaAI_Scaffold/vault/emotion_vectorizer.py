# Emotion Vectorizer

#The ultimate purpose of this file is to access text based inputs and to return a dictionary. 
#this stored dcitionary willserve as a subset that scans the overall 'emotional tone' associated with each given user entry

#Output:
##will append dict classification, with an associated score (0-1) for each emotional category (closer to 1; higher user importance)
###example: {contentment: 0.8, distress: 0.2, etc...}

######-----STEPS-----#######
#1. Import necessary libraries
##kinda goes without saying lel

#2. define emotional categories: 
##to form basis of 'emotional vector' space
##categories to be pre defined here
###append values as necessary

EMOTION_CATEGORIES = [ #temporary placeholder for emotional categories
    "contentment",
    "distress",
    "anger",
    "fear",
    "sadness",
    "joy",
    "surprise",
    "disgust"
]

#3. placeholder emotional keyword dict
##to be replaced with actual ML logic later on!
##for prototyping purposes, we will define a preset array of keywords associated with each emotional category
EMOTION_KEYWORDS={ #"EMOTION_LABEL": ["WROD1", "WORD2", "WORD3", ...]
    
    #EXAMPLES:
    "contentment": ["happy", "satisfied", "pleased"],
    "distress": ["sad", "unhappy", "displeased"],
    "anger": ["angry", "furious", "mad"],
    "fear": ["scared", "afraid", "terrified"],
    "sadness": ["depressed", "down", "blue"],
    "joy": ["joyful", "elated", "cheerful"],
    "surprise": ["shocked", "astonished", "amazed"],
    "grief": ["loss", "death", "cry", "funeral"],
    "anticipation": ["excited", "eager", "hopeful"],
    "disgust": ["disgusted", "repulsed", "nauseated"]

}

#4. processing logic
def preprocess(text:str)->str:
    """
    to serve purpose of cleaning up text inputs. 
    deals with normalization, lowercasing, and preparing text entires for further processing
    """

    return cleaned_text #to be defined later on: will effectively be  our final cleared up outputs


#5. emotional processing logic
def classify_emotions(text:str) -> dict:
    """
    to serve purpose of classifying emotional tone of user input. to return a dictionaly of detected user emotions along with their associated weight scores
    ex: {contentment: 0.8, distress: 0.2, etc...} 
    #all summate to 1.0, or at least should in theory.
    """

    text = preproccess(text) #preprocess to be defined here

    emotion_scores={ #initializes or dictionary for results

    #for each emotional category: 
    #search for presence of keywords/patterns in text contents
    #if matched:
    ##increase score of that specific emotion   

    #OPTIONAL: normalize scores, so that they cumulatively summate to 1.0

    } 

    return emotion_scores #returns dictionary of emotional scores, as per the user input

#Step 6: intensity estimation:
def estimate_intensity(text:str) -> float:
    """ 
    placeholder function for future use: poses as an estimator for how emotionally 'intense' a a given entry is.
    #to be used fro adjusting memory salience factor

    #IDEAS#
    -concerning user input, classification factors could be based off of 
    exclamations, repetition, strong word densities as far as idea importance/reinforcement patterns are concerned, 
    even word capitalization (etc etc etc.).... 
    """
    return intensity_score #returns valuation between 0.0 and 1.0 (TO BE DEFINED!)


    