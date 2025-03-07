# This is the web-app for Ojibwe-English translation package demo.
# Please use `pip -r requirements.txt`
# Or pip `install nicegui` to install nicegui package
from nicegui import ui 
import ojibwe_translation as oj2en
from ojibwe_translation.oj_constants import *
import json 

def initialize(data_folder_path) -> dict:
    """
        Initialize Ojibwe translation core-environment variable

    Args:
        data_folder_path (_type_): path to the data folder containing FST, dictionary and template data

    Returns:
        dict: core environment dictionary containing FST parser and necessary dataframes
    """
    core_environment = oj2en.initialize_environment(data_path=data_folder_path)     # initialize blank core-environment variables
    core_environment = oj2en.load_foma(environment=core_environment,                # load FST parser
                                       file_name="foma_bin/ojibwe.att")             
    core_environment = oj2en.load_templates(environment=core_environment)           # load template data
    
    return core_environment

def translate(ojibwe_word:str, explanation: bool=True) -> list:
    """Translate Ojibwe verb -> English using ojibwe_translation package

    Args:
        ojibwe_word (str): Inflected Ojibwe verb (e.g. giwaabamin)

    Returns:
        str: English translation
    """
    if ojibwe_word is None or ojibwe_word.strip() == "":
        return f"Please enter an Ojibwe verb to translate."
    
    translations = oj2en.oj2en_builder(inflected_ojibwe_word=ojibwe_word, environment=core_environment)

    output = []
    output.append("**Translations:**")

    if translations is None:
        return "**Sorry, I'm not unable to translate this.**"
    
    for translation_item in translations:
        if explanation:
            opd_base_url = "https://ojibwe.lib.umn.edu/search?utf8=%E2%9C%93&commit=Search&type=ojibwe"   # base endpoint for Ojibwe People Dictionary
            lemma = translation_item[OUTPUT_SENT_STRUCTURE].get(VERB_LEMMA, '')
            if lemma:
                opd_link = f"[(see in OPD dictionary)]({opd_base_url}&q={lemma})"
            else:
                opd_link = "" 
            # produce more detailed explanation (FST analyses, lemma definition, etc)
            item_text = f"\n**FST analysis:** \n&emsp;{translation_item.get(OUTPUT_FST_OUTPUT, '')}" + \
                        (f"\n**Lemma definition**: \n&emsp;{translation_item[OUTPUT_SENT_STRUCTURE].get(VERB_LEMMA, '')} {opd_link} = {translation_item.get(OUTPUT_DEFINITION)}"
                        if translation_item.get(OUTPUT_DEFINITION, "") != ""
                        else ""
                        ) + \
                        (f"\n**Translation:** \n&emsp;{translation_item.get(OUTPUT_TRANSLATION, '')}" 
                        if translation_item.get(OUTPUT_TRANSLATION, "") != ""
                        else ""
                        ) + \
                        (f"\n**Error:** \n&emsp;{translation_item.get(OUTPUT_ERROR, '')}" 
                        if translation_item.get(OUTPUT_ERROR, "") != ""
                        else "") + \
                        (f"\n**Message:** \n&emsp;{translation_item.get(OUTPUT_MESSAGE, '')}" 
                        if translation_item.get(OUTPUT_MESSAGE, "") != ""
                        else "")
        else:
            item_text = (f"- {translation_item.get(OUTPUT_TRANSLATION, '')}" 
                        if translation_item.get(OUTPUT_TRANSLATION, "") != ""
                        else ""
                        ) + \
                        (f"- (Error: {translation_item.get(OUTPUT_ERROR, '')})" 
                        if translation_item.get(OUTPUT_ERROR, "") != ""
                        else "")

        output.append(item_text)
        
    # show a short message if the translator returns extra message
    if translations[0].get("message", "") != "":
        ui.notification(translations[0].get("message", ""), close_button=True, type="warning", timeout=5)
        
    return "\n".join(output)

@ui.page("/")
def home_page():
    ui.markdown("#### Ojibwe → English Translation Demo")
    ui.separator()

    ui.markdown("Please enter inflected Ojibwe verb bellow:") 
    ui.markdown("Some examples: odaadawa'amaan, aadawa'am, nindagwaa'aan, abweninjii, gaawiin gii-abweninjiisiin")

    # store the option to display detailed explanations or not
    page_states = {"require_explanations":False,
                   "feeback_section_visible": False,
                   }
    
    # translate lambda function
    translate_function = lambda: translation_text.set_content(translate(ojibwe_input.value, 
                                                                        explanation=page_states["require_explanations"]))
    
    ojibwe_input = (ui.input(value="giwaabamin")
                    .props("clearable")
                    .on("keydown.enter", translate_function)
                    )
    
    ui.switch("Provide explanations", value=False).bind_value_to(page_states, "require_explanations")
    ui.button("Translate", color="orange", icon="translate", on_click=translate_function) 

    translation_text = ui.markdown().style("white-space:pre-wrap;") # support multiple-line markdown
    
def initialization():
    # Initialize FST parser and loading templates  
    data_path = "./data/samples/"
    print("Loading FST Parser and templates...", end="")
    global core_environment 
    core_environment = initialize(data_folder_path=data_path)
    assert core_environment[ENV_FST] is not None 
    assert core_environment[ENV_VTA_DICTIONARY_DF] is not None
    assert core_environment[ENV_VTI_DICTIONARY_DF] is not None
    assert core_environment[ENV_VAI_DICTIONARY_DF] is not None
    assert core_environment[ENV_VII_DICTIONARY_DF] is not None
    print("OK")
    
    ui.run(title="Ojibwe Translation")

initialization()
