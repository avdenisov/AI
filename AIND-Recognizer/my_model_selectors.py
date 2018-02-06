import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Bayesian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """

    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components

        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on BIC scores
        BICscores = []
        models = []

        for num_hidden_states in range(self.min_n_components, self.max_n_components + 1):
            #print("seqs: ", len(self.sequences), "max: ", self.max_n_components)
            try:
                model = self.base_model(num_hidden_states)
                logL = model.score(self.X, self.lengths)
                logN = np.log(len(self.X))
                # p = num_free_params = init_state_occupation_probs + transition_probs + emission_probs
                p = num_hidden_states ** 2 + 2 * num_hidden_states * model.n_features - 1
                BICscore = -2.0 * logL + p * logN
                BICscores.append(BICscore)
                #print("  ", num_hidden_states, "BICscores", BICscores)
                        
                models.append(model)
                
            except Exception as e:
                pass
            
        #print(" ")
        #print(BICscores)
        if len(BICscores) == 0:
            return self.base_model(self.n_constant)
        else:
            return models[BICscores.index(min(BICscores))]  # returns a model with the lowest BIC score

class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    https://pdfs.semanticscholar.org/ed3d/7c4a5f607201f3848d4c02dd9ba17c791fc2.pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on DIC scores
        DICscores = []
        models = []
        
        logL_other_words = []

        for num_hidden_states in range(self.min_n_components, self.max_n_components + 1):
            #print("seqs: ", len(self.sequences), "max: ", self.max_n_components)
            try:
                model = self.base_model(num_hidden_states)
                logL = model.score(self.X, self.lengths)
                for word, (X, lengths) in self.hwords.items():
                    if word != self.this_word:
                        logL_other_words.append(model.score(X, lengths))
                        #print("  =>", num_hidden_states, "logL_other_words", logL_other_words)

                DICscore = logL - np.mean(logL_other_words)
                DICscores.append(DICscore)
                logL_other_words[:] = []
                #print(" ", num_hidden_states, "DICscores", DICscores)
                        
                models.append(model)
                
            except Exception as e:
                pass
            
        #print(" ")
        #print(DICscores)
        if len(DICscores) == 0:
            return self.base_model(self.n_constant)
        else:
            return models[DICscores.index(max(DICscores))] # returns a model with the highest DIC score


class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds

    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection using CV
        kf = KFold(n_splits=3)
        logLs = []
        models = []
        
        CV_logLs = []

        for num_hidden_states in range(self.min_n_components, self.max_n_components + 1):
            #print("seqs: ", len(self.sequences), "max: ", self.max_n_components)
            try:
                if len(self.sequences) > 2:
                    for train_index, test_index in kf.split(self.sequences):
                        X, length = self.X, self.lengths # save initial X, length
                        self.X, self.lengths = combine_sequences(train_index, self.sequences)
                        X_test, lengths_test = combine_sequences(test_index, self.sequences)
                        model = self.base_model(num_hidden_states)
                        logL = model.score(X_test, lengths_test)
                        CV_logLs.append(logL)
                        # print("  ", num_hidden_states, "CV_logLs", CV_logLs)
                        self.X, self.lengths = X, length # restore initial X, length
                        
                    logLs.append(np.mean(CV_logLs))
                    models.append(self.base_model(num_hidden_states))
                    CV_logLs[:] = [] # clean the list
                    
                else:
                    model = self.base_model(num_hidden_states)
                    logL = model.score(self.X, self.lengths)
                    logLs.append(logL)
                    models.append(model)
                    
                #print(num_hidden_states," => ", logLs, len(logLs), len(models))
                
            except Exception as e:
                pass
            
        #print(" ")
        #print(logLs)
        if len(logLs) == 0:
            return self.base_model(self.n_constant)
        else:
            return models[logLs.index(max(logLs))]# returns a model with the highest logL
    