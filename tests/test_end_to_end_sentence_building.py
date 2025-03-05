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

    global core_environment

    data_folder_path = './data/'

    # Initialize new core environment object
    core_environment = oj_to_en.initialize_environment(data_folder_path)
    assert type(core_environment) == dict 

    # Load FST parser
    core_environment = oj_to_en.load_foma(environment=core_environment, file_name="foma_bin/ojibwe.att")
    assert core_environment[ENV_FST] is not None
    assert type(core_environment[ENV_FST]) == Fst
    assert core_environment[ENV_DATA_PATH] == data_folder_path


def test_fst_parser():
    """
       Test FST parser up and down functions
    """
    logger.debug("Test FST parser up_analysis() and down_generation() functions...")

    assert core_environment[ENV_FST] is not None
    assert type(core_environment[ENV_FST]) == Fst

    # Test up_analysis function
    logger.debug("FST Type = %s", type(core_environment[ENV_FST]))
    result = list(core_environment[ENV_FST].up_analysis("giwaabamin"))
    for analysis in result:
        logger.debug(analysis)
    assert len(result) > 0
    assert result[0].output_string.startswith("waabam+VTA")

    # Test down_generation function
    parsed_word = "waabam+VTA+Ind+Pos+Neu+1SgSubj+2SgObj"
    result = list(core_environment[ENV_FST].down_generation(parsed_word))
    for item in result:
        logger.debug(item)
    assert len(result) > 0
    assert result[0].output_string.startswith("giwaabamin")


def test_loading_datasets():
    """
        Test loading dictionary and templates from csv files
    """
    logger.debug("Test loading templates from csv files...")
    global core_environment
    
    # load templates from csv files    
    template_filenames = {
        ENV_ALL_DICTIONARY_DF: "templates/ob_en_dict.csv",
        ENV_VTA_DICTIONARY_DF: "templates/vta_dict.csv",
        ENV_VTI_DICTIONARY_DF: "templates/vti_dict.csv",
        ENV_VAI_DICTIONARY_DF: "templates/vai_dict.csv",
        ENV_VII_DICTIONARY_DF: "templates/vii_dict.csv",
    }  
    core_environment = oj_to_en.load_templates(environment=core_environment, filenames=template_filenames)

    assert core_environment[ENV_ALL_DICTIONARY_DF] is not None
    assert core_environment[ENV_VTA_DICTIONARY_DF] is not None
    assert core_environment[ENV_VTI_DICTIONARY_DF] is not None
    assert core_environment[ENV_VAI_DICTIONARY_DF] is not None
    assert core_environment[ENV_VII_DICTIONARY_DF] is not None

    assert type(core_environment[ENV_ALL_DICTIONARY_DF]) == DataFrame
    assert type(core_environment[ENV_VTA_DICTIONARY_DF]) == DataFrame
    assert type(core_environment[ENV_VTI_DICTIONARY_DF]) == DataFrame
    assert type(core_environment[ENV_VAI_DICTIONARY_DF]) == DataFrame
    assert type(core_environment[ENV_VII_DICTIONARY_DF]) == DataFrame


def test_vta_verbs():
    """
        Test more complex VTA verbs with various mode and tenses
    """
    logger.debug("Testing end-to-end translation for VTA verbs")


    # VTA verb
    input = "odaadawa'amaan" # he/she goes with him/her/it in a boat
    logger.debug(f"VTA Input = {input}")
    result = oj_to_en.oj2en_builder(input, environment=core_environment)
    logger.debug(f"Outputs = {result}")
    assert len(result) > 0
    assert OUTPUT_INPUT in result[0].keys()
    assert OUTPUT_TRANSLATION in result[0].keys()
    assert OUTPUT_DEFINITION in result[0].keys()
    assert result[0][OUTPUT_INPUT] == input.lower()
    assert result[0][OUTPUT_FST_OUTPUT].lower().startswith("aadawa'am+vta") 
    assert result[0][OUTPUT_TRANSLATION].lower().startswith(f"he/she ({PROXIMATE_TAG}) goes with him/her/it ({OBVIATIVE_TAG}) in a boat")


    input = "aadawa'amaasig" # with conjunction + negation 
    logger.debug(f"VTA Input = {input}")
    result = oj_to_en.oj2en_builder(input, environment=core_environment)
    logger.debug(f"Outputs = {result}")
    assert len(result) > 0
    assert result[0][OUTPUT_INPUT] == input.lower()
    assert result[0][OUTPUT_FST_OUTPUT].lower().startswith("aadawa'am+vta+cnj") 
    assert result[0][OUTPUT_TRANSLATION].lower().startswith(f"if/when he/she ({PROXIMATE_TAG}) does not go with him/her/it ({OBVIATIVE_TAG}) in a boat")

    input = "gii-aadawa'amaasig" # with conjunction + negation + past tense
    logger.debug(f"VTA Input = {input}")
    result = oj_to_en.oj2en_builder(input, environment=core_environment)
    logger.debug(f"Outputs = {result}")
    assert len(result) > 0
    assert result[0][OUTPUT_INPUT] == input.lower()
    assert result[0][OUTPUT_FST_OUTPUT].lower().startswith("pvtense/gii+aadawa'am+vta+cnj") 
    assert result[0][OUTPUT_TRANSLATION].lower().startswith(f"if/when he/she ({PROXIMATE_TAG}) did not go with him/her/it ({OBVIATIVE_TAG}) in a boat")


    input = "aadawa'am" # imperative
    logger.debug(f"VTA Input = {input}")
    result = oj_to_en.oj2en_builder(input, environment=core_environment)
    logger.debug(f"Outputs = {result}")
    assert len(result) > 0
    assert result[0][OUTPUT_INPUT] == input.lower()
    assert result[0][OUTPUT_FST_OUTPUT].lower().startswith("aadawa'am+vta+imp") 
    assert result[0][OUTPUT_TRANSLATION].lower().startswith(f"(please) go with him/her/it ({PROXIMATE_TAG}) in a boat")

def test_vti_verbs():
    """
        Test more complex VTA verbs with various mode and tenses
    """
    logger.debug("Testing end-to-end translation for VTA verbs")
    # VTI verb
    input = "nindagwaa'aan" # 
    logger.debug(f"VTI Input = {input}")
    result = oj_to_en.oj2en_builder(input, environment=core_environment)
    logger.debug(f"Outputs = {result}")
    assert len(result) > 0
    assert result[0][OUTPUT_INPUT] == input.lower()
    assert result[0][OUTPUT_FST_OUTPUT].lower().startswith("agwaa'an+vti") 
    assert result[0][OUTPUT_TRANSLATION].lower().startswith("i take it off the water")


    input = "nindagwaa'anziin" # with negation
    logger.debug(f"VTI Input = {input}")
    result = oj_to_en.oj2en_builder(input, environment=core_environment)
    logger.debug(f"Outputs = {result}")
    assert len(result) > 0
    assert result[0][OUTPUT_INPUT] == input.lower()
    assert result[0][OUTPUT_FST_OUTPUT].lower().startswith("agwaa'an+vti") 
    assert result[0][OUTPUT_TRANSLATION].lower().startswith("i do not take it off the water")

    input = "gii-agwaa'anzig" # with conjunction + negation + past tense
    logger.debug(f"VTI Input = {input}")
    result = oj_to_en.oj2en_builder(input, environment=core_environment)
    logger.debug(f"Outputs = {result}")
    assert len(result) > 0
    assert result[0][OUTPUT_INPUT] == input.lower()
    assert result[0][OUTPUT_FST_OUTPUT].lower().startswith("pvtense/gii+agwaa'an+vti+cnj") 
    assert result[0][OUTPUT_TRANSLATION].lower().startswith(f"if/when he/she ({PROXIMATE_TAG}) did not take it off the water")

    input = "ninga-agwaa'anziin" # with future tense + negation
    logger.debug(f"VTI Input = {input}")
    result = oj_to_en.oj2en_builder(input, environment=core_environment)
    logger.debug(f"Outputs = {result}")
    assert len(result) > 0
    assert result[0][OUTPUT_INPUT] == input.lower()
    assert result[0][OUTPUT_FST_OUTPUT].lower().startswith("pvtense/ga+agwaa'an+vti") 
    assert result[0][OUTPUT_TRANSLATION].lower().startswith("i will not take it off the water")

    input = "agwaa'an" # imperative 
    logger.debug(f"VTI Input = {input}")
    result = oj_to_en.oj2en_builder(input, environment=core_environment)
    logger.debug(f"Outputs = {result}")
    assert len(result) > 0
    assert result[0][OUTPUT_INPUT] == input.lower()
    assert result[0][OUTPUT_FST_OUTPUT].lower().startswith("agwaa'an+vti+imp") 
    assert result[0][OUTPUT_TRANSLATION].lower().startswith("(please) take it off the water")


def test_vai_verbs():
    """
        Test more complex VTA verbs with various mode and tenses
    """
    logger.debug("Testing end-to-end translation for VAI verbs")

    # VAI verb
    input = "abweninjii"
    logger.debug(f"VAI Input = {input}")
    result = oj_to_en.oj2en_builder(input, environment=core_environment)
    logger.debug(f"Outputs = {result}")
    assert len(result) > 0
    assert result[0][OUTPUT_INPUT] == input.lower()
    assert result[0][OUTPUT_FST_OUTPUT].lower().startswith("abweninjii+vai") 
    assert result[0][OUTPUT_TRANSLATION].lower().startswith(f"he/she ({PROXIMATE_TAG}) has a sweaty hand")

    input = "abweninjiisiin" # with negation
    logger.debug(f"VAI Input = {input}")
    result = oj_to_en.oj2en_builder(input, environment=core_environment)
    logger.debug(f"Outputs = {result}")
    assert len(result) > 0
    assert result[0][OUTPUT_INPUT] == input.lower()
    assert result[0][OUTPUT_FST_OUTPUT].lower().startswith("abweninjii+vai") 
    assert result[0][OUTPUT_TRANSLATION].lower().startswith(f"he/she ({PROXIMATE_TAG}) does not have a sweaty hand")

    input = "gii-abweninjiisiin" # with negation + past tense
    logger.debug(f"VAI Input = {input}")
    result = oj_to_en.oj2en_builder(input, environment=core_environment)
    logger.debug(f"Outputs = {result}")
    assert len(result) > 0
    assert result[0][OUTPUT_INPUT] == input.lower()
    assert result[0][OUTPUT_FST_OUTPUT].lower().startswith("pvtense/gii+abweninjii+vai") 
    assert result[0][OUTPUT_TRANSLATION].lower().startswith(f"he/she ({PROXIMATE_TAG}) did not have a sweaty hand")

    input = "wii-abweninjiisiin" # with future/wish tense + negation
    logger.debug(f"VAI Input = {input}")
    result = oj_to_en.oj2en_builder(input, environment=core_environment)
    logger.debug(f"Outputs = {result}")
    assert len(result) > 0
    assert result[0][OUTPUT_INPUT] == input.lower()
    assert result[0][OUTPUT_FST_OUTPUT].lower().startswith("pvtense/wii+abweninjii+vai") 
    assert result[0][OUTPUT_TRANSLATION].lower().startswith(f"he/she ({PROXIMATE_TAG}) does not want to have a sweaty hand")

    input = "abweninjiid" # conjunction mode 
    logger.debug(f"VAI Input = {input}")
    result = oj_to_en.oj2en_builder(input, environment=core_environment)
    logger.debug(f"Outputs = {result}")
    assert len(result) > 0
    assert result[0][OUTPUT_INPUT] == input.lower()
    assert result[0][OUTPUT_FST_OUTPUT].lower().startswith("abweninjii+vai+cnj") 
    assert result[0][OUTPUT_TRANSLATION].lower().startswith(f"if/when he/she ({PROXIMATE_TAG}) has a sweaty hand")
    
    input = "ninibaa" 
    logger.debug(f"VAI Input = {input}")
    result = oj_to_en.oj2en_builder(input, environment=core_environment)
    logger.debug(f"Outputs = {result}")
    assert len(result) > 0
    assert result[0][OUTPUT_INPUT] == input.lower()
    assert result[0][OUTPUT_FST_OUTPUT].lower().startswith("nibaa+vai+ind+pos") 
    assert result[1][OUTPUT_TRANSLATION].lower().startswith(f"i am asleep")
    assert result[0][OUTPUT_TRANSLATION].lower().startswith(f"i sleep")
    

def test_vii_verbs():
    """
        Test more complex VTA verbs with various mode and tenses
    """
    logger.debug("Testing end-to-end translation for VII verbs")

    # VII verb
    input = "minjimishkoode"
    logger.debug(f"VII Input = {input}")
    result = oj_to_en.oj2en_builder(input, environment=core_environment)
    logger.debug(f"Outputs = {result}")
    assert len(result) > 0
    assert result[0][OUTPUT_INPUT] == input.lower()
    assert result[0][OUTPUT_FST_OUTPUT].lower().startswith("minjimishkoode+vii") 
    assert result[0][OUTPUT_TRANSLATION].lower().startswith(f"it ({INANIMATE_TAG}) is pinned down")

    input = "minjimishkoodesinoon" # with negation + plural
    logger.debug(f"VII Input = {input}")
    result = oj_to_en.oj2en_builder(input, environment=core_environment)
    logger.debug(f"Outputs = {result}")
    assert len(result) > 0
    assert result[0][OUTPUT_INPUT] == input.lower()
    assert result[0][OUTPUT_FST_OUTPUT].lower().startswith("minjimishkoode+vii") 
    assert result[0][OUTPUT_TRANSLATION].lower().startswith(f"they ({INANIMATE_TAG}) are not pinned down")

    input = "gii-minjimishkoodesinoon" # with negation + past tense
    logger.debug(f"VII Input = {input}")
    result = oj_to_en.oj2en_builder(input, environment=core_environment)
    logger.debug(f"Outputs = {result}")
    assert len(result) > 0
    assert result[0][OUTPUT_INPUT] == input.lower()
    assert result[0][OUTPUT_FST_OUTPUT].lower().startswith("pvtense/gii+minjimishkoode+vii") 
    assert result[0][OUTPUT_TRANSLATION].lower().startswith(f"they ({INANIMATE_TAG}) were not pinned down")

    input = "wii-minjimishkoodesinoon" # with future/wish tense + negation
    logger.debug(f"VII Input = {input}")
    result = oj_to_en.oj2en_builder(input, environment=core_environment)
    logger.debug(f"Outputs = {result}")
    assert len(result) > 0
    assert result[0][OUTPUT_INPUT] == input.lower()
    assert result[0][OUTPUT_FST_OUTPUT].lower().startswith("pvtense/wii+minjimishkoode+vii") 
    assert result[0][OUTPUT_TRANSLATION].lower().startswith(f"they ({INANIMATE_TAG}) do not want to be pinned down")

    input = "wii-minjimishkoodesinog" # conjunction mode + future/wish + negation
    logger.debug(f"VTI Input = {input}")
    result = oj_to_en.oj2en_builder(input, environment=core_environment)
    logger.debug(f"Outputs = {result}")
    assert len(result) > 0
    assert result[0][OUTPUT_INPUT] == input.lower()
    assert result[0][OUTPUT_FST_OUTPUT].lower().startswith("pvtense/wii+minjimishkoode+vii+cnj") 
    assert result[0][OUTPUT_TRANSLATION].lower().startswith(f"if/when they ({INANIMATE_TAG}) do not want to be pinned down")


def test_edge_cases():
    """
        Test edge cases such as non-existence words, word not in dictionary, etc
    """
    # non-existent word
    input = "hello"
    logger.debug(f"(Non-existence word) Input = {input}")
    result = oj_to_en.oj2en_builder(input, environment=core_environment)
    logger.debug(f"Outputs = {result}")
    assert len(result) > 0
    assert isinstance(result[0], dict) 
    assert result[0].get(OUTPUT_ERROR, "").startswith(OUTPUT_ERROR_FST_PARSE)

    # not valid Ojibwe word
    input = "gii-waabamig"
    logger.debug(f"(Not valid Ojibwe word) Input = {input}")
    result = oj_to_en.oj2en_builder(input, environment=core_environment)
    logger.debug(f"Outputs = {result}")
    assert len(result) > 0
    assert isinstance(result[0], dict) 
    assert result[0].get(OUTPUT_ERROR, "").startswith(OUTPUT_ERROR_FST_PARSE)

    # word in FST, but not in test dictionary template
    input = "waagibizh" # "bend something with hands"
    logger.debug(f"(Ojibwe word not in dictionary) Input = {input}")
    result = oj_to_en.oj2en_builder(input, environment=core_environment)
    logger.debug(f"Outputs = {result}")
    assert len(result) > 0
    assert isinstance(result[0], dict) 
    assert result[0].get(OUTPUT_ERROR, "").startswith(OUTPUT_ERROR_LEMMA_NOT_FOUND)

    
    # word in FST, but not in test dictionary template
    input = "agaasadegamaa" # VII "it is a narrow lake"
    logger.debug(f"(Ojibwe word not in dictionary) Input = {input}")
    result = oj_to_en.oj2en_builder(input, environment=core_environment)
    logger.debug(f"Outputs = {result}")
    assert len(result) > 0
    assert isinstance(result[0], dict) 
    assert result[0].get(OUTPUT_ERROR, "").startswith(OUTPUT_ERROR_LEMMA_NOT_FOUND)

print("Running tests for Ojibwe-translation package: Sentence building")

test_initialize()
test_fst_parser()
test_loading_datasets()
test_vta_verbs()
test_vti_verbs()
test_vai_verbs()
test_vii_verbs()

test_edge_cases()

print("All tests passed")
