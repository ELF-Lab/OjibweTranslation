"""
    structures and functions to translate VAI (Animate, Intransitive) verbs to English.
    Because there are some differences between VTA and VAI verbs, some functions are re-written.
"""
from ojibwe_translation.oj_translation_core import *
from ojibwe_translation.vta import *
from ojibwe_translation.oj_constants import *

def vai_add_null_object(fst_analysis_string:str)->str:
    """
    Add NullObj tag to FST tags of VAI/VII verbs for compatibility with VTA structure.

    Parameters
    ----------
    fst_analysis_string : str
        The output string from the FST that needs the NullObj tag added.

    Returns
    -------
    str
        The modified FST output string with the NullObj tag added.
    """
    # add Null object tag to the fst analysis to be compatible with VTA/VTI
    if ((f"+{FST_VAI}" in fst_analysis_string.lower() or f"+{FST_VII}" in fst_analysis_string.lower()) 
        and ("obj" not in fst_analysis_string.lower())):
        return fst_analysis_string + NULL_OBJ_TAG
    else:
        return fst_analysis_string


def fst_vai_normal_analyzer(fst_analysis_string:str, sentence_structure:dict=VAI_STRUCTURE)->dict:
    """
    VAI wrapper function, will call VTA function.
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
    # add Null object tag to the fst analysis to be compatible with VTA/VTI
    fst_analysis_string = vai_add_null_object(fst_analysis_string)
    return fst_vta_normal_analyzer(fst_analysis_string, sentence_structure)
    
def fst_vai_imp_analyzer(fst_analysis_string:str, sentence_structure:dict=VAI_IMP_STRUCTURE)->dict:
    """
    VAI wrapper function, will call VTA function.

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
    # add Null object tag to the fst analysis to be compatible with VTA/VTI
    fst_analysis_string = vai_add_null_object(fst_analysis_string)
    return fst_vta_imp_analyzer(fst_analysis_string, sentence_structure)



def fst_vai_verb_analyzer(fst_analysis_string:str, vai_structure:dict=VAI_STRUCTURE, vai_imp_structure:dict=VAI_IMP_STRUCTURE)->dict:
    """
    VAI wrapper function, will call VTA function.

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
    # add Null object tag to the fst analysis to be compatible with VTA/VTI
    fst_analysis_string = vai_add_null_object(fst_analysis_string)
    return fst_vta_verb_analyzer(fst_analysis_string, vai_structure, vai_imp_structure)


def vai_build_en_sentence(sentence_structure:dict, dict_template_dataframe:DataFrame)->list[str]:
    """
    VAI wrapper function, will call VTA function.

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
    return vta_build_en_sentence(sentence_structure=sentence_structure, dictionary_template_dataframe=dict_template_dataframe)


def vai_oj2en_builder(inflected_ojibwe_word:str, core_environment:dict)->list[dict]:

    """
    Simple sentence builder from an Ojibwe VAI verb to possible English sentences.

    Parameters
    ----------
    inflected_ojibwe_word : str
        Ojibwe word, e.g. 'niwaabamig'.
    core_environment : dict
        The core environment dict object containing FST parser, dictionary and templates data

    Returns
    -------
    list of dict
        List of translated English sentence with definition and sentence structure, 
        e.g. [{'input', 'definition', 'sentence_structure', 'translation'}, ...]
    """
    return vta_oj2en_builder(inflected_ojibwe_word=inflected_ojibwe_word, 
                             core_environment=core_environment,
                             verb_analyzer_function=fst_vai_verb_analyzer
                             )
