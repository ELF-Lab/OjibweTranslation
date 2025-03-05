import ojibwe_translation.oj_en_translation as oj_to_en
from ojibwe_translation.oj_constants import *
from ojibwe_translation import logger

def test_subject_pronouns():
    """
        Test converting Test converting FST subject tags to English pronouns
    """
    logger.debug("Test converting FST subject tags to English pronouns...")    
    assert oj_to_en.convert_fst_subject_tag_to_en_pronoun("1SgSubj") == "I"
    assert oj_to_en.convert_fst_subject_tag_to_en_pronoun("3SgSubj") == "he/she"
    assert oj_to_en.convert_fst_subject_tag_to_en_pronoun("3sgXSubj") == "(someone)"
    assert oj_to_en.convert_fst_subject_tag_to_en_pronoun("3SgProxSubj") == f"he/she ({PROXIMATE_TAG})"
    assert oj_to_en.convert_fst_subject_tag_to_en_pronoun("0SgSubj") == f"it ({INANIMATE_TAG})"
    assert oj_to_en.convert_fst_subject_tag_to_en_pronoun("0PlSubj") == f"they ({INANIMATE_TAG})"

def test_object_pronouns():
    """
        Test converting Test converting FST object tags to English pronouns
    """
    logger.debug("Test converting FST object tags to English pronouns...")    
    assert oj_to_en.convert_fst_object_tag_to_en_pronoun("1SgObj") == "me"
    assert oj_to_en.convert_fst_object_tag_to_en_pronoun("1PlObj") == "us"
    assert oj_to_en.convert_fst_object_tag_to_en_pronoun("2SgObj") == "you"
    assert oj_to_en.convert_fst_object_tag_to_en_pronoun("2PlObj") == "you (all)"
    assert oj_to_en.convert_fst_object_tag_to_en_pronoun("3SgObj") == "him/her/it"
    assert oj_to_en.convert_fst_object_tag_to_en_pronoun("3PlObj") == "them"

    assert oj_to_en.convert_fst_object_tag_to_en_pronoun("0SgObj") == "it"
    assert oj_to_en.convert_fst_object_tag_to_en_pronoun("0PlObj") == "them"
    assert oj_to_en.convert_fst_object_tag_to_en_pronoun("NullObj") == ""


def test_to_be_verbs():
    """
        Test building to-be verbs with tenses
    """
    logger.debug("Test to-be verbs....")    

    assert oj_to_en.build_verb_in_past_tense(main_sentence_verb="be", subject_tag="1SgSubj", 
                                             polarity_tag="pos", mode_tag="neu", tense_tag="past") == "was"
    assert oj_to_en.build_verb_in_past_tense("be", "3PlSubj",                 
                                             polarity_tag="pos", mode_tag="neu", tense_tag="past") == "were"
    assert oj_to_en.build_verb_in_simple_future_tense("be", "1Sg", polarity_tag="pos", mode_tag="neu", tense_tag="future/will") == "will be"
    assert oj_to_en.build_verb_future_wish_tense("be", "1Sg", polarity_tag="pos", mode_tag="neu", tense_tag="future/wish") == "want to be"

    assert oj_to_en.build_verb("be", "1SgSubj", polarity_tag="pos", mode_tag="neu", tense_tag="") == "am"
    assert oj_to_en.build_verb("be", "3Sg", polarity_tag="pos", mode_tag="neu", tense_tag="") == "is"
    assert oj_to_en.build_verb("be", "3Pl", polarity_tag="pos", mode_tag="neu", tense_tag="") == "are"
    assert oj_to_en.build_verb("be", "3SgXSubj", polarity_tag="pos", mode_tag="neu", tense_tag="") == "is"

    assert oj_to_en.build_verb("be", "1Sg", polarity_tag="pos", mode_tag="neu", tense_tag="") == "am" 
    assert oj_to_en.build_verb("be", "3SgXsubj", polarity_tag="pos", mode_tag="neu", tense_tag="") == "is" 
    assert oj_to_en.build_verb("be", "1Sg", polarity_tag="pos", mode_tag="neu", tense_tag="past") == "was" 
    assert oj_to_en.build_verb("be", "1Sg", polarity_tag="neg", mode_tag="neu", tense_tag="past") == "was not" 
    
    assert oj_to_en.build_verb("be", "3SgXSubj", polarity_tag="neg", mode_tag="neu", tense_tag="past") == "was not" 

    assert oj_to_en.build_verb("be", "1Sg", polarity_tag="pos", mode_tag="neu", tense_tag="future/will") == "will be" 
    assert oj_to_en.build_verb("be", "1Sg", polarity_tag="neg", mode_tag="neu", tense_tag="future") == "will not be" 

    assert oj_to_en.build_verb("be", "1Sg", polarity_tag="pos", mode_tag="neu", tense_tag="future/going") == "am going to be" 
    assert oj_to_en.build_verb("be", "1Sg", polarity_tag="neg", mode_tag="neu", tense_tag="future/going") == "am not going to be" 
    assert oj_to_en.build_verb("be", "3Sg", polarity_tag="neg", mode_tag="neu", tense_tag="future/going") == "is not going to be" 
    assert oj_to_en.build_verb("be", "3SgXSubj", polarity_tag="neg", mode_tag="neu", tense_tag="future/going") == "is not going to be" 
    assert oj_to_en.build_verb("be", "2Sg", polarity_tag="neg", mode_tag="neu", tense_tag="future/going") == "are not going to be" 

    assert oj_to_en.build_verb("be", "3Sg", polarity_tag="pos", mode_tag="neu", tense_tag="future/wish") == "wants to be" 
    assert oj_to_en.build_verb("be", "3SgXSubj", polarity_tag="pos", mode_tag="neu", tense_tag="future/wish") == "wants to be" 
    assert oj_to_en.build_verb("be", "2Sg", polarity_tag="pos", mode_tag="neu", tense_tag="future/wish") == "want to be" 
    assert oj_to_en.build_verb("be", "3Sg", polarity_tag="neg", mode_tag="neu", tense_tag="future/wish") == "does not want to be" 
    assert oj_to_en.build_verb("be", "3SgX", polarity_tag="neg", mode_tag="neu", tense_tag="future/wish") == "does not want to be" 
    assert oj_to_en.build_verb("be", "2Sg", polarity_tag="neg", mode_tag="neu", tense_tag="future/wish") == "do not want to be" 


def test_verbs_past_tense():
    """
        Test verb building in past tense
    """
    logger.debug("Testing building verb with past tense...")
    assert oj_to_en.build_verb_in_past_tense("see", "1Sg", polarity_tag="pos", mode_tag="neu", tense_tag="past") == "saw"
    assert oj_to_en.build_verb_in_past_tense("do", "2Pl", polarity_tag="pos", mode_tag="neu", tense_tag="past") == "did"
    assert oj_to_en.build_verb_in_past_tense("dance", "2Pl", polarity_tag="pos", mode_tag="neu", tense_tag="past") == "danced"
    assert oj_to_en.build_verb_in_past_tense("see", "1Sg", polarity_tag="neg", mode_tag="neu", tense_tag="past") == "did not see"

    assert oj_to_en.build_verb_in_past_tense("dance", "1Sg", polarity_tag="pos", mode_tag="prt", tense_tag="past") == "used to dance"
    assert oj_to_en.build_verb_in_past_tense("dance", "3Pl", polarity_tag="neg", mode_tag="prt", tense_tag="past") == "did not used to dance"

    assert oj_to_en.build_verb_in_past_tense("dance", "1Sg", polarity_tag="pos", mode_tag="dub", tense_tag="past") == "might have danced"
    assert oj_to_en.build_verb_in_past_tense("dance", "3Pl", polarity_tag="neg", mode_tag="dub", tense_tag="past") == "might not have danced"

def test_verbs_simple_future_tense():
    """
        Test verb building in future tense
    """
    logger.debug("Testing future (will) tense...")

    assert oj_to_en.build_verb_in_simple_future_tense("see", "1Sg", polarity_tag="pos", mode_tag="neu", tense_tag="future") == "will see"
    assert oj_to_en.build_verb_in_simple_future_tense("dance", "2Pl", polarity_tag="pos", mode_tag="neu", tense_tag="future/will") == "will dance"
    assert oj_to_en.build_verb_in_simple_future_tense("see", "1Sg", polarity_tag="neg", mode_tag="neu", tense_tag="future/will") == "will not see"

    assert oj_to_en.build_verb_in_simple_future_tense("dance", "1Sg", polarity_tag="pos", mode_tag="prt", tense_tag="future") == "dance" # not valid, return verb in present tense
    assert oj_to_en.build_verb_in_simple_future_tense("dance", "3Pl", polarity_tag="neg", mode_tag="prt", tense_tag="future") == "dance" # not valid, return verb in present tense

    assert oj_to_en.build_verb_in_simple_future_tense("dance", "1Sg", polarity_tag="pos", mode_tag="dub", tense_tag="future") == "dance" # not valid, return verb in present tense
    assert oj_to_en.build_verb_in_simple_future_tense("dance", "3Pl", polarity_tag="neg", mode_tag="dub", tense_tag="future") == "dance" # not valid, return verb in present tense

def test_verbs_future_wish_tense():
    """
        Test verb building in future/wish tense (I want to do something)
    """
    logger.debug("Testing future (wish) tense...")

    assert oj_to_en.build_verb_future_wish_tense("see", "1Sg", polarity_tag="pos", mode_tag="neu", tense_tag="future/wish") == "want to see"
    assert oj_to_en.build_verb_future_wish_tense("do", "2Pl", polarity_tag="pos", mode_tag="neu", tense_tag="future/wish") == "want to do"
    assert oj_to_en.build_verb_future_wish_tense("dance", "3Sg", polarity_tag="pos", mode_tag="neu", tense_tag="future/wish") == "wants to dance"
    assert oj_to_en.build_verb_future_wish_tense("dance", "3sgxsubj", polarity_tag="pos", mode_tag="neu", tense_tag="future/wish") == "wants to dance"
    assert oj_to_en.build_verb_future_wish_tense("see", "3Sg", polarity_tag="neg", mode_tag="neu", tense_tag="future/wish") == "does not want to see"

    assert oj_to_en.build_verb_future_wish_tense("dance", "1Sg", mode_tag="prt", polarity_tag="pos", tense_tag="future/wish") == "was going to dance"
    assert oj_to_en.build_verb_future_wish_tense("dance", "3Pl", polarity_tag="neg", mode_tag="prt", tense_tag="future/wish") == "were not going to dance"

    assert oj_to_en.build_verb_future_wish_tense("dance", "1Sg", polarity_tag="pos", mode_tag="dub", tense_tag="future/wish") == "might dance"
    assert oj_to_en.build_verb_future_wish_tense("dance", "3Pl", polarity_tag="neg", mode_tag="dub", tense_tag="future/wish") == "might not dance"


def test_verbs_future_wish_tense():
    """
        Test verb building with various tenses, subjects and modes
    """
    logger.debug("Testing verb building with various subject, modes and tenses...")
    assert oj_to_en.build_verb("see", "1Sg", polarity_tag="pos", mode_tag="neu", tense_tag="") == "see" # should be "see"
    assert oj_to_en.build_verb("see", "3SgXsubj", polarity_tag="pos", mode_tag="neu", tense_tag="") == "sees" # should be "sees"
    assert oj_to_en.build_verb("see", "1Sg", polarity_tag="pos", mode_tag="neu", tense_tag="past") == "saw" # should be "saw"
    assert oj_to_en.build_verb("see", "1Sg", polarity_tag="neg", mode_tag="neu", tense_tag="past") == "did not see" # should be "did not see"
    assert oj_to_en.build_verb("see", "3SgXSubj", polarity_tag="neg", mode_tag="neu", tense_tag="past") == "did not see" # should be "did not see"

    assert oj_to_en.build_verb("see", "1Sg", polarity_tag="pos", mode_tag="neu", tense_tag="future/will") == "will see" # should be "will see"
    assert oj_to_en.build_verb("see", "1Sg", polarity_tag="neg", mode_tag="neu", tense_tag="future") == "will not see" # should be "will not see"

    assert oj_to_en.build_verb("see", "1Sg", polarity_tag="pos", mode_tag="neu", tense_tag="future/going") == "am going to see" # should be "am going to see"
    assert oj_to_en.build_verb("see", "1Sg", polarity_tag="neg", mode_tag="neu", tense_tag="future/going") == "am not going to see" # should be "am not going to see"
    assert oj_to_en.build_verb("see", "3Sg", polarity_tag="neg", mode_tag="neu", tense_tag="future/going") == "is not going to see" # should be "is not going to see"
    assert oj_to_en.build_verb("see", "3SgXSubj", polarity_tag="neg", mode_tag="neu", tense_tag="future/going") == "is not going to see" # should be "is not going to see"
    assert oj_to_en.build_verb("see", "2Sg", polarity_tag="neg", mode_tag="neu", tense_tag="future/going") == "are not going to see" # should be "are not going to see"

    assert oj_to_en.build_verb("see", "3Sg", polarity_tag="pos", mode_tag="neu", tense_tag="future/wish") == "wants to see" # should be "wants to see"
    assert oj_to_en.build_verb("see", "3SgXSubj", polarity_tag="pos", mode_tag="neu", tense_tag="future/wish") == "wants to see" # should be "wants to see"
    assert oj_to_en.build_verb("see", "2Sg", polarity_tag="pos", mode_tag="neu", tense_tag="future/wish") == "want to see" # should be "want to see"
    assert oj_to_en.build_verb("see", "3Sg", polarity_tag="neg", mode_tag="neu", tense_tag="future/wish") == "does not want to see" # should be "doesn't want to see"
    assert oj_to_en.build_verb("see", "3SgX", polarity_tag="neg", mode_tag="neu", tense_tag="future/wish") == "does not want to see" # should be "doesn't want to see"
    assert oj_to_en.build_verb("see", "2Sg", polarity_tag="neg", mode_tag="neu", tense_tag="future/wish") == "do not want to see" # should be "don't want to see"

    # test with negation
    logger.debug("Testing with negation...")
    assert oj_to_en.build_verb("see", "1Sg", polarity_tag="neg", mode_tag="neu", tense_tag="") == "do not see" # should be "don't see"
    assert oj_to_en.build_verb("see", "3Sg", polarity_tag="neg", mode_tag="neu", tense_tag="") == "does not see" # should be "doesn't see"

    # test with Prt mode (in the past, but not in the present)
    logger.debug("Testing verb building with Prt mode...")
    assert oj_to_en.build_verb("see", "1Sg", mode_tag="prt", polarity_tag="pos", tense_tag="") == "saw" # should be "saw"
    assert oj_to_en.build_verb("eat", "1Sg", mode_tag="prt", polarity_tag="pos", tense_tag="") == "ate" # should be "ate"

    # test with Prt mode (in the past, but not in the present), with negation
    logger.debug("Testing verb building with Prt mode with negation...")
    assert oj_to_en.build_verb("see", "1Sg", polarity_tag="neg", mode_tag="prt", tense_tag="") == "did not see" # should be "didn't see"
    assert oj_to_en.build_verb("eat", "1Sg", polarity_tag="neg", mode_tag="prt", tense_tag="") == "did not eat" # should be "didn't eat"

    
    # test with Dub mode (uncertainty)
    logger.debug("Test verb building with Dub (uncertainty) mode...")

    assert oj_to_en.build_verb("eat", "1Sg", mode_tag="dub", polarity_tag="pos", tense_tag="") == "might eat" # should be "might eat"
    assert oj_to_en.build_verb("see", "1Sg", mode_tag="dub", polarity_tag="pos", tense_tag="") == "might see" # should be "saw"

    # test with Dub mode (uncertainty), with negation
    print("Test verb building with Dub (uncertainty) mode with negation...")

    assert oj_to_en.build_verb("eat", "1Sg", polarity_tag="neg", mode_tag="dub", tense_tag="") == "might not eat" # should be "might not eat"
    assert oj_to_en.build_verb("see", "1Sg", polarity_tag="neg", mode_tag="dub", tense_tag="") == "might not see" # should be "might not see"


print("Running tests for Ojibwe-translation package: Pronouns and Verb building")

test_subject_pronouns()
test_object_pronouns()
test_to_be_verbs()
test_verbs_past_tense()
test_verbs_simple_future_tense()
test_verbs_future_wish_tense()
test_verbs_future_wish_tense()

print("All tests passed")
