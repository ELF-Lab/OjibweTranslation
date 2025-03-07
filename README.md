# OjibweTranslation

This repository houses a basic translation tool for Ojibwe verbs

### (Documentation works in progress.)

### Project Contributors:
- Miikka Silfverberg
- Christopher Hammerly
- Minh Nguyen
- Scott Parkhill


### Package description
ELF-Lab OjibweTranslation is a Python package to analyze and translate inflected Ojibwe verbs to English phrases and short sentences. 

It works closely with [ELF-Lab FST parser](https://github.com/ELF-Lab/OjibweMorph) to process inflected verbs into informational parts (such as lemma, subject, object, mode, tense etc.). From that output of the FST parser and processed dictionary templates, it will construct possible corresponding English phrases and sentences. 

Currently the translation package supports:
- All verb paradigms (VTA, VTI, VAI, VII)
- Negations (positive, negative)
- Orders: Independence, Imperative, Conjunction
- Modes: Simple, Neutral, Preterit, Dubtative, Delayed, Prohibitive
- Tenses: Present, Future (will do something), Future (want to do something), Past

### Project Organization
The package is broadly divided into 2 parts:
- Template extraction: Using LLMs (Large Language Model) to process dictionary data (at this momment, it supports OPD - Ojibwe People's Dictionary) to extract and pre-process templates for sentence building
- Sentence building: with the extracted and pre-processed templates for various Ojibwe verbs (e.g. `{{subject}} pulls {{object}} out of water`), and output from the FST parser (lemma, tense, mode, negation, etc), the sentence building code will construct the corresponding English sentence (e.g. `They pulled him/her/it out of water`, with past tense, 3rd plural subject and 3rd singular object).

### Code structure
The code is organized in the following folders:
- `data`: (required for translation functions) contains the dictionary data and templates, together with the binary file of Ojibwe Foma
  - `foma_bin`: contains the `objiwe.fomabin` binary file
  - various `.csv` files for dictionary data and templates (vta, vti, vai, vii verbs, etc)
- `src`: contains the source code
  - `dictionary_template_building`: (*not* required for translation functions) contains the Jupyter notebook files to pre-process, data extraction and template building for VTA, VTI, VAI and VII verbs with external LLM (Large Language Model). These code should run once ahead of time, and will produce various `.csv` into the `data` folder.
  - `demo`: contains Jupyter notebook file to demonstrate how to use the package
  - `test`: contains Jupyter notebook files to test the code, including verb inflection, verb building with tense, subject, object, etc as well as full translation
  - python files (required to run for translation functions):
    - `vta.py`: process VTA (Transitive, Animate) verbs
    - `vti.py`: process VTI (Transitive, Inanimate) verbs
    - `vai.py`: process VAI (Animate, Intransitive) verbs
    - `vii.py`: process VII (Inanimate, Intransitive) verbs
    - `oj_translation_core.py`: handle template loading, FOMA parser loading, low-level verb inflections, etc
    - `oj_en_translation.py`: contains abstract functions as interface to end-users, to translate inflected Ojibwe verbs to English, regardless of the verb types (VTA, VTI, etc)
    - `OJ_CONSTANTS.py`: contains pre-set values for all other functions and modules. 

### Dependencies
The package requires sereral software and packages to operate:

- [`fst-runtime`](https://github.com/CultureFoundryCA/fst-runtime) to parse words using FST binary `att` file
- [`pandas`](https://pandas.pydata.org/docs/index.html) to import and process `csv` and `json` files
- [`ELF-Lab Ojibwe FST parser`](https://github.com/ELF-Lab/OjibweMorph) binary files (`ojibwe.fomabin`)  in order for the Foma parser to correctly construct and deconstruct inflected Ojibwe verbs into elements such as lemma, tense, mode, etc.
- [`pyinflect`](https://pypi.org/project/pyinflect/0.2.0/) in order to do inflections on English verbs (such as `see` -> `saw` in past tense)



### Install using `conda` and `pip`
- Clone the package repo
  
  `git clone https://github.com/ELF-Lab/OjibweTranslation.git`
- (During development time, before official release) Switch to the `dev` branch
  
  `git checkout dev`
- Create a conda environment (if you don't have Python 3.12 running, or want to use virtual environment with conda)
  
  `conda create --name ojibwe_translation`
- Activate the new environment
  
  `conda activate ojibwe_translation`
- Move the cloned folder and install the package. It will also install required dependencies
  
  `cd OjibweTranslation`
  `pip install -e .`

### Run the web interface
- Move to the `app` folder:

  `cd app`
- Install dependencies (niceGUI). You will need to do it once only.
  
  `pip install -r requirements.txt`
- Run the web app
  
  `python main.py`


### How to use
First, please install the package as in the instruction above.

Then, use the following code

```
import ojibwe_translation as oj_to_en

# Initialization
# If you have obtained the full dataset, please change the path to the obtained folder
data_folder_path = '../tests/data/'  # Point to the data folder.

# Initialize new core environment object
core_env = oj_to_en.initialize_environment(data_folder_path)
# Load FST parser
core_env = oj_to_en.load_foma(environment=core_env, 
                              file_name="foma_bin/ojibwe.att")
# Load templates from csv files
core_env = oj_to_en.load_templates(environment=core_env)

# Translation
input = "wiikwaabiiginang" # VTI, if/when he/she pulls it with a rope

print(f"Input = {input}")
result = oj_to_en.oj2en_builder(input, environment=core_env)
print(result)
print(result[0]["translation"])
```
The output will be like:
```
[{'input': 'wiikwaabiiginang', 
  'definition': 'pull h/ with a rope', 
  'fst_output': 'wiikwaabiigin+VTA+Cnj+Pos+Neu+InclSubj+3SgProxObj', 
  'sentence_structure': {'verb': 'wiikwaabiigin', 'verb_type': 'vta', 'order': 'cnj', 'polarity': 'pos', 'mode': 'neu', 'subject': 'inclsubj', 'object': '3sgproxobj'}, 
  'translation': 'If/when we (inclusive) pull him/her/it with a rope'}, 
 
 {'input': 'wiikwaabiiginang', 
  'definition': 'pull it with a rope', 
  'fst_output': 'wiikwaabiiginan+VTI+Cnj+Pos+Neu+3SgProxSubj+0SgObj', 
  'sentence_structure': {'verb': 'wiikwaabiiginan', 'verb_type': 'vti', 'order': 'cnj', 'polarity': 'pos', 'mode': 'neu', 'subject': '3sgproxsubj', 'object': '0sgobj'}, 
  'translation': 'If/when he/she pulls it with a rope'}, 

 {'input': 'wiikwaabiiginang', 
  'definition': 'pull it with a rope', 
  'fst_output': 'wiikwaabiiginan+VTI+Cnj+Pos+Neu+3SgProxSubj+0PlObj', 
  'sentence_structure': {'verb': 'wiikwaabiiginan', 'verb_type': 'vti', 'order': 'cnj', 'polarity': 'pos', 'mode': 'neu', 'subject': '3sgproxsubj', 'object': '0plobj'}, 
  'translation': 'If/when he/she pulls them with a rope'}
]
If/when we (inclusive) pull him/her/it with a rope
```


### License
Please see "License" tab
