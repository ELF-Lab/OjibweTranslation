"""
    Core functions of Objiwe -> English translations
"""

import pandas as pd
from pandas import DataFrame
import json
from pyinflect import getAllInflections, getInflection
from fst_runtime.fst import Fst
from ojibwe_translation.oj_constants import *
from ojibwe_translation import logger


def load_fst_parser(fst_att_file_path: str) -> Fst:
    """
    Load foma parser from fomabin file.

    Parameters
    ----------
    fst_att_file_path : str
        Full path to the ojibwe.fomabin file.

    Returns
    -------
    Fst
        FST parser.
    """


    try:
        logger.debug("Loading from file: %s", fst_att_file_path)
        fst = Fst(fst_att_file_path)
        logger.debug("FST loaded.")
        return fst
    except ValueError as e:
        logger.debug("Error loading the FST parser.")
        raise e


def load_dictionary_templates(dictionary_template_file_path: str) -> pd.DataFrame:
    """
    Load Ojibwe to English dictionary from a CSV file.

    Parameters
    ----------
    dictionary_template_file_path : str
        Full path to the dictionary CSV file.

    Returns
    -------
    DataFrame
        DataFrame containing the dictionary data.
    """

    try:
        logger.debug(f"Loading data from file {dictionary_template_file_path}")
        dataframe = pd.read_csv(dictionary_template_file_path)
        logger.debug(f"Record counts = {len(dataframe)}")
        return dataframe
    except FileNotFoundError as e:
        raise ValueError("The dictionary template file was not found at the provided path: %s", 
                         dictionary_template_file_path) from e
    except pd.errors.ParserError as e:
        raise ValueError("Dictionary template file provided is not a valid CSV file.") from e
    except Exception as e:
        raise IOError(f"Error loading from file. {e}")



def inflected_ojibwe_word_process_inflected_form(inflected_word: str, fst: Fst) -> list[str]:
    """
    Call foma to process inflected word.

    Parameters
    ----------
    inflected_word : str
        An Ojibwe inflected word, e.g. "niwaabamig".
    fst : FST
        FST Parser.

    Returns
    -------
    list of str"1Sg"
        List of parsed word structure, e.g. ["waabam+VTA+Pos+Neu+3SgProx+1Sg"].
    """
    inflected_word = inflected_word.lower().strip()
        
    analysis_results = list(fst.up_analysis(inflected_word))

    # The resulting analysis may have no forms in which case an empty list will be returned, which is expected.
    return [output.output_string 
            for output in analysis_results
           ]


def convert_fst_subject_tag_to_en_pronoun(fst_subject_tag: str, subject_tag_to_en_dict: dict[str, str] = EN_SUBJECTS) -> str:
    """
    Convert FST tags of subjects to English pronoun.

    Parameters
    ----------
    fst_subject_tag : str
        Subject word tag, e.g. '3SgSubj'.
    subject_tag_to_en_dict : dict, optional
        Dictionary for converting tags to English pronouns, by default EN_SUBJECTS.

    Returns
    -------
    str
        The English subject word, e.g. 'he/she'.
    """

    fst_subject_tag = fst_subject_tag.lower()
    result = subject_tag_to_en_dict.get(fst_subject_tag, "")

    # TODO This likely should be removed in favour of having the dictionary be a 1-1 representation 
    # of the current state of the FST in order to guarantee accuracy.
    if result == "":
        # not found -> find inside keys to find partial match, 
        # e.g 3SgProx not found, will find 3Sg
        for k in subject_tag_to_en_dict.keys():
            if fst_subject_tag.startswith(k):
                result = subject_tag_to_en_dict[k]
    
    return result


def convert_fst_object_tag_to_en_pronoun(fst_object_tag: str, object_tag_to_en_dict: dict[str, str] = EN_OBJECTS) -> str:
    """
    Convert FST tags of objects to English pronoun.

    Parameters
    ----------
    fst_object_tag : str
        Object word tag, e.g. '1SgObj'.
    object_tag_to_en_dict : dict, optional
        Dictionary for converting tags to English pronouns, by default EN_OBJECTS.

    Returns
    -------
    str
        The English object word, e.g. 'me'.
    """

    fst_object_tag = fst_object_tag.lower()
    result = object_tag_to_en_dict.get(fst_object_tag, "")

    if result == "":
        # not found -> find inside keys to find partial match, 
        # e.g 3SgProx not found, will find 3Sg
        for k in object_tag_to_en_dict.keys():
            if fst_object_tag.startswith(k):
                result = object_tag_to_en_dict[k]
    
    return result

def build_verb_in_past_tense(main_sentence_verb: str, subject_tag: str, polarity_tag: str, mode_tag: str, tense_tag: str) -> str:
    """
    Build verb in past tense (gii-).

    Parameters
    ----------
    main_sentence_verb : str
        The main verb
    subject_tag : str
        Subject tag
    polarity_tag : str
        Negation status ("positive", "negative")
    mode_tag : str
        Mode
    tense_tag : str
        Tense

    Returns
    -------
    str
        The verb in past tense.
    """


    if tense_tag != TENSE_PAST:
        result = ""

    # Handle different modes in the past tense.
    if mode_tag == FST_MODE_PRETERIT:
        if polarity_tag == FST_POLARITY_NEGATIVE: 
            result = f"did not used to {main_sentence_verb}"
        else:
            result = f"used to {main_sentence_verb}"

    elif mode_tag == FST_MODE_DUBITATIVE:
        inflected_verb = getInflection(main_sentence_verb, INFLECT_VBN)[0] # see -> seen
        if polarity_tag == FST_POLARITY_NEGATIVE: 
            result = f"might not have {inflected_verb}"
        else:
            result = f"might have {inflected_verb}"
            
    # Neutral mode.
    else: 
        if main_sentence_verb != TO_BE_VERB:
            inflected_verb = getInflection(main_sentence_verb, INFLECT_VBD) # past form: see -> saw
            if polarity_tag == FST_POLARITY_NEGATIVE:
                result = f"did not {main_sentence_verb}"
            else:
                result = inflected_verb[0]
        else:
            # main verb = TOBE
            inflected_verb = TOBE_SUBJ_PAST.get(subject_tag.lower(), "was")
            if polarity_tag == FST_POLARITY_NEGATIVE:
                result = f"{inflected_verb} not"
            else:
                result = inflected_verb
    
    return result

# Handle simple future tense.
# `subject_tag` here is unused because it is unnecessary in English, but will be required for non-English languages so is retained.
def build_verb_in_simple_future_tense(main_sentence_verb: str, subject_tag: str, polarity_tag: str, mode_tag: str, tense_tag: str) -> str:
    """
    Build verb in simple future tense (da/ga-).

    Parameters
    ----------
    main_sentence_verb : str
        The main verb
    subject_tag : str
        Subject tag
    polarity_tag : str
        Negation status
    mode_tag : str
        Mode
    tense_tag : str
        Tense

    Returns
    -------
    str
        The verb in simple future tense.
    """

    # This is set to the main verb because if it's not in the neutral mode we only want this value.
    # I.e. if the mode is preterite or dubitative, then it's not grammatically possible.
    result = main_sentence_verb

    if not (tense_tag == TENSE_FUTURE_WILL or tense_tag == TENSE_FUTURE):
        result = ""

    if mode_tag == FST_MODE_NEUTRAL:
        if polarity_tag == FST_POLARITY_NEGATIVE:
            result = f"will not {main_sentence_verb}"
        else:
            result = f"will {main_sentence_verb}"

    return result


# handle future/wish tense
# def build_verb_future_wish_tense(main_verb="see", subj=SUBJ_1SG, negation=FST_POLARITY_POSITIVE, mode=FST_MODE_NEUTRAL, tense=TENSE_FUTURE_WISH):
def build_verb_future_wish_tense(main_sentence_verb: str, subject_tag: str, polarity_tag: str, mode_tag: str, tense_tag: str) -> str:
    """
    Build verb in future/wish tense (wii-).

    Parameters
    ----------
    main_sentence_verb : str
        The main verb
    subject_tag : str
        Subject tag
    negation : str
        Negation status
    mode_tag : str
        Mode
    tense_tag : str
        Tense

    Returns
    -------
    str
        The verb in future/wish tense.
    """

    result = ""
    if not tense_tag.startswith(TENSE_FUTURE_WISH):
        # suppose to handle future/wish tense only
        return ""

    # handle future/wish tense
    if mode_tag == FST_MODE_PRETERIT: # preterit mode
        if polarity_tag == FST_POLARITY_NEGATIVE: # 
            if (SUBJ_3SG in subject_tag.lower()
                or SUBJ_0SG in subject_tag.lower()
                or SUBJ_1SG in subject_tag.lower() 
                or XSUBJ in subject_tag.lower()): # 
                result = f"was not going to {main_sentence_verb}"
            else: # do not want to do 
                result = f"were not going to {main_sentence_verb}"
        else: # positive
            if (SUBJ_3SG in subject_tag.lower()
                or SUBJ_0SG in subject_tag.lower()
                or SUBJ_1SG in subject_tag.lower() 
                or XSUBJ in subject_tag.lower()): # 
                result = f"was going to {main_sentence_verb}"
            else: # do not want to do 
                result = f"were going to {main_sentence_verb}"
            

        pass # end of preterit mode
    elif mode_tag == FST_MODE_DUBITATIVE:
        if polarity_tag == FST_POLARITY_NEGATIVE: # 
            result = f"might not {main_sentence_verb}"
        else: # positive
            result = f"might {main_sentence_verb}"

        pass # end of dubitative mode
    else: # neutral mode
        modal_verb = "want"

        if polarity_tag == FST_POLARITY_NEGATIVE: # does not / do not want to do
            if SUBJ_3SG in subject_tag.lower() or SUBJ_0SG in subject_tag.lower() or XSUBJ in subject_tag.lower(): 
                result = f"does not {modal_verb} to {main_sentence_verb}"
            else: # do not want to do 
                result = f"do not {modal_verb} to {main_sentence_verb}"
        else: # want / wants to do 
            if SUBJ_3SG in subject_tag.lower() or SUBJ_0SG in subject_tag.lower() or XSUBJ in subject_tag.lower(): # 
                modal_verb = getInflection(modal_verb, INFLECT_VBZ)[0]
            result = f"{modal_verb} to {main_sentence_verb}"

    return result

def build_verb_tobe(main_sentence_verb:str, subject_tag:str, polarity_tag:str, mode_tag:str, tense_tag:str) -> str:
    """
    Build a to-be verb based on subject, negation, mode, tense, etc.

    Parameters
    ----------
    main_sentence_verb : str
        The main verb
    subject_tag : str
        Subject tag
    negation : str
        Negation status
    mode_tag : str
        Mode
    tense_tag : str
        Tense

    Returns
    -------
    str
        Inflected verb, e.g. 'is', 'are', 'will be', etc.
    """

    result = main_sentence_verb
    tense_tag = tense_tag.lower().strip()
    mode_tag = mode_tag.lower().strip()
    polarity_tag = polarity_tag.lower().strip()
    subject_tag = subject_tag.lower().strip().strip()


    main_verb = TO_BE_VERB

    if tense_tag == TENSE_PAST:
        # handle past tense
        result = build_verb_in_past_tense(main_sentence_verb=main_verb, 
                                        subject_tag=subject_tag, 
                                        polarity_tag=polarity_tag, 
                                        mode_tag=mode_tag, 
                                        tense_tag=tense_tag
                                      )
    elif tense_tag.startswith(TENSE_FUTURE):
        # handle future tense
        if tense_tag.startswith(TENSE_FUTURE_WILL) or tense_tag == TENSE_FUTURE: # will see / will not see
            result = build_verb_in_simple_future_tense(main_sentence_verb=main_verb, 
                                                    subject_tag=subject_tag, 
                                                    polarity_tag=polarity_tag, 
                                                    mode_tag=mode_tag, 
                                                    tense_tag=tense_tag
                                                   )
            pass
            
        elif tense_tag.startswith(TENSE_FUTURE_GOING): # is going to see / is not going to see
            # first, process to be verb (am/is/are going to do...)
            tobe_verb = "are" # default
            
            if (SUBJ_3SG in subject_tag.lower()) or (SUBJ_0SG in subject_tag.lower()): # is going to do
                tobe_verb = "is"
            elif SUBJ_1SG in subject_tag.lower(): # I am going to do
                tobe_verb = "am"
            
            if polarity_tag == FST_POLARITY_NEGATIVE: # is not going to do
                result = f"{tobe_verb} not going to {main_verb}"
            else: # is going to do
                result = f"{tobe_verb} going to {main_verb}"
            pass
            
        elif tense_tag.startswith(TENSE_FUTURE_WISH): # wants to see / don't want to see
            result = build_verb_future_wish_tense(main_sentence_verb=main_verb, 
                                                   subject_tag=subject_tag, 
                                                   polarity_tag=polarity_tag, 
                                                   mode_tag=mode_tag, 
                                                   tense_tag=tense_tag
                                                  )
            pass
            
            
        pass # end of future tense
    else: # present tense
        if mode_tag == FST_MODE_NEUTRAL:
            if polarity_tag!=FST_POLARITY_NEGATIVE:
                result = "are" # default
                if (SUBJ_3SG in subject_tag.lower()) or (SUBJ_0SG in subject_tag.lower()):
                    result = "is"
                elif SUBJ_1SG in subject_tag.lower():
                    result = "am"
                    
            else: # negation == FST_NEGATION_NEGATIVE
                result = "are not" # default
                # if SUBJ_3SG in subject_tag.lower():
                if (SUBJ_3SG in subject_tag.lower()) or (SUBJ_0SG in subject_tag.lower()):
                    inflected_verb = f"is not"
                    result = inflected_verb
                elif SUBJ_1SG in subject_tag.lower(): 
                    inflected_verb = f"am not"
                    result = inflected_verb
                
        elif mode_tag == FST_MODE_PRETERIT:
        # handle Preterit mode (assuming it's past tense, but not true to the present, 
        # e.g. I saw him (but not now))
            result = build_verb_in_past_tense(main_sentence_verb=main_verb, 
                                            subject_tag=subject_tag, 
                                            polarity_tag=polarity_tag, 
                                            mode_tag=mode_tag, 
                                            tense_tag=tense_tag
                                          )
                
        elif mode_tag == FST_MODE_DUBITATIVE:
        # handle Dubitative mode (uncertainty, e.g. "he might see it")
            if polarity_tag!=FST_POLARITY_NEGATIVE: # see -> might see
                # insert "might" before the verb
                inflected_verb = f"might {main_verb}"
                result = inflected_verb
            else: # negation = FST_NEGATION_NEGATIVE, see -> might not see
                inflected_verb = f"might not {main_verb}"
                result = inflected_verb
        pass # end of if tense == "", present tense

    return result

def build_verb(main_sentence_verb: str, subject_tag: str, polarity_tag: str, mode_tag: str, tense_tag: str) -> str:
    """
    Build a verb based on subject, negation, mode, tense, etc.

    Parameters
    ----------
    main_sentence_verb : str
        The main verb
    subject_tag : str
        Subject tag
    negation : str
        Negation status
    mode_tag : str
        Mode
    tense_tag : str
        Tense

    Returns
    -------
    str
        Inflected verb, e.g. 'see' or 'sees'.
    """
    result = main_sentence_verb
    tense_tag = tense_tag.lower().strip()
    mode_tag = mode_tag.lower().strip()
    polarity_tag = polarity_tag.lower().strip()
    subject_tag = subject_tag.lower().strip().strip()

    
    main_verb = main_sentence_verb.split()[0]  # e.g. 'put up' -> 'put'

    if main_verb == TO_BE_VERB: # special case, for passive voice
        
        result = build_verb_tobe(main_sentence_verb=TO_BE_VERB,
                                 subject_tag=subject_tag, 
                                 polarity_tag=polarity_tag, 
                                 mode_tag=mode_tag, 
                                 tense_tag=tense_tag
                                )
        return result
        
        
    if tense_tag == TENSE_PAST:
        # handle past tense
        result = build_verb_in_past_tense(main_sentence_verb=main_verb, 
                                        subject_tag=subject_tag, 
                                        polarity_tag=polarity_tag, 
                                        mode_tag=mode_tag, 
                                        tense_tag=tense_tag
                                      )
    elif tense_tag.startswith(TENSE_FUTURE):
        # handle future tense
        if tense_tag.startswith(TENSE_FUTURE_WILL) or tense_tag == TENSE_FUTURE: # will see / will not see
            result = build_verb_in_simple_future_tense(main_sentence_verb=main_verb, 
                                                    subject_tag=subject_tag, 
                                                    polarity_tag=polarity_tag, 
                                                    mode_tag=mode_tag, 
                                                    tense_tag=tense_tag
                                                   )
            pass
            
        elif tense_tag.startswith(TENSE_FUTURE_GOING): # is going to see / is not going to see
            # first, process to be verb (am/is/are going to do...)
            tobe_verb = "are" # default
            
            if (SUBJ_3SG in subject_tag.lower()) or (SUBJ_0SG in subject_tag.lower()):
                # is going to do
                tobe_verb = "is"
            elif SUBJ_1SG in subject_tag.lower(): 
                # I am going to do
                tobe_verb = "am"
            
            if polarity_tag == FST_POLARITY_NEGATIVE: # is not going to do
                result = f"{tobe_verb} not going to {main_verb}"
            else: # is going to do
                result = f"{tobe_verb} going to {main_verb}"
            pass
            
        elif tense_tag.startswith(TENSE_FUTURE_WISH): # wants to see / don't want to see
            result = build_verb_future_wish_tense(main_sentence_verb=main_verb, 
                                                   subject_tag=subject_tag, 
                                                   polarity_tag=polarity_tag, 
                                                   mode_tag=mode_tag, 
                                                   tense_tag=tense_tag
                                                  )
            pass
            
            
        pass # end of future tense
    else: # present tense
        # debug
        if mode_tag == FST_MODE_NEUTRAL:
            if polarity_tag!=FST_POLARITY_NEGATIVE:
                if (SUBJ_3SG in subject_tag.lower()) or (SUBJ_0SG in subject_tag.lower()):
                    inflected_verb = getInflection(main_verb, INFLECT_VBZ)
                    if inflected_verb is not None and len(inflected_verb) > 0:
                        inflected_verb = inflected_verb[0]
                        result = inflected_verb
                    else:
                        result = main_sentence_verb
            else: # negation == FST_NEGATION_NEGATIVE
                if (SUBJ_3SG in subject_tag.lower()) or (SUBJ_0SG in subject_tag.lower()): # see -> doesn't see
                    inflected_verb = f"does not {main_verb}"
                    result = inflected_verb
                else: # see -> don't see
                    inflected_verb = f"do not {main_verb}"
                    result = inflected_verb
                
        elif mode_tag == FST_MODE_PRETERIT:
        # handle Preterit mode (assuming it's past tense, but not true to the present, 
        # e.g. I saw him (but not now))
            if polarity_tag!=FST_POLARITY_NEGATIVE: # see -> saw
                inflected_verb = getInflection(main_verb, INFLECT_VBD)
                if inflected_verb is not None and len(inflected_verb) > 0:
                    inflected_verb = inflected_verb[0]
                    result = inflected_verb
                else:
                    result = main_sentence_verb
            else: # negation == FST_NEGATION_NEGATIVE, see -> didn't see
                inflected_verb = f"did not {main_verb}"
                result = inflected_verb
                
        elif mode_tag == FST_MODE_DUBITATIVE:
        # handle Dubitative mode (uncertainty, e.g. "he might see it")
            if polarity_tag!=FST_POLARITY_NEGATIVE: # see -> might see
                # insert "might" before the verb
                inflected_verb = f"might {main_verb}"
                result = inflected_verb
            else: # negation = FST_NEGATION_NEGATIVE, see -> might not see
                inflected_verb = f"might not {main_verb}"
                result = inflected_verb
        pass # end of if tense == "", present tense

    return result

def build_imperative_sentence(sentence_structure_dict: dict, sentence: str) -> str:
    """
    Build an imperative sentence.

    Parameters
    ----------
    sentence_structure_dict : dict
        Dictionary containing FST tags of the sentence.
    sentence : str
        The base sentence, e.g. "dip him/her/it in water".

    Returns
    -------
    str
        imperative sentences, e.g. "dip him/her/it in water" / "don't dip him/her/it in water".
    """

    result = ""
    if sentence_structure_dict[ORDER] != FST_ORDER_IMPERATIVE:
        # not correct input
        return result

    # filter out {{subject}} in the sentence
    if f"{SUBJECT_SLOT} " in sentence:
        sentence = sentence.replace(f"{SUBJECT_SLOT} ", "")
    
    if sentence_structure_dict[MODE] == FST_MODE_PROHIBITIVE:
        # Prohibitive mode, e.g. "Dont't close the door"
        result = f"{TRANSLATION_IMP_PREFIX} don't {sentence}"
    elif sentence_structure_dict[MODE] == FST_MODE_DELAYED:
        # Delayed mode, e.g. Close the door later
        result = f"{TRANSLATION_IMP_PREFIX} {sentence} {TRANSLATION_IMP_DELAYED_AFFIX}"
    else: # sentence_structure[MODE] == "sim":
        # simple imperative (e.g. Close the door)
        result = f"{TRANSLATION_IMP_PREFIX} {sentence}"

    return result

def verb_oj2en(ojibwe_verb: str, dictionary_template_dataframe: DataFrame) -> dict:
    """
    Get the corresponding verb and definitions from Ojibwe lemma to English.

    Parameters
    ----------
    ojibwe_verb : str
        Ojibwe lemma, e.g. "waabam".
    dictionary_template_dataframe : DataFrame
        DataFrame containing definitions and templates of VTA verbs.

    Returns
    -------
    dict
        English verb, e.g. "see", and templates, e.g. "see {{object}}" in form of dictionary.
        {"verbs":[], "templates:[]}
    """

    ojibwe_verb = ojibwe_verb.lower()
    
    result = {VERB_LEMMA:[], DATA_TEMPLATES:[]}
    query_results = dictionary_template_dataframe.query(f"{DATA_LEMMA} == @ojibwe_verb")
    if len(query_results) > 0:
        item = query_results.iloc[0]
        json_object = item[DATA_LLM_TEMPLATES]
        if json_object.strip() != "":
            try:
                result = eval(json_object)
            except:
                logger.debug("Error parsing data =", json_object)
                return None
    return result

def replace_possessive_reflexive_words(sentence: str, subject_tag:str) -> str:
    """
    Replace generic words like `one's` or `oneself` with appropriate words (my, myself, etc).

    Parameters
    ----------
    sentence : str
        The sentence containing `one*` words.
    subject_tag : str
        The subject (1sgsubj, 3sgsubj, etc), by default "3sgsubj".

    Returns
    -------
    str
        The sentence with words replaced (e.g. "he looks at oneself" -> "he looks at himself")
    """
    result = sentence
    word = f" {TRANSLATION_ONE_POSSESSIVE}"
    if word in sentence:
        new_word = SUBJ_POSSESSIVE.get(subject_tag, f"({TRANSLATION_ONE_POSSESSIVE})")
        result = result.replace(word, f" {new_word}")
    
    word = f" {TRANSLATION_ONESELF}"
    if word in sentence:
        new_word = SUBJ_REFLEXIVE.get(subject_tag, f"({TRANSLATION_ONESELF})")
        result = result.replace(word, f" {new_word}")

    return result


def replace_possessive_obj(sentence:str, object_tag:str, slot=OBJECT_POSSESSIVE_SLOT) -> str:
    """
    Replace {{object-possessive}} with his/her/its, etc.

    Parameters
    ----------
    sentence : str
        The sentence containing `one*` words.
    object_tag : str
        The object (1sgobj, 3sgobj, etc)
    slot : str, optional
        The possessive slot, by default "{{object-possessive}}".

    Returns
    -------
    str
        The sentence with words replaced. (e.g. "he turns on one's side" -> "he turns on his side")
    """

    result = sentence
    word = slot
    if word in sentence:
        new_word = OBJ_POSSESSIVE.get(object_tag, f"{TRANSLATION_ONE_POSSESSIVE}")
        result = result.replace(word, f"{new_word}")
    
    return result
