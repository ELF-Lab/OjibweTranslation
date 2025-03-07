"""
    Structures and functions to translate VTA (Transitive, Animated) verbs to English
"""
from ojibwe_translation.oj_translation_core import *
from ojibwe_translation.oj_constants import *

def fst_vta_normal_analyzer(fst_analysis_string: str, sentence_structure:dict=VTA_STRUCTURE) -> dict:
    """
    Parse FST tags to a JSON object (dictionary) for normal (independent) VTA verb.

    Parameters
    ----------
    fst_analysis_string : str
        FST-output string of a verb, e.g., "waabam+VTA+Pos+Neu3SgProx+1S".
    sentence_structure : dict, optional
        Structure of the VTA foma output (default is VTA_STRUCTURE).

    Returns
    -------
    dict
        Dictionary object containing {"verb", "verb_type", "subject", "object"}.
    """
    
    result = dict()
    
    tokens = fst_analysis_string.split(FST_SEPARATOR)

    # handle tense
    if tokens[0].lower().strip().startswith(FST_TENSE_PREFIX):
        tense = tokens[0].split(FST_TENSE_SEPARATOR)[-1] # e.g. PVTense/ga -> extract "ga"
        result[TENSE] = TENSE_MAPPING.get(tense, DEFAULT_TENSE) # convert gii -> "past", etc
        tokens.pop(0)
        
    
    if len(tokens) < len(sentence_structure.keys()):
        # wrong format
        logger.debug(f"Wrong format. Expecting {len(sentence_structure.keys())} elements. Got {len(tokens)} instead.")
        return None

    result[VERB_LEMMA] = tokens[sentence_structure[VERB_LEMMA]].lower().strip()
    result[VERB_TYPE] = tokens[sentence_structure[VERB_TYPE]].lower().strip()
    result[ORDER] = tokens[sentence_structure[ORDER]].lower().strip()

    # if result[ORDER] == "ind": # normal VTA
    result[POLARITY] = tokens[sentence_structure[POLARITY]].lower().strip()
    result[MODE] = tokens[sentence_structure[MODE]].lower().strip()
    result[SUBJECT] = tokens[sentence_structure[SUBJECT]].lower().strip()

    # special case: handle XSubj -> "3SgXSubj"
    if result[SUBJECT] == XSUBJ:
        result[SUBJECT] = X3SG_SUBJ
        
    result[OBJECT] = tokens[sentence_structure[OBJECT]].lower().strip()
    # special case: handle XObj -> "3SgXObj"
    if result[OBJECT] == XOBJ:
        result[OBJECT] = X3SG_OBJ

    return result

def fst_vta_imp_analyzer(fst_analysis_string:str, sentence_structure:dict=VTA_IMP_STRUCTURE) -> dict:
    """
    Parse FST tags to a JSON object (dictionary) for Imperative VTA verb.

    Parameters
    ----------
    fst_analysis_string : str
        FST-output string of a verb, e.g., "jekibiin+VTA+Imp+Sim+2SgSubj+3SgProxObj".
    sentence_structure : dict, optional
        Structure of the VTA foma output (default is VTA_IMP_STRUCTURE).

    Returns
    -------
    dict
        JSON dictionary containing {"verb", "verb_type", "subject", "object"}.
    """    
    result = dict()
    
    tokens = fst_analysis_string.split(FST_SEPARATOR)

    # handle tense. Imperative shouldn't have tense -> will ignore tense
    if tokens[0].lower().strip().startswith(FST_TENSE_PREFIX):
        logger.debug("Invalid tense detected (with Imperative) =", tokens[0])
        # remove tense token
        tokens.pop(0)

    if len(tokens) < len(sentence_structure.keys()):
        # wrong format
        return None

    result[VERB_LEMMA] = tokens[sentence_structure[VERB_LEMMA]].lower().strip()
    result[VERB_TYPE] = tokens[sentence_structure[VERB_TYPE]].lower().strip()
    result[ORDER] = tokens[sentence_structure[ORDER]].lower().strip()

    result[MODE] = tokens[sentence_structure[MODE]].lower().strip()
    result[SUBJECT] = tokens[sentence_structure[SUBJECT]].lower().strip()
    result[OBJECT] = tokens[sentence_structure[OBJECT]].lower().strip()

    return result

def fst_vta_verb_analyzer(fst_analysis_string:str, vta_structure:dict=VTA_STRUCTURE, vta_imp_structure:dict=VTA_IMP_STRUCTURE) -> dict:
    """
    Analyze the VTA verb based on order (independence / imperative / conjunction).

    Parameters
    ----------
    fst_analysis_string : str
        FST string of a verb, e.g., "waabam+VTA+Pos+Neu3SgProx+1S".
    vta_structure : dict, optional
        Structure for VTA, by default VTA_STRUCTURE.
    vta_imp_structure : dict, optional
        Structure for VTA imperative, by default VTA_IMP_STRUCTURE.

    Returns
    -------
    dict
        JSON object dictionary containing {"verb", "verb_type", "subject", "object"}.
    """

    
    result = dict()
    
    tokens = fst_analysis_string.split(FST_SEPARATOR)

    # handle tense
    if tokens[0].lower().strip().startswith(FST_TENSE_PREFIX):
        tokens.pop(0) # remove tense tag

    if len(tokens) < min(len(vta_structure.keys()),
                         len(vta_imp_structure.keys())
                        ):
        # wrong format
        logger.debug(f"Error, wrong format. Expecting at least {min(len(vta_structure.keys()), len(vta_imp_structure.keys()))} elements.\n" + 
              f"Got {len(tokens)} instead")
        return None

    result[ORDER] = tokens[vta_structure[ORDER]].lower().strip()

    if result[ORDER] == FST_ORDER_CONJUNCTION:  
        # conjuction VTA -> use the same normal analyzer (same structure as Independence)
        result = fst_vta_normal_analyzer(fst_analysis_string, vta_structure)
    elif result[ORDER] == FST_ORDER_IMPERATIVE: # imperative mode
        result = fst_vta_imp_analyzer(fst_analysis_string, vta_imp_structure)
    else: #  normal VTA
        result = fst_vta_normal_analyzer(fst_analysis_string, vta_structure) 

    return result

   
def _get_english_subject_and_object(sentence_structure:dict, sentence_template:str) -> tuple[str, str]:
    """
    Get English subject and object based on sentence structure and sentence template.

    Parameters
    ----------
    sentence_structure : dict
        Dictionary containing FST data, e.g., {'verb': 'waabam', 'verb_type': 'VTA', 'subject': '3SgProx', 'object': '1Sg'}.
    sentence_template : str
        The template from the database (e.g., "{{subject}} see {{object}}").

    Returns
    -------
    tuple[str, str]
        Subject string and object string.
    """
    # find subject and object
    subject = convert_fst_subject_tag_to_en_pronoun(sentence_structure.get(SUBJECT, ""))
    object = convert_fst_object_tag_to_en_pronoun(sentence_structure.get(OBJECT, ""))
    
    # handle special case: "there is something" -> no subject
    if (EXISTENCE_PREFIX) in sentence_template.lower():
        # existential sentence (e.g. 'there is a stone on the ground' -> no subject replacement by pronoun (it/they/etc)
        subject = "" 
    
    return (subject, object)    
    
# building base sentence in English doesn't need subject, because imperative can omit subject (e.g. "Please close the door")
def _build_base_sentence(sentence_structure: dict, english_verb: str, sentence_template: str, subject:str, object:str) -> str:   
    """
    Build the base English sentence from various factors (subject/object/tense/etc).

    Parameters
    ----------
    sentence_structure : dict
        Dictionary containing FST data, e.g., {'verb': 'waabam', 'verb_type': 'VTA', 'subject': '3SgProx', 'object': '1Sg'}.
    sentence_template : str
        The template from the database (e.g., "{{subject}} see {{object}}").
    english_verb : str
        The main English verb in the sentence.
    subject : str
        The subject (e.g., we/they/he/she).
    object : str
        The object (e.g., me/us/him/her).

    Returns
    -------
    str
        The English sentence.
    """

    result = sentence_template
        
    # inflect English verb based on subject, tense, etc
    logger.debug(f"Main verb = {english_verb}")
    english_verb_inflected = build_verb(main_sentence_verb=english_verb, 
                                        subject_tag=sentence_structure.get(SUBJECT, ""),
                                        polarity_tag=sentence_structure.get(POLARITY, DEFAULT_NEGATION),
                                        mode_tag=sentence_structure.get(MODE, DEFAULT_MODE),
                                        tense_tag=sentence_structure.get(TENSE, DEFAULT_TENSE),
                                        )
    
    logger.debug(f"Verb type = {sentence_structure[VERB_TYPE]}")
    
    if sentence_structure[VERB_TYPE] in [FST_VTA, FST_VTI]:
        result = result.replace(OBJECT_SLOT, object)
    elif sentence_structure[VERB_TYPE] in [FST_VAI, FST_VII]:
        # VAI/VII templates sometimes doesn't have {{object}} slot
        if OBJECT_SLOT in sentence_template:
            sentence = sentence_template.replace(OBJECT_SLOT, object)
        elif ((object == "them") and 
              (" it" or " (it)" in sentence_template) and 
              (SUBJECT_SLOT in sentence) and
              (not OBJ_INTRANSITIVE_SLOT in sentence_template)
             ):
            # special case for VAIO, with Plural Object
            # replace "it" / "(it)" with object
            sentence = sentence_template.replace(" it", f" {object}").replace("(it)", f"({object})")

    
    result = result.replace(english_verb, english_verb_inflected)
    
    return result

def _modify_sentence_by_order(sentence_structure:dict, sentence:str, subject:str, object:str) -> str:
    """
    Modify the base sentence according to the order (Independence / Conjunction / Imperative).

    Parameters
    ----------
    sentence_structure : dict
        Dictionary containing FST data, e.g., {'verb': 'waabam', 'verb_type': 'VTA', 'subject': '3SgProx', 'object': '1Sg'}.
    sentence : str
        The base sentence.
    subject : str
        The subject (e.g., we/they/he/she).
    object : str
        The object (e.g., me/us/him/her).

    Returns
    -------
    str
        The modified sentence according to the specified order.
    """

    result = ""
    # handle "independent" / "imperative" order
    if sentence_structure[ORDER] == FST_ORDER_INDEPENDENCE: 
        # independent order (e.g. I see him) -> subject - verb - object
        if SUBJECT_SLOT in sentence:
            # replace {{subject}} slot with subject
            result = sentence.replace(SUBJECT_SLOT, subject)
        # else:
        #     # put subject at the beginning of the sentence
        #     result = f"{subject} {sentence}"
        elif OBJ_INTRANSITIVE_SLOT in sentence:
            # has {{object-intransitive}} slot -> replace he/she -> him/her
            # logger.debug("Object-transitive Detected")
            obj_int = convert_fst_object_tag_to_en_pronoun(sentence_structure.get(SUBJECT, "").replace(SUBJ, OBJ))
            # logger.debug("Object =", obj_int)
            result = sentence.replace(OBJ_INTRANSITIVE_SLOT, obj_int)
        else:
            # put subject at the beginning of the sentence
            if subject != "":
                result = f"{subject} {sentence}"
            else:
                result = f"{sentence}"
        
    elif sentence_structure[ORDER] == FST_ORDER_IMPERATIVE: 
        # imperative order (e.g. Close the door) -> verb - object
        result = build_imperative_sentence(sentence_structure, sentence) 
    elif sentence_structure[ORDER] == FST_ORDER_CONJUNCTION: 
        # conjunction order (e.g. I see her -> if/when I see her)
        if SUBJECT_SLOT in sentence:
            # replace {{subject}} slot with subject
            result = f"{TRANSLATION_CONJ_PREFIX} {sentence.replace(SUBJECT_SLOT, subject)}"
        else:
            # put subject at the beginning of the sentence
            # result = f"{TRANSLATION_CONJ_PREFIX} {subject} {sentence}"
            if subject != "":
                result = f"{TRANSLATION_CONJ_PREFIX} {subject} {sentence}"
            else:
                result = f"{TRANSLATION_CONJ_PREFIX} {sentence}"

    return result

def _post_process_sentence(sentence_structure:dict, sentence:str) -> str:
    """
    Post-process the sentence based on the sentence structure.

    Parameters
    ----------
    sentence_structure : dict
        Dictionary containing FST data, e.g., {'verb': 'waabam', 'verb_type': 'VTA', 'subject': '3SgProx', 'object': '1Sg'}.
    sentence : str
        The sentence to be post-processed.

    Returns
    -------
    str
        The post-processed sentence.
    """

    result = sentence
    # replacing "{{object-possessive}}" with appropriate words for some verbs, e.g. "I follow them by **their** footprints"
    result = replace_possessive_obj(result, sentence_structure.get(OBJECT, None))
   
    # replacing "one's" and "oneself" with appropriate words for VAIs
    result = replace_possessive_reflexive_words(result, sentence_structure.get(SUBJECT, ""))

    return result

def _build_sentence_from_a_template(sentence_structure:dict, english_verb:str, sentence_template:str) -> str:
    """
    Build a sentence from the sentence structure and a template.

    Parameters
    ----------
    sentence_structure : dict
        Dictionary containing FST data, e.g., {'verb': 'waabam', 'verb_type': 'VTA', 'subject': '3SgProx', 'object': '1Sg'}.
    english_verb : str
        The main English verb in the sentence.
    sentence_template : str
        Template for the sentence, e.g., "{{subject}} see {{object}}".

    Returns
    -------
    str
        The constructed sentence.
    """

    result = ""
    
    (subject, object) = _get_english_subject_and_object(sentence_structure=sentence_structure, sentence_template=sentence_template)
    # logger.debug(f"Subject = {subject}, object = {object}")
    
    # build the base sentence (with tense, negation, etc, but WITHOUT mode)
    sentence = _build_base_sentence(sentence_structure=sentence_structure, english_verb=english_verb, 
                                    sentence_template=sentence_template, subject=subject, object=object)
    # logger.debug(f"Base sentence = {sentence}")

    # modify the sentence with mode
    result = _modify_sentence_by_order(sentence_structure=sentence_structure, sentence=sentence, 
                                      subject=subject, object=object)
    # logger.debug(f"Sentence after modifying by order = {sentence}")
    
    # post-process sentence for replacing ("oneself", "one's", etc with appropriate words)
    result = _post_process_sentence(sentence_structure=sentence_structure, sentence=result)
    # logger.debug(f"Sentence after post-processing = {sentence}")
        
    return result


def vta_build_en_sentence(sentence_structure : dict, dictionary_template_dataframe:DataFrame) -> list[str]:
    """
    Build an English sentence based on the sentence structure.

    Parameters
    ----------
    sentence_structure : dict
        Dictionary containing FST data, e.g., {'verb': 'waabam', 'verb_type': 'VTA', 'subject': '3SgProx', 'object': '1Sg'}.
    dictionary_template_dataframe : pandas.DataFrame
        DataFrame containing definitions and templates for the verbs.

    Returns
    -------
    list of str
        A list of alternative English sentences.
    """    
    result = []

    inflected_ojibwe_verb = sentence_structure.get(VERB_LEMMA)
    english_dictionary_template_obj = verb_oj2en(inflected_ojibwe_verb, 
                                                 dictionary_template_dataframe=dictionary_template_dataframe)

    
    templates = english_dictionary_template_obj.get(DATA_TEMPLATES, "")
    if len(templates) <= 0:
        # no definition/templates found -> nothing to build on
        logger.debug(f"Definition templates for [{inflected_ojibwe_verb}] not found")
        return []

    for sentence_template in templates:
        # find the verb from verb list
        english_verb = ""
        for word in english_dictionary_template_obj[DATA_VERBS]:
            # find the first verb appears in the template
            # we use word.split() to handle compound verb like "look after" -> "look"
            if word.split()[0] in sentence_template.split(): # if the verb match any word in the template?
                english_verb = word.split()[0]
                break
        sentence_output = _build_sentence_from_a_template(sentence_structure=sentence_structure, 
                                                          english_verb=english_verb, 
                                                          sentence_template=sentence_template)
        result.append(sentence_output)
    
    return result


def vta_oj2en_builder(inflected_ojibwe_word:str, core_environment:dict, verb_analyzer_function=fst_vta_verb_analyzer)->list[dict]:
    """
    Simple end-to-end sentence builder, from an Ojibwe VTA verb to an English sentence.

    Parameters
    ----------
    inflected_ojibwe_word : str
        Ojibwe word, e.g., 'niwaabamig'.
    
    core_environment : dict
        The core environment dict object containing FST parser, dictionary and templates data
        
    verb_analyzer_function: function
        The function to analyze parsed FST string to a sentence structure
    
    Returns
    -------
    list of dict
        List of translated English sentence with definition and sentence structure, 
        e.g. [{'input', 'definition', 'sentence_structure', 'translation'}, ...]
    """    
    input = inflected_ojibwe_word

    # get all possible FST parse results from Foma
    fst_output_tags = ""
    fst_output_tags = inflected_ojibwe_word_process_inflected_form(input, fst=core_environment[ENV_FST]) 
    if len(fst_output_tags) <= 0:
        return [{OUTPUT_INPUT: inflected_ojibwe_word,
                 OUTPUT_ERROR: OUTPUT_ERROR_FST_PARSE
               }]
        
    output = []

    if type(fst_output_tags) == list:
        for fst_output_item in fst_output_tags:
            # build possible translation for **each** parsed fst output item 
            sentence_structure = verb_analyzer_function(fst_output_item)
                
            if sentence_structure is None:
                return [{OUTPUT_INPUT: inflected_ojibwe_word,
                         OUTPUT_FST_OUTPUT: fst_output_item,
                         OUTPUT_TRANSLATION: "",
                         OUTPUT_ERROR: OUTPUT_ERROR_SENTENCE_STRUCTURE
                       }]
                
            
            lemma = sentence_structure[VERB_LEMMA]
            definition = "" # dictionary definition for the lemma
            if lemma != "":
                # dictionary_df = None # initial value
                
                if sentence_structure[VERB_TYPE] == FST_VTA:
                    dictionary_df = core_environment.get(ENV_VTA_DICTIONARY_DF)
                elif sentence_structure[VERB_TYPE] == FST_VTI:
                    dictionary_df = core_environment.get(ENV_VTI_DICTIONARY_DF)
                elif sentence_structure[VERB_TYPE] == FST_VAI:
                    dictionary_df = core_environment.get(ENV_VAI_DICTIONARY_DF)
                elif sentence_structure[VERB_TYPE] == FST_VII:
                    dictionary_df = core_environment.get(ENV_VII_DICTIONARY_DF)

                if (dictionary_df is not None) and isinstance(dictionary_df, DataFrame):
                    query_result = dictionary_df.query(f"{DATA_LEMMA} == @lemma")
                    if len(query_result) > 0:
                        definition = query_result.iloc[0][DATA_DEFINITION]
                else:
                    # no valid dataframe provided
                        definition = ""
            
            if definition != "":
                sentences = vta_build_en_sentence(sentence_structure, dictionary_template_dataframe=dictionary_df)
            else:
                sentences = []

            # build JSON objects for output
            if type(sentences) == list and len(sentences) > 0:
                for translation in sentences:
                    translation_item = {OUTPUT_INPUT: input,
                                        OUTPUT_DEFINITION: definition,
                                        OUTPUT_FST_OUTPUT: fst_output_item,
                                        OUTPUT_SENT_STRUCTURE: sentence_structure,
                                        OUTPUT_TRANSLATION: translation
                                       }
                    output.append(translation_item)
            elif type(sentences) == list and len(sentences) == 0: 
                # likely lemma not found in the dictionary dataframe
                translation_item = {OUTPUT_INPUT: input,
                                    OUTPUT_DEFINITION: definition,
                                    OUTPUT_FST_OUTPUT: fst_output_item,
                                    OUTPUT_SENT_STRUCTURE: sentence_structure,
                                    OUTPUT_TRANSLATION: "",
                                    OUTPUT_ERROR: OUTPUT_ERROR_LEMMA_NOT_FOUND
                                    }
                output.append(translation_item)
                
            # end of for loop
    
    return output
