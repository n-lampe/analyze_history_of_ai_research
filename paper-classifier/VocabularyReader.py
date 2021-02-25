import json


# Configuration class that contains all ontology information
class VocabularyReader:

    hi_vocabulary = ""
    ti_vocabulary = ""
    cv_proof = ""
    cv_ind = ""
    si_proof = ""
    si_ind = ""
    nlp_proof = ""
    nlp_ind = ""
    es_proof = ""
    es_ind = ""
    ml_proof = ""
    ml_ind = ""
    dl_proof = ""
    dl_ind = ""
    nn_proof = ""
    nn_ind = ""
    sl_proof = ""
    sl_ind = ""
    ul_proof = ""
    ul_ind = ""
    rl_proof = ""
    rl_ind = ""

    def __init__(self):
        self.read_ontology()

    # Read ontology as json
    def read_ontology(self):
        with open('ontology.json') as f:
            ontology = json.load(f)

            self.hi_vocabulary = ontology["hi"]
            self.ti_vocabulary = ontology["ti"]

            self.cv_proof = ontology["ai"]["computer vision"]["proof"]
            self.cv_ind = ontology["ai"]["computer vision"]["indicator"]
            self.si_proof = ontology["ai"]["social intelligence"]["proof"]
            self.si_ind = ontology["ai"]["social intelligence"]["indicator"]
            self.nlp_proof = ontology["ai"]["nlp"]["proof"]
            self.nlp_ind = ontology["ai"]["nlp"]["indicator"]
            self.es_proof = ontology["ai"]["expert systems"]["proof"]
            self.es_ind = ontology["ai"]["expert systems"]["indicator"]
            self.ml_proof = ontology["ai"]["machine learning"]["proof"]
            self.ml_ind = ontology["ai"]["machine learning"]["indicator"]
            self.dl_proof = ontology["ai"]["deep learning"]["proof"]
            self.dl_ind = ontology["ai"]["deep learning"]["indicator"]
            self.nn_proof = ontology["ai"]["neural networks"]["proof"]
            self.nn_ind = ontology["ai"]["neural networks"]["indicator"]
            self.sl_proof = ontology["ai"]["supervised learning"]["proof"]
            self.sl_ind = ontology["ai"]["supervised learning"]["indicator"]
            self.ul_proof = ontology["ai"]["unsupervised learning"]["proof"]
            self.ul_ind = ontology["ai"]["unsupervised learning"]["indicator"]
            self.rl_proof = ontology["ai"]["reinforcement learning"]["proof"]
            self.rl_ind = ontology["ai"]["reinforcement learning"]["indicator"]
