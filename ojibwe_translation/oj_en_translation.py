"""
    Abstract functions of Objiwe -> English translations
    Will analyze the verb type (VTA/VTI/VAI/VII) and call appropriate functions
"""
import copy
from ojibwe_translation.oj_translation_core import *
from ojibwe_translation.oj_constants import *
from ojibwe_translation.vta import *
from ojibwe_translation.vti import *
from ojibwe_translation.vai import *
from ojibwe_translation.vii import *


def initialize_environment(data_path: str):
    """
    Initialize core environment.

    Parameters
    ----------
    data_path : str, optional
        Path to the data folder, by default DATA_FOLDER.

    Returns
    -------
    dict
        Dictionary object core environment.
    """
    environment = copy.deepcopy(CORE_ENVIRONMENT)
    environment[ENV_DATA_PATH] = data_path
    return environment
    
def load_foma(environment: dict, file_name : str) -> dict:
    """
    Load FST Parser.

    Parameters
    ----------
    environment : dict
        Environment dict object
    file_name : str
        path to the fomabin (.att) file, relative to environment data folder

    Returns
    -------
    dict
        Updated environment JSON object with the fst attribute.
    """
    try:
        path = environment[ENV_DATA_PATH] + file_name
        fst = load_fst_parser(path)
        environment[ENV_FST] = fst
        return environment
    except ValueError as e:
        logger.debug("Error loading the FST parser.")
        raise e

def load_templates(environment: dict, filenames:dict=TEMPLATES_FILENAMES) -> dict:

    """
    Load dictionary templates.

    Parameters
    ----------
    environment : dict
        Environment JSON object
    filenames : list of str, optional
        Full path to the dictionary files (dict format), by default TEMPLATES_FILENAMES.

    Returns
    -------
    dict
        Updated environment object with "vta_dict_df", "vti_dict_df", "vai_dict_df", "vii_dict_df" attributes.
    """
    try:
        path = environment[ENV_DATA_PATH]
        logger.debug(f"Loading generic dictionary ...")
        environment[ENV_ALL_DICTIONARY_DF] = load_dictionary_templates(path + filenames[ENV_ALL_DICTIONARY_DF])

        logger.debug(f"Loading {FST_VTA} templates...")
        environment[ENV_VTA_DICTIONARY_DF] = load_dictionary_templates(path + filenames[ENV_VTA_DICTIONARY_DF])

        logger.debug(f"Loading {FST_VTI} templates...")
        environment[ENV_VTI_DICTIONARY_DF] = load_dictionary_templates(path + filenames[ENV_VTI_DICTIONARY_DF])
        
        logger.debug(f"Loading {FST_VAI} templates...")
        environment[ENV_VAI_DICTIONARY_DF] = load_dictionary_templates(path + filenames[ENV_VAI_DICTIONARY_DF])
        
        logger.debug(f"Loading {FST_VII} templates...")
        environment[ENV_VII_DICTIONARY_DF] = load_dictionary_templates(path + filenames[ENV_VII_DICTIONARY_DF])
        
        return environment
    except Exception as e:
        logger.debug("Error loading dictionary templates. Error =", e)
        return environment


def fst_verb_analyzer(fst_analysis_string: str) -> dict:
    """
    Analyze the inflected Ojibwe verb, based on paradigm (VTA/VTI, etc) and order (independence / imperative / conjunction).

    Parameters
    ----------
    fst_analysis_string : str
        Parsed FST string of a verb, e.g. "waabam+VTA+Pos+Neu3SgProx+1S".

    Returns
    -------
    dict
        JSON object dictionary with keys "verb", "verb_type", "subject", and "object".
    """
    fst_analysis_string = fst_analysis_string.lower()
    if f"+{FST_VTA}" in fst_analysis_string:
        return fst_vta_verb_analyzer(fst_analysis_string)
    elif f"+{FST_VTI}" in fst_analysis_string:
        return fst_vti_verb_analyzer(fst_analysis_string)
    elif f"+{FST_VAI}" in fst_analysis_string:
        return fst_vai_verb_analyzer(fst_analysis_string)
    elif f"+{FST_VII}" in fst_analysis_string:
        return fst_vii_verb_analyzer(fst_analysis_string)
    else:
        # not a valid verb
        return [{OUTPUT_INPUT: inflected_ojibwe_word,
                 OUTPUT_FST_OUTPUT: fst_output,
                 OUTPUT_ERROR: OUTPUT_ERROR_NOT_VERB
                }]

def build_en_sentence(sentence_structure: dict, environment: dict) -> list:
    """
    Build an English sentence based on the sentence structure.

    Parameters
    ----------
    sentence_structure : dict
        Dictionary containing FST tags, e.g. {'verb': 'waabam', 'verb_type': 'VTA', 'subject': '3SgProx', 'object': '1Sg'}.
    environment : dict
        Environment JSON object that contains templates.

    Returns
    -------
    list of str
        A list of alternative English sentences.
    """
    logger.debug(f"FST tags = {sentence_structure}")
    if FST_VTA in sentence_structure.get(VERB_TYPE, ""):
        return vta_build_en_sentence(sentence_structure, environment[ENV_VTA_DICTIONARY_DF])
    elif FST_VTI in sentence_structure.get(VERB_TYPE, ""):
        return vti_build_en_sentence(sentence_structure, environment[ENV_VTI_DICTIONARY_DF])
    elif FST_VAI in sentence_structure.get(VERB_TYPE, ""):
        return vai_build_en_sentence(sentence_structure, environment[ENV_VAI_DICTIONARY_DF])
    elif FST_VII in sentence_structure.get(VERB_TYPE, ""):
        return vai_build_en_sentence(sentence_structure, environment[ENV_VII_DICTIONARY_DF])
    else:
        # not a valid verb
        # return None 
        return [{OUTPUT_INPUT: inflected_ojibwe_word,
                 OUTPUT_FST_OUTPUT: fst_output,
                 OUTPUT_ERROR: OUTPUT_ERROR_NOT_VERB
                }]

def _bipartite_check(negation_token:str, fst_analysis_string:str) -> str:
    """ Check if the negation token (gaawiin / gego ) matches with the FST analysis string
        Return a message (str)
    """
    result = ""
    
    # first case: "gaawiin x" with verb in Independence order and Negative polarity
    if negation_token.lower().strip() == GAAWIIN_TOKEN and \
        f"+{FST_ORDER_INDEPENDENCE}" in fst_analysis_string and \
            f"+{FST_POLARITY_NEGATIVE}" in fst_analysis_string:
                return "" 
    
    # first case: "gaawiin x" with verb in Independence order and Negative polarity
    if negation_token.lower().strip() == GEGO_TOKEN and \
        f"+{FST_MODE_PROHIBITIVE}" in fst_analysis_string:
                return "" 
            
    # check if the negation token is required 
    if (f"+{FST_ORDER_INDEPENDENCE}" in fst_analysis_string and \
        f"+{FST_POLARITY_NEGATIVE}" in fst_analysis_string) and \
        negation_token.lower() != GAAWIIN_TOKEN:
            return OUTPUT_MESSAGE_BIPARTITE_NEGATION_MISSING.replace(BIPARTITE_TOKEN_SLOT, f"'{GAAWIIN_TOKEN}'")

    if (f"+{FST_MODE_PROHIBITIVE}" in fst_analysis_string) and \
        negation_token.lower() != GEGO_TOKEN:
            return OUTPUT_MESSAGE_BIPARTITE_NEGATION_MISSING.replace(BIPARTITE_TOKEN_SLOT, f"'{GEGO_TOKEN}'")
    
    return result 

def oj2en_builder(inflected_ojibwe_word: str, environment: dict) -> list[dict]:
    """
    Simple sentence builder from an Ojibwe verb to an English sentence.

    Parameters
    ----------
    inflected_ojibwe_word : str
        Ojibwe word, e.g. 'niwaabamig'.
    environment : dict
        Environment JSON object that contains FST parser and templates dataframes.

    Returns
    -------
    list of dict
        list of translation results, each contains the input, definition, translation, etc
        [{"input":, "fst_output":, "sentence_structure":, "translation":},]
    """
    result = None    
    inflected_ojibwe_word = inflected_ojibwe_word.strip().lower()
    
    # special case (bipartite negation), e.g. I don't sleep = "gaawiin ninibaasii" instead of just "ninibaasii"
    # the special token "gaawiin" is required for **independent** order and **negative** polarity
    # similarly, the token "gego" is required for **prohibitive imperative** (e.g.  "gego nibaaken" -> "do not sleep")
    if inflected_ojibwe_word.split()[0].strip() in [GAAWIIN_TOKEN, GEGO_TOKEN]:
        # save the token to be checked later, and continue with the rest of the word
        negation_pre_word = inflected_ojibwe_word.split()[0].strip()
        inflected_ojibwe_word = " ".join(inflected_ojibwe_word.split()[1:]) 
    else:
        negation_pre_word = ""
    
    # parse the word
    if environment[ENV_FST] is None:
        return [{OUTPUT_INPUT: inflected_ojibwe_word,
                 OUTPUT_ERROR: OUTPUT_ERROR_FOMA_NOT_FOUND
               }]
        
    fst_output = inflected_ojibwe_word_process_inflected_form(inflected_ojibwe_word, fst=environment[ENV_FST])
    logger.debug(f"FST tags = {fst_output}")
    
    if fst_output is None or len(fst_output) == 0:
        return [{OUTPUT_INPUT: inflected_ojibwe_word,
                 OUTPUT_ERROR: OUTPUT_ERROR_FST_PARSE
                }]

    fst_output = fst_output[0].lower()


    if f"+{FST_VTA}" in fst_output:
        result = vta_oj2en_builder(inflected_ojibwe_word=inflected_ojibwe_word, core_environment=environment)
    elif f"+{FST_VTI}" in fst_output:
        result = vti_oj2en_builder(inflected_ojibwe_word=inflected_ojibwe_word, core_environment=environment)
    elif f"+{FST_VAI}" in fst_output:
        result = vai_oj2en_builder(inflected_ojibwe_word=inflected_ojibwe_word, core_environment=environment)
    
    elif f"+{FST_VII}" in fst_output:
        result = vii_oj2en_builder(inflected_ojibwe_word=inflected_ojibwe_word, core_environment=environment)
    else:
        # invalid verb
        result = [{OUTPUT_INPUT: inflected_ojibwe_word,
                 OUTPUT_FST_OUTPUT: fst_output,
                 OUTPUT_ERROR: OUTPUT_ERROR_NOT_VERB
                }]
        
    # check if the negation token (gaawiin / gego) matches with the FST analysis string
    bipartite_message =  _bipartite_check(negation_token=negation_pre_word, fst_analysis_string=fst_output)

    if bipartite_message != "" and len(result) > 0:
        for item in result:
            item[OUTPUT_MESSAGE] = bipartite_message 
        
    return result 

    