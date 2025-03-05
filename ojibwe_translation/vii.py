"""
    structures and functions to translate VII (intransitive, Inanimate) verbs to English.
    Because VAI (Animate, Intransitive) are very similar to VII, 
    the VII functions will mainly be wrapper functions to call VAI functions
"""
from ojibwe_translation.oj_translation_core import *
from ojibwe_translation.vai import *
from ojibwe_translation.oj_constants import *


def fst_vii_normal_analyzer(fst_analysis_string:str, sentence_structure:dict=VAI_STRUCTURE) -> dict:
    """
    VII wrapper function, will call VAI function.
    Parse FST tags to a JSON object (dictionary), for normal (independent) VAI verb.

    Parameters
    ----------
    fst_analysis_string : str
        FST string of a verb, e.g. "waabam+VTA+Pos+Neu3SgProx+1S".
    sentence_structure : dict, optional
        Structure of the VTA foma output, by default VAI_STRUCTURE.

    Returns
    -------
    dict
        Dictionary object with keys "verb", "verb_type", "subject", and "object".
    """
    return fst_vai_normal_analyzer(fst_analysis_string, sentence_structure)
    



def fst_vii_imp_analyzer(fst_analysis_string:str, sentence_structure:dict=VAI_IMP_STRUCTURE)-> dict:
    """
    VII wrapper function, will call VAI function.

    Parse FST tags to a JSON object (dictionary), for Imperative VAI verb.

    Parameters
    ----------
    fst_analysis_string : str
        FST string of a verb, e.g. "jekibiin+VTA+Imp+Sim+2SgSubj+3SgProxObj".
    sentence_structure : dict, optional
        Structure of the VTA foma output, by default VAI_IMP_STRUCTURE.

    Returns
    -------
    dict
        JSON dictionary with keys "verb", "verb_type", "subject", and "object".
    """    
    return fst_vai_imp_analyzer(fst_analysis_string=fst_analysis_string, sentence_structure=sentence_structure)



def fst_vii_verb_analyzer(fst_analysis_string:str, vai_structure:str=VAI_STRUCTURE, vai_imp_structure:str=VAI_IMP_STRUCTURE)-> dict:
    """
    VII wrapper function, will call VAI function.

    Analyze the VTA verb, based on order (independence / imperative / conjunction).

    Parameters
    ----------
    fst_analysis_string : str
        FST string of a verb, e.g. "waabam+VTA+Pos+Neu3SgProx+1S".
    vai_structure : dict, optional
        Structure for independent VAI verbs, by default VAI_STRUCTURE.
    vai_imp_structure : dict, optional
        Structure for imperative VAI verbs, by default VAI_IMP_STRUCTURE.

    Returns
    -------
    dict
        JSON object dictionary with keys "verb", "verb_type", "subject", and "object".
    """
    return fst_vai_verb_analyzer(fst_analysis_string, vai_structure, vai_imp_structure)



def vii_build_en_sentence(sentence_structure:dict, dict_template_dataframe:DataFrame)->list[str]:
    """
    VII wrapper function, will call VAI function.

    Build an English sentence based on the sentence structure.

    Parameters
    ----------
    sentence_structure : dict
        Dictionary containing FST tags, e.g. {'verb': 'waabam', 'verb_type': 'VTA', 'subject': '3SgProx', 'object': '1Sg'}.
    dict_template_dataframe : DataFrame
        The dataframe containing definitions and templates for the verbs.

    Returns
    -------
    list of str
        A list of alternative English sentences.
    """
    return vai_build_en_sentence(sentence_structure, dict_template_dataframe)


def vii_oj2en_builder(inflected_ojibwe_word:str, core_environment:dict)->list[dict]:
    """
    Simple sentence builder from an Ojibwe VAI verb to possible English sentences.

    Parameters
    ----------
    inflected_ojibwe_word : str
        Ojibwe word, e.g. 'niwaabamig'.
    fst_parser : FST
        FST to connect to Foma backend.
    dict_template_dataframe : DataFrame
        The dataframe containing definitions and templates for the verbs.

    Returns
    -------
    list of dict
        List of translated English sentence with definition and sentence structure, 
        e.g. [{'input', 'definition', 'sentence_structure', 'translation'}, ...]
    """
    return vai_oj2en_builder(inflected_ojibwe_word=inflected_ojibwe_word, core_environment=core_environment)

