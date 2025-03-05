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

    # return core_env


def test_fst_parser():
    """
       Test FST parser up and down functions
    """
    logger.debug("Test FST parser up_analysis() and down_generation() functions...")

    assert core_env[ENV_FST] is not None
    assert type(core_env[ENV_FST]) == Fst

    # Test up_analysis function
    logger.debug("FST Type = %s", type(core_env[ENV_FST]))
    result = list(core_env[ENV_FST].up_analysis("giwaabamin"))
    for analysis in result:
        logger.debug(analysis)
    assert len(result) > 0
    assert result[0].output_string.startswith("waabam+VTA")

    # Test down_generation function
    parsed_word = "waabam+VTA+Ind+Pos+Neu+1SgSubj+2SgObj"
    result = list(core_env[ENV_FST].down_generation(parsed_word))
    for item in result:
        logger.debug(item)
    assert len(result) > 0
    assert result[0].output_string.startswith("giwaabamin")


def test_loading_datasets():
    """
        Test loading dictionary and templates from csv files
    """
    logger.debug("Test loading templates from csv files...")
    global core_env

    # load templates from csv files
    template_filenames = {
        ENV_ALL_DICTIONARY_DF: "templates/ob_en_dict.csv",
        ENV_VTA_DICTIONARY_DF: "templates/vta_dict.csv",
        ENV_VTI_DICTIONARY_DF: "templates/vti_dict.csv",
        ENV_VAI_DICTIONARY_DF: "templates/vai_dict.csv",
        ENV_VII_DICTIONARY_DF: "templates/vii_dict.csv",
    }    
    core_env = oj_to_en.load_templates(environment=core_env, filenames=template_filenames)
    # core_env = oj_to_en.load_templates(environment=core_env)

    # print(type(core_env[ENV_ALL_DICTIONARY_DF]))
    assert core_env[ENV_ALL_DICTIONARY_DF] is not None
    assert core_env[ENV_VTA_DICTIONARY_DF] is not None
    assert core_env[ENV_VTI_DICTIONARY_DF] is not None
    assert core_env[ENV_VAI_DICTIONARY_DF] is not None
    assert core_env[ENV_VII_DICTIONARY_DF] is not None

    assert type(core_env[ENV_ALL_DICTIONARY_DF]) == DataFrame
    assert type(core_env[ENV_VTA_DICTIONARY_DF]) == DataFrame
    assert type(core_env[ENV_VTI_DICTIONARY_DF]) == DataFrame
    assert type(core_env[ENV_VAI_DICTIONARY_DF]) == DataFrame
    assert type(core_env[ENV_VII_DICTIONARY_DF]) == DataFrame


print("Running tests for Ojibwe-translation package: Initialization")
core_env = dict()

test_initialize()
test_fst_parser()
test_loading_datasets()

print("Tests passed")



