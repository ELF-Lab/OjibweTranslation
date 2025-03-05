import ojibwe_translation.oj_en_translation as oj_to_en
from ojibwe_translation.oj_constants import *
from ojibwe_translation import logger
from fst_runtime.fst import Fst
from pandas import DataFrame


def test_initialize():
    """
        initialize translation variables and data
    """
    logger.debug("Test initializing FST parser...")

    global core_env

    data_folder_path = './data/'

    # Initialize new core environment object
    core_env = oj_to_en.initialize_environment(data_folder_path)
    assert type(core_env) == dict 

    # Load FST parser
    core_env = oj_to_en.load_foma(environment=core_env, file_name="foma_bin/ojibwe.att")
    assert core_env[ENV_FST] is not None
    assert type(core_env[ENV_FST]) == Fst
    assert core_env[ENV_DATA_PATH] == data_folder_path

def test_ojibwe_word_to_fst_tags():
    """
        Test parsing ojibwe word into separated fst tags
    """
    logger.debug("Test parsing inflected verb to fst tags...")

    inflected_word = "waabam"
    parsed_strings = oj_to_en.inflected_ojibwe_word_process_inflected_form(inflected_word=inflected_word, fst=core_env[ENV_FST])

    logger.debug(parsed_strings)
    assert len(parsed_strings) > 0
    assert parsed_strings[0].startswith("waabam+VTA+Imp")

    # Test VTA verb
    fst_parsed_string = "waabam+VTA+Ind+Pos+Neu+1SgSubj+2SgObj"
    sentence_structure = oj_to_en.fst_verb_analyzer(fst_analysis_string=fst_parsed_string)
    # logger.debug(sentence_structure)

    assert sentence_structure["verb"] == "waabam"
    assert sentence_structure["polarity"] == "pos"
    assert sentence_structure["verb_type"] == "vta"

    # Test VTI verb
    fst_parsed_string = "waabandan+VTI+Ind+Pos+Neu+1SgSubj+0SgObj"
    sentence_structure = oj_to_en.fst_verb_analyzer(fst_analysis_string=fst_parsed_string)
    # logger.debug(sentence_structure)

    assert sentence_structure["verb"] == "waabandan"
    assert sentence_structure["polarity"] == "pos"
    assert sentence_structure["verb_type"] == "vti"

    # Test VAI verb
    fst_parsed_string = "namadabi+VAI+Imp+Sim+2SgSubj"
    sentence_structure = oj_to_en.fst_verb_analyzer(fst_analysis_string=fst_parsed_string)
    # logger.debug(sentence_structure)

    assert sentence_structure["verb"] == "namadabi"
    assert sentence_structure["order"] == "imp"
    assert sentence_structure["verb_type"] == "vai"

    # Test VII verb
    fst_parsed_string = "agaasaa+VII+Ind+Pos+Neu+0SgSubj"
    sentence_structure = oj_to_en.fst_verb_analyzer(fst_analysis_string=fst_parsed_string)
    # logger.debug(sentence_structure)

    assert sentence_structure["verb"] == "agaasaa"
    assert sentence_structure["polarity"] == "pos"
    assert sentence_structure["verb_type"] == "vii"


print("Running tests for Ojibwe-translation package: FST Parser and Sentence analyzer")
core_env = dict()

test_initialize()
test_ojibwe_word_to_fst_tags()

print("Tests passed")
