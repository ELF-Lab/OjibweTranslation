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

    # return core_environment


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

    # print(type(core_environment[ENV_ALL_DICTIONARY_DF]))
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

def test_simple_sentences():
    """
        Test building simple sentences with verbs
    """
    # VTA
    logger.debug("Testing full sentence building with VTA verb...")
    sentence_structure = oj_to_en.fst_verb_analyzer("PVTense/gii+niimaakwa'+VTA+Ind+Pos+Neu+3SgSubj+3SgObj")
    result = oj_to_en.build_en_sentence(sentence_structure, environment=core_environment)

    assert len(result[0]) > 0
    assert result[0].lower().startswith("he/she picked him/her/it up")
    logger.debug(result)

    # VTI
    logger.debug("Testing full sentence building with VTI verb...")
    sentence_structure = oj_to_en.fst_verb_analyzer("PVTense/gii+boozwebinan+VTI+Ind+Neg+Neu+1SgSubj+0SgObj")
    result = oj_to_en.build_en_sentence(sentence_structure, environment=core_environment)

    assert len(result[0]) > 0
    assert result[0].lower().startswith("i did not throw it aboard")
    logger.debug(result)

    # VAI
    logger.debug("Testing full sentence building with VAI verb...")
    sentence_structure = oj_to_en.fst_vai_verb_analyzer("onibiimi+VAI+Ind+Pos+Neu+1SgSubj")
    result = oj_to_en.build_en_sentence(sentence_structure, environment=core_environment)

    assert len(result[0]) > 0
    assert result[0].lower().startswith("i have water")
    logger.debug(result)

    # VII
    logger.debug("Testing full sentence building with VII verb...")
    sentence_structure = oj_to_en.fst_verb_analyzer("minjimishkoode+VII+Ind+Pos+Neu+0SgSubj")
    result = oj_to_en.build_en_sentence(sentence_structure, environment=core_environment)

    assert len(result[0]) > 0
    assert result[0].lower().startswith(f"it ({INANIMATE_TAG}) is pinned down")
    logger.debug(result)


def test_complex_sentences():
    """
        Test building more complex sentences with verbs, tenses and negation
    """
    logger.debug("Testing more complex full sentence building with various tense...")
    # test with past tense (gii) + negation
    sentence_structure = oj_to_en.fst_verb_analyzer("PVTense/gii+niimaakwa'+VTA+Ind+Neg+Neu+3SgSubj+3SgObj")
    result = oj_to_en.build_en_sentence(sentence_structure, environment=core_environment)

    assert len(result[0]) > 0
    assert result[0].lower().startswith("he/she did not pick him/her/it")

    # test with future wii (desire) mode
    sentence_structure = oj_to_en.fst_verb_analyzer("PVTense/wii+niimaakwa'+VTA+Ind+Pos+Neu+3SgSubj+3SgObj")
    result = oj_to_en.build_en_sentence(sentence_structure, environment=core_environment)
    assert result[0].lower().startswith("he/she wants to pick him/her/it up")

    # test with future wii (wish) + negative + neutral ( -> do not want to something )
    sentence_structure = oj_to_en.fst_verb_analyzer("PVTense/wii+onibiimi+VAI+Ind+Neg+Neu+1SgSubj")
    result = oj_to_en.build_en_sentence(sentence_structure, environment=core_environment)
    assert result[0].lower().startswith("i do not want to have water")


    # test with future wii (wish) + dubitative tense ( -> might do something )
    sentence_structure = oj_to_en.fst_verb_analyzer("PVTense/wii+boozwebinan+VTI+Ind+Pos+Dub+1SgSubj+0SgObj")
    result = oj_to_en.build_en_sentence(sentence_structure, environment=core_environment)
    assert result[0].lower().startswith("i might throw it")

    # test with future da / ga (will) 
    sentence_structure = oj_to_en.fst_verb_analyzer("PVTense/da+minjimishkoode+VII+Ind+Pos+Neu+0SgSubj")
    result = oj_to_en.build_en_sentence(sentence_structure, environment=core_environment)
    assert result[0].lower().startswith(f"it ({INANIMATE_TAG}) will be pinned down")

    # test with future wii (wish) + negative + neutral ( -> do not want to something )
    sentence_structure = oj_to_en.fst_verb_analyzer("PVTense/wii+niimaakwa'+VTA+Ind+Neg+Neu+3SgSubj+3SgObj")
    result = oj_to_en.build_en_sentence(sentence_structure, environment=core_environment)
    assert result[0].lower().startswith("he/she does not want to pick him/her/it up")

    # test with past tense (gii) + Conj
    sentence_structure = oj_to_en.fst_verb_analyzer("PVTense/gii+onibiimi+VAI+Cnj+Pos+Neu+3PlSubj")
    result = oj_to_en.build_en_sentence(sentence_structure, environment=core_environment)
    assert result[0].lower().startswith("if/when they had water")

    # test with past tense (gii) + Conj
    sentence_structure = oj_to_en.fst_verb_analyzer("PVTense/gii+minjimishkoode+VII+Cnj+Pos+Neu+0SgSubj")
    result = oj_to_en.build_en_sentence(sentence_structure, environment=core_environment)
    assert result[0].lower().startswith(f"if/when it ({INANIMATE_TAG}) was pinned down")    

    # test with future da / ga (will) + negation
    sentence_structure = oj_to_en.fst_verb_analyzer("PVTense/da+onibiimi+VAI+Ind+Neg+Neu+3SgSubj")
    result = oj_to_en.build_en_sentence(sentence_structure, environment=core_environment)
    assert result[0].lower().startswith("he/she will not have water")


def test_simple_end_to_end_translation():
    """
        Test simple end-to-end translation, from inflected Ojibwe verbs to English phrases / sentences 
    """
    logger.debug("Testing simple end-to-end translations...")

    # VTA verb
    input = "niniimaakwa'waa" # I pick it up
    logger.debug(f"VTA Input = {input}")
    result = oj_to_en.oj2en_builder(input, environment=core_environment)
    logger.debug(f"Outputs = {result}")
    assert len(result) > 0
    assert OUTPUT_INPUT in result[0].keys()
    assert OUTPUT_TRANSLATION in result[0].keys()
    assert OUTPUT_DEFINITION in result[0].keys()
    assert result[1][OUTPUT_INPUT] == input.lower()
    assert result[1][OUTPUT_FST_OUTPUT].lower().startswith("niimaakwa'+vta") 
    assert result[1][OUTPUT_TRANSLATION].lower().startswith(f"i pick him/her/it ({PROXIMATE_TAG}) up")
    
    # VTI verb
    input = "wiikwaabiiginang" # 
    logger.debug(f"VTI Input = {input}")
    result = oj_to_en.oj2en_builder(input, environment=core_environment)
    logger.debug(f"Outputs = {result}")
    assert len(result) > 0
    assert result[1][OUTPUT_INPUT] == input.lower()
    assert result[1][OUTPUT_FST_OUTPUT].lower().startswith("wiikwaabiiginan+vti+cnj") 
    assert result[1][OUTPUT_TRANSLATION].lower().startswith(f"if/when he/she ({PROXIMATE_TAG}) pulls it")

    # VAI verb
    input = "nimaakishin"
    logger.debug(f"VAI Input = {input}")
    result = oj_to_en.oj2en_builder(input, environment=core_environment)
    logger.debug(f"Outputs = {result}")
    assert len(result) > 0
    assert result[0][OUTPUT_INPUT] == input.lower()
    assert result[0][OUTPUT_FST_OUTPUT].lower().startswith("maakishin+vai") 
    assert result[0][OUTPUT_TRANSLATION].lower().startswith("i am injured by falling")

    # VII verb
    input = "wewebaasing"
    logger.debug(f"VII Input = {input}")
    result = oj_to_en.oj2en_builder(input, environment=core_environment)
    logger.debug(f"Outputs = {result}")
    assert len(result) > 0
    assert result[0][OUTPUT_INPUT] == input.lower()
    assert result[0][OUTPUT_FST_OUTPUT].lower().startswith("wewebaasin+vii") 
    assert result[0][OUTPUT_TRANSLATION].lower().startswith(f"if/when it ({INANIMATE_TAG}) is blown back")


print("Running tests for Ojibwe-translation package: Sentence building")

test_initialize()
test_fst_parser()
test_loading_datasets()
test_simple_sentences()
test_complex_sentences()
test_simple_end_to_end_translation()

print("All tests passed")
