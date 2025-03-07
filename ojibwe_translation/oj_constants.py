"""
    Frequently used constant values in Ojibwe - English translation
"""
### ========= DATA COLUMNS ========= ### 
DATA_LEMMA = "lemma"
DATA_DEFINITION = "definition"
DATA_VERBS = "verbs"
DATA_TEMPLATES = "templates"
DATA_LLM_TEMPLATES = "llm_templates"

### ========= OUTPUT FORMAT ========= ### 
OUTPUT_ERROR = "error"
OUTPUT_INPUT = "input"
OUTPUT_MESSAGE = "message"
OUTPUT_FST_OUTPUT = "fst_output"
OUTPUT_DEFINITION = "definition"
OUTPUT_SENT_STRUCTURE = "sentence_structure"
OUTPUT_TRANSLATION ="translation"
OUTPUT_ERROR_FOMA_NOT_FOUND = "FST Parser not found. Please load FST parser first using load_foma() function."
OUTPUT_ERROR_FST_PARSE = "FST parse error. Likely not valid Ojibwe verb, or verb not in FST dictionary."
OUTPUT_ERROR_SENTENCE_STRUCTURE = "Sentence structure error. Invalid FST parsed output."
OUTPUT_ERROR_LEMMA_NOT_FOUND = "Lemma not found in dictionary / templates data source"
OUTPUT_ERROR_NOT_VERB = "The input is likely not an Ojibwe verb. Please double check."
BIPARTITE_TOKEN_SLOT = "{{TOKEN}}"
OUTPUT_MESSAGE_BIPARTITE_NEGATION_MISSING = f"Please add {BIPARTITE_TOKEN_SLOT} before the word to make a more grammatical sentence."

### ========= FST Parser CONSTANTS ========= ### 
FST_SEPARATOR = "+"
FST_TENSE_PREFIX = "pvtense" 
FST_TENSE_SEPARATOR = "/"
FST_ORDER_CONJUNCTION = "cnj"
FST_ORDER_IMPERATIVE = "imp"
FST_ORDER_INDEPENDENCE = "ind"
FST_MODE_PRETERIT = "prt"
FST_MODE_DUBITATIVE = "dub"
FST_MODE_PROHIBITIVE = "prb"
FST_MODE_DELAYED = "del"
FST_MODE_NEUTRAL = "neu"

FST_VTA = "vta"
FST_VTI = "vti"
FST_VAI = "vai"
FST_VII = "vii"

FST_POLARITY_POSITIVE = "pos"
FST_POLARITY_NEGATIVE = "neg"

FST_TENSE_GII = "gii"
FST_TENSE_GA = "ga"
FST_TENSE_DA = "da"
FST_TENSE_WII = "wii"

### ========= SENTENCE STRUCTURE CONSTANTS ========= ### 
SUBJECT = "subject"
OBJECT = "object"
SUBJ = "subj"
OBJ = "obj"
VERB_LEMMA = "verb"
VERB_TYPE = "verb_type"
TENSE = "tense"
ORDER = "order"
MODE = "mode"
POLARITY = "polarity"
TO_BE_VERB = "be"

### ========= INFLECTION CONSTANTS ========= ### 
INFLECT_VBN = "VBN"   # pefect, e.g. see -> seen
INFLECT_VBZ = "VBZ"   # 3rd singular, e.g. want -> wants
INFLECT_VBD = "VBD"   # past tense, e.g. want -> wanted

### ========= TRANSLATION CONSTANTS ========= ### 
TRANSLATION_CONJ_PREFIX = "If/when"
TRANSLATION_IMP_PREFIX = "(Please)"
TRANSLATION_IMP_DELAYED_AFFIX = "later"
TRANSLATION_ONESELF = "oneself"
TRANSLATION_ONE_POSSESSIVE = "one's"

### ========= CORE TRANSLATION MAPPING CONSTANTS ========= ### 
# define tense-mapping
TENSE_PAST = "past"
TENSE_FUTURE = "future"
TENSE_FUTURE_WILL = "future/will"
TENSE_FUTURE_WISH = "future/wish"
TENSE_FUTURE_GOING = "future/going"

TENSE_MAPPING = {
    FST_TENSE_GII: TENSE_PAST,
    FST_TENSE_GA: TENSE_FUTURE_WILL,
    FST_TENSE_DA: TENSE_FUTURE_WILL,
    FST_TENSE_WII: TENSE_FUTURE_WISH,
}

# keyword for tense in fst tags


# special-case subject and object tags
SUBJ_1SG = "1sg"
SUBJ_3SG = "3sg"
SUBJ_0SG = "0sg"

OBJ_1SG = "1sgobj"
OBJ_3SG = "3sgobj"
OBJ_0SG = "0sgobj"


XSUBJ = "xsubj"
XOBJ = "xobj"

X3SG_SUBJ = "3sgxsubj"
X3SG_OBJ = "3sgxobj"

PROXIMATE_TAG = "proximate"
OBVIATIVE_TAG = "obviative"
INANIMATE_TAG = "inanimate"

# define subjects and objects
EN_SUBJECTS = {
    "0sgsubj" : f"it ({INANIMATE_TAG})",    # inanimate singular subject for VII
    "0plsubj" : f"they ({INANIMATE_TAG})",  # inanimate plural subject for VII
    "0sgobvsubj": f"it ({INANIMATE_TAG}, {OBVIATIVE_TAG})",
    "0plobvsubj": f"they ({INANIMATE_TAG}, {OBVIATIVE_TAG})",
    "1sgsubj" : "I",
    "2sgsubj" : "you",
    "2plsubj" : "you (all)",
    "3sgsubj" : "he/she",
    "3plsubj" : "they",
    "3sgproxsubj": f"he/she ({PROXIMATE_TAG})",
    "3sgobvsubj" : f"he/she ({OBVIATIVE_TAG})",
    "3plproxsubj": f"they ({PROXIMATE_TAG})",
    "3plobvsubj" : f"they ({OBVIATIVE_TAG})",
    "inclsubj": "we (inclusive)",
    "exclsubj": "we (exclusive)",
    "3sgxsubj": "(someone)", 
}

# define to be verb, present tense
TOBE_SUBJ_PRESENT = {
    "0sgsubj" : "is",
    "0plsubj" : "are",
    "1sgsubj" : "am",
    "1plsubj" : "are",
    "2sgsubj" : "are",
    "2plsubj" : "are",
    "3sgsubj" : "is",
    "3plsubj" : "are",
    "3sgproxsubj": "is",
    "3sgobvsubj" : "is",
    "3plproxsubj": "are",
    "3plobvsubj" : "are",
    "inclsubj": "are",
    "exclsubj": "are",
    "3sgxsubj": "are", 
}

TOBE_SUBJ_PAST = {
    "0sgsubj" : "was",
    "0plsubj" : "were",
    "1sgsubj" : "was",
    "1plsubj" : "were",
    "2sgsubj" : "were",
    "2plsubj" : "were",
    "3sgsubj" : "was",
    "3plsubj" : "were",
    "3sgproxsubj": "was",
    "3sgobvsubj" : "was",
    "3plproxsubj": "were",
    "3plobvsubj" : "were",
    "inclsubj": "were",
    "exclsubj": "were",
    "3sgxsubj": "was", 
}

SUBJ_POSSESSIVE = {
    "0sgsubj" : "its",
    "0plsubj" : "their",  
    "0sgobvsubj": f"its ({OBVIATIVE_TAG})",
    "0plobvsubj": f"their ({OBVIATIVE_TAG})",
    "1sgsubj" : "my",
    "2sgsubj" : "your",
    "2plsubj" : "your",
    "3sgsubj" : "his/her/its",
    "3plsubj" : "their",
    "3sgproxsubj": f"his/her ({PROXIMATE_TAG})",
    "3sgobvsubj" : f"his/her ({OBVIATIVE_TAG})",
    "3plproxsubj": f"their ({PROXIMATE_TAG})",
    "3plobvsubj" : f"their ({OBVIATIVE_TAG})",
    "inclsubj": "our",
    "exclsubj": "our",
    "3sgxsubj": "(their)", 
}

OBJ_POSSESSIVE = {
    "0sgobj" : "its",
    "0plobj" : "their",  
    "0sgobvobj": f"its ({OBVIATIVE_TAG})",
    "0plobvobj": f"their ({OBVIATIVE_TAG})",
    "1sgobj" : "my",
    "2sgobj" : "your",
    "2plobj" : "your",
    "3sgobj" : "his/her/its",
    "3plobj" : "their",
    "3sgproxobj": f"his/her ({PROXIMATE_TAG})",
    "3sgobvobj" : f"his/her ({OBVIATIVE_TAG})",
    "3plproxobj": f"their ({PROXIMATE_TAG})",
    "3plobvobj" : f"their ({OBVIATIVE_TAG})",
    "inclobj": "our",
    "exclobj": "our",
    "3sgxobj": "(their)", 
}

SUBJ_REFLEXIVE = {
    "0sgsubj" : "itself",
    "0plsubj" : "themselves",  
    "0sgobvsubj": f"itself ({OBVIATIVE_TAG})",
    "0plobvsubj": f"themselves ({OBVIATIVE_TAG})",
    "1sgsubj" : "myself",
    "2sgsubj" : "yourself",
    "2plsubj" : "yourselves",
    "3sgsubj" : "him/her/it-self",
    "3plsubj" : "themselves",
    "3sgproxsubj": f"him/her/it-self ({PROXIMATE_TAG})",
    "3sgobvsubj" : f"him/her/it-self ({OBVIATIVE_TAG})",
    "3plproxsubj": f"themselves ({PROXIMATE_TAG})",
    "3plobvsubj" : f"themselves ({OBVIATIVE_TAG})",
    "inclsubj": "ourselves",
    "exclsubj": "ourselves",
    "3sgxsubj": "(themselves)", 
}


EN_OBJECTS = {
    "0sgobj" : "it",    # inanimate singular object
    "0plobj" : "them",  # inanimate plural object
    "1sgobj" : "me",
    "1plobj" : "us",
    "2sgobj" : "you",
    "2plobj" : "you (all)",
    "3sgobj" : "him/her/it",
    "3sgproxobj": f"him/her/it ({PROXIMATE_TAG})",
    "3sgobvobj": f"him/her/it ({OBVIATIVE_TAG})",
    "3plproxobj": f"them ({PROXIMATE_TAG})",
    "3plobj" : "them",
    "3plobvobj": f"them ({OBVIATIVE_TAG})",
    "inclobj": "us (inclusive)",
    "exclobj": "us (exclusive)",
    "3sgxobj": "(something animate)",
    "nullobj": ""  # null object for VAI/VII
}

SUBJECT_SLOT = "{{subject}}"
OBJECT_SLOT = "{{object}}"
OBJECT_POSSESSIVE_SLOT = "{{object-possessive}}"

### ========= VTA/VTI CONSTANTS ========= ### 
# define structure of standard Independence VTA FST output
# e.g niwaabamig = "waabam+VTA+Ind+Pos+Neu+3SgProxSubj+1SgObj"
VTA_STRUCTURE = {VERB_LEMMA:0, 
                 VERB_TYPE:1,
                 ORDER:2,
                 POLARITY:3,
                 MODE:4,
                 SUBJECT:5,
                 OBJECT:6
                }


# define structure of VTA FST with Imperative mode 
# (e.g. "Close the door", which has different structure than normal VTA)
# jekibiinik -> jekibiin+VTA+Imp+Sim+2PlSubj+3SgProxObj
VTA_IMP_STRUCTURE = {VERB_LEMMA:0, 
                      VERB_TYPE:1,
                      ORDER:2,
                      MODE:3,
                      SUBJECT:4,
                      OBJECT:5
                     }


# define structure of VTA FST with Conjuction mode 
# example: jekibiin +VTA +Cnj +Pos +Neu +3SgProx +2Sg
# it's enssentially the same as Independence order
VTA_CONJ_STRUCTURE = {VERB_LEMMA:0, 
                      VERB_TYPE:1,
                      ORDER:2,
                      POLARITY:3,
                      MODE:4,
                      SUBJECT:5,
                      OBJECT:6
                     }

# default sentence structure values 
DEFAULT_ORDER = "ind"    # independence order
DEFAULT_NEGATION = "pos" # positive
DEFAULT_MODE = "neu"     # neutral mode
DEFAULT_TENSE = ""       # present tense

### ========= VAI/VII CONSTANTS ========= ### 
NULL_OBJ_TAG = "+nullObj"   # null object adding to VAI and VII for structure compatibility


OBJ_INTRANSITIVE_SLOT = "{{object-intransitive}}"  # handle subject becomes object, e.g. in VAI verbs

VAI_STRUCTURE = {VERB_LEMMA:0, 
                  VERB_TYPE:1,
                  ORDER:2,
                  POLARITY:3,
                  MODE:4,
                  SUBJECT:5,
                  OBJECT:6
                 }


VAI_IMP_STRUCTURE = {VERB_LEMMA:0, 
                      VERB_TYPE:1,
                      ORDER:2,
                      MODE:3,
                      SUBJECT:4,
                      OBJECT:5
                     }


VAI_CONJ_STRUCTURE = {VERB_LEMMA:0, 
                      VERB_TYPE:1,
                      ORDER:2,
                      POLARITY:3,
                      MODE:4,
                      SUBJECT:5,
                      OBJECT:6
                     }


EXISTENCE_PREFIX = "there be "

### ========= DATA CONSTANTS ========= ### 
# core environment object, contains essential objects (FST parser, templates, etc)
# DATA_FOLDER = "./tests/data/"
# DEFAULT_FOMABIN_PATH = "foma_bin/ojibwe.fomabin"

ENV_DATA_PATH = "data_folder_path"
ENV_FST = "fst"
ENV_ALL_DICTIONARY_DF = "all_dict_df"
ENV_ALL_DICTIONARY_SUFFFIX = "all"
ENV_VTA_DICTIONARY_DF = "vta_dict_df"
ENV_VTI_DICTIONARY_DF = "vti_dict_df"
ENV_VAI_DICTIONARY_DF = "vai_dict_df"
ENV_VII_DICTIONARY_DF = "vii_dict_df"

# empty core environment values for initialization
CORE_ENVIRONMENT = {
    ENV_DATA_PATH: "",
    ENV_FST: None,
    ENV_ALL_DICTIONARY_DF: None,
    ENV_VTA_DICTIONARY_DF: None,
    ENV_VTI_DICTIONARY_DF: None,
    ENV_VAI_DICTIONARY_DF: None,
    ENV_VII_DICTIONARY_DF: None,
}


TEMPLATES_FILENAMES = {
    ENV_ALL_DICTIONARY_DF: "templates/ob_en_dict.csv",
    ENV_VTA_DICTIONARY_DF: "templates/vta_dict.csv",
    ENV_VTI_DICTIONARY_DF: "templates/vti_dict.csv",
    ENV_VAI_DICTIONARY_DF: "templates/vai_dict.csv",
    ENV_VII_DICTIONARY_DF: "templates/vii_dict.csv",
    
}


# PRE-WORD TOKEN FOR BIPARTITE NEGATION
# "gawiin" (pre-word) is required for independence order and negative polarity, e.g. "gaawiin ninibaasii" -> "I do not sleep" 
GAAWIIN_TOKEN = "gaawiin" 
# "gego" (pre-word) is required for Prohibitive imperative, e.g. "gego nibaaken" -> "do not sleep"
GEGO_TOKEN = "gego"       