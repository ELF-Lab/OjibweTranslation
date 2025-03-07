"""
    Structures and functions to translate VTI (Transitive, Inanimate) verbs to English.
    Because VTA (Transitive, Animate) are very similar to VTI, 
    the VTI functions will mainly be wrapper functions to call VTA functions
"""
from ojibwe_translation.oj_translation_core import *
from ojibwe_translation.vta import *

def fst_vti_normal_analyzer(fst_analysis_string:str, sentence_structure:dict=VTA_STRUCTURE)->dict:
    """
    VTI wrapper function that calls the VTA function to parse FST tags to a JSON object (dictionary) for normal (independent) VTI verb.

    Parameters
    ----------
    fst_analysis_string : str
        FST string of a verb, e.g., "waabam+VTA+Pos+Neu3SgProx+1S".
    sentence_structure : dict, optional
        Structure of the VTA foma output (default is VTA_STRUCTURE).

    Returns
    -------
    dict
        Dictionary object containing {"verb", "verb_type", "subject", "object"}.
    """
    return fst_vta_normal_analyzer(fst_analysis_string, sentence_structure)
    



def fst_vti_imp_analyzer(fst_analysis_string:str, sentence_structure:dict=VTA_IMP_STRUCTURE)->dict:
    """
    VTI wrapper function that calls the VTA function to parse FST tags to a JSON object (dictionary) for Imperative VTA verb.

    Parameters
    ----------
    fst_analysis_string : str
        FST string of a verb, e.g., "jekibiin+VTA+Imp+Sim+2SgSubj+3SgProxObj".
    sentence_structure : dict, optional
        Structure of the VTA foma output (default is VTA_IMP_STRUCTURE).

    Returns
    -------
    dict
        JSON dictionary containing {"verb", "verb_type", "subject", "object"}.
    """
    return fst_vta_imp_analyzer(fst_analysis_string, sentence_structure)



def fst_vti_verb_analyzer(fst_analysis_string:str, vta_structure:dict=VTA_STRUCTURE, vta_imp_structure:dict=VTA_IMP_STRUCTURE)->dict:
    """
    VTI wrapper function that calls the VTA function to analyze the VTA verb based on order (independence / imperative / conjunction).

    Parameters
    ----------
    fst_analysis_string : str
        FST string of a verb, e.g., "waabam+VTA+Pos+Neu3SgProx+1S".
    vta_structure : dict, optional
        Structure of the VTA foma output (default is VTA_STRUCTURE).
    vta_imp_structure : dict, optional
        Structure of the VTA foma output for imperative verbs (default is VTA_IMP_STRUCTURE).

    Returns
    -------
    dict
        JSON object dictionary containing {"verb", "verb_type", "subject", "object"}.
    """
    return fst_vta_verb_analyzer(fst_analysis_string, vta_structure, vta_imp_structure)



def vti_build_en_sentence(sentence_structure:str, dict_template_dataframe:DataFrame)->list[str]:
    """
    VTI wrapper function that calls the VTA function to build an English sentence based on the sentence structure.

    Parameters
    ----------
    sentence_structure : dict
        Dictionary containing FST data, e.g., {'verb': 'waabam', 'verb_type': 'VTA', 'subject': '3SgProx', 'object': '1Sg'}.
    dict_template_dataframe : pandas.DataFrame
        DataFrame containing definitions and templates for the verbs.

    Returns
    -------
    list of str
        A list of alternative English sentences.
    """    
    return vta_build_en_sentence(sentence_structure, dict_template_dataframe)

def vti_oj2en_builder(inflected_ojibwe_word:str, core_environment:dict)->list[dict]:
    """
    VTI wrapper function that calls the VTA function to build a simple sentence from an Ojibwe VTA verb to an English sentence.

    Parameters
    ----------
    inflected_ojibwe_word : str
        Ojibwe word, e.g., 'niwaabamig'.
    fst_parser : FST
        FST to connect to Foma backend.
    dict_template_dataframe : pandas.DataFrame
        DataFrame containing definitions and templates for the verbs.

    Returns
    -------
    list of dict
        List of translated English sentence with extra information such as definition and sentence structure, 
        e.g. [{'input', 'definition', 'sentence_structure', 'translation'}, ...]
    """
    return vta_oj2en_builder(inflected_ojibwe_word=inflected_ojibwe_word, core_environment=core_environment)

