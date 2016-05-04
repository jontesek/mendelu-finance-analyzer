import re
import xml.etree.ElementTree as etree


class LexiconReader(object):

    def __init__(self):
        self.file_paths = {'input': '../input_sources/'}
        self.dicts = {}

    def get_dictionary(self, s_dictionary_name):
        """Read lexicon file to a dictionary: [word] -> [value]"""
        # CUSTOM DICTS
        if s_dictionary_name == 'custom_dict_orig':
            s_dict = self._get_custom_dict_orig()
        elif s_dictionary_name == 'custom_dict_fs_added':
            s_dict = self._get_custom_dict_fs_added()
        # ORIGINAL DICTS
        elif s_dictionary_name == 'afinn':
            s_dict = self._get_afinn_dictionary()
        elif s_dictionary_name == 'wordstat':
            s_dict = self._get_wordstat_dictionary()
        elif s_dictionary_name == 'subjclues':
            s_dict = self._get_subjclues_dictionary()
        elif s_dictionary_name == 'sentiwordnet':
            s_dict = self._get_sentiwordnet_dictionary()
        elif s_dictionary_name == 'bing':
            s_dict = self._get_bing_dictionary()
        elif s_dictionary_name == 'senticnet':
            s_dict = self._get_senticnet_dictionary()
        elif s_dictionary_name == 'vader':
            s_dict = self._get_vader_dictionary()
        elif s_dictionary_name == 'labmt':
            s_dict = self._get_labmt_dictionary()
        elif s_dictionary_name == 'warriner':
            s_dict = self._get_warriner_dictionary()
        elif s_dictionary_name == 'mcdonald':
            s_dict = self._get_mcdonald_dictionary()
        elif s_dictionary_name == 'henry':
            s_dict = self._get_henry_dictionary()
        elif s_dictionary_name == 'hajek':
            s_dict = self._get_hajek_dictionary()
        elif s_dictionary_name == 'lsd':
            s_dict = self._get_lsd_dictionary()
        elif s_dictionary_name == 'micrownop':
            s_dict = self._get_micrownop_dictionary()
        else:
            return False
        # OK
        return s_dict

    #### CUSTOM DICTS

    def _get_custom_dict_orig(self):
        """
        Combined directory from McDonald, Henry, Hajek, VADER (duplicate removed in the order).
        Contains only single words and some weights.
        """
        # Prepare variables.
        dict_file = open(self.file_paths['input'] + "custom_dicts/custom_dict_orig.txt", 'r')
        custom_dict = {}
        # Skipt header line.
        dict_file.readline()
        # For every line, read a word and its value and save it to dictionary.
        for line in dict_file:
            l_items = line.strip().split('\t')
            word = l_items[0].strip()
            polarity = float(l_items[1])
            custom_dict[word] = polarity
        # result
        return custom_dict


    #### ORIGINAL DICTS

    def _get_afinn_dictionary(self):
        """
        n-grams: no
        weights: yes
        """
        afinn = dict(map(lambda (k,v): (k,int(v)),
                     [line.split('\t') for line in open(self.file_paths['input']+"sentiment_dicts/AFINN-111.txt")]))
        return afinn

    def _get_wordstat_dictionary(self):
        """
        n-grams: no
        weights: no
        """
        dict_file = open(self.file_paths['input']+"sentiment_dicts/WordStat Sentiments.CAT", 'r')
        wordstat = {}
        for line_n, line_content in enumerate(dict_file.readlines(), 1):
            line_value = line_content.strip().split(' ')[0].lower()
            # Save negative words
            if line_n > 61 and line_n < 9615:
                wordstat[line_value] = -1
                continue
            # Save positive words
            if line_n > 9615:
                wordstat[line_value] = 1
        # result
        dict_file.close()
        return wordstat

    def _get_subjclues_dictionary(self):
        """
        n-grams: no
        weights: partially
        """
        # Open file
        dict_file = open(self.file_paths['input']+"sentiment_dicts/subjclueslen1-HLTEMNLP05.tff", 'r')
        subjclues = {}
        val_regex = re.compile('(.+)=(.+)')
        # Read file
        for line in dict_file:
            # Save values from line into dictionary
            values = line.split(' ')
            vals_dict = {}
            for val in values:
                matches = val_regex.match(val)
                vals_dict[matches.group(1).strip()] = matches.group(2).strip()
            # Get word polarity
            word_polarity = 1 if vals_dict['priorpolarity'] == 'positive' else -1
            word_weight = 1.0 if vals_dict['type'] == 'strongsubj' else 0.6
            # Insert word and its polarity into subjcluse dict.
            subjclues[vals_dict['word1']] = word_polarity * word_weight
        # result
        dict_file.close()
        return subjclues

    def _get_sentiwordnet_dictionary(self):
        """
        n-grams: yes
        weights: yes
        """
        # Open file
        dict_file = open(self.file_paths['input']+"sentiment_dicts/SentiWordNet_3.0.0_20130122.txt", 'r')
        sentiwordnet = {}
        regexp_term = re.compile('(.+)#(\d+)')
        # Read file
        for line in dict_file:
            # skip comment lines
            if line.startswith('#'):
                continue
            # Get values from line
            values = line.split('\t')
            # Choose synset polarity
            pos_score = float(values[2])
            neg_score = float(values[3])
            if pos_score > 0.0:
                polarity = pos_score
            elif neg_score > 0.0:
                polarity = - neg_score
            else:
                polarity = 0.0
            # Get individual terms
            terms = values[4].split(' ')
            for term in terms:
                # Get term string.
                term_string = regexp_term.match(term).group(1)
                # Add term to the sentiwordnet dict.
                sentiwordnet[term_string] = polarity
        # result
        dict_file.close()
        return sentiwordnet

    def _get_bing_dictionary(self):
        """
        n-grams: no
        weights: no
        """
        binglexicon = {}
        # 1. Positive words
        dict_file = open(self.file_paths['input']+"sentiment_dicts/bing-opinion-lexicon/positive-words.txt", 'r')
        for line in dict_file:
            # Skip comment lines.
            if line.startswith(';'):
                continue
            # Save word to binglexicon
            binglexicon[line.strip()] = 1
        dict_file.close()
        # 2. Negative words
        dict_file = open(self.file_paths['input']+"sentiment_dicts/bing-opinion-lexicon/negative-words.txt", 'r')
        for line in dict_file:
            # Skip comment lines.
            if line.startswith(';'):
                continue
            # Save word to binglexicon
            binglexicon[line.strip()] = -1
        dict_file.close()
        # result
        return binglexicon

    def _get_senticnet_dictionary(self):
        """
        n-grams: yes
        weights: yes
        """
        # Open XML file
        tree = etree.parse(self.file_paths['input']+"sentiment_dicts/senticnet.rdf.xml")
        senticnet = {}
        # Get all concepts
        root = tree.getroot()
        for concept in root:
            word = concept[1].text.strip().lower()
            polarity = float(concept[2].text)
            senticnet[word] = polarity
        # result
        return senticnet

    def _get_vader_dictionary(self):
        """
        n-grams: no
        weights: yes
        """
        # Open file
        dict_file = open(self.file_paths['input']+"sentiment_dicts/vader_sentiment_lexicon.txt", 'r')
        vaderlexicon = {}
        # Read file
        for line in dict_file:
            # Get values
            values = line.split('\t')
            word = values[0]
            polarity = float(values[1])
            # Add word to the vaderlexicon
            vaderlexicon[word] = polarity
        # result
        dict_file.close()
        return vaderlexicon

    def _get_labmt_dictionary(self):
        # Open file
        dict_file = open(self.file_paths['input']+"sentiment_dicts/journal.pone.0026752.s001.txt", 'r')
        labmtlexicon = {}
        # Get statistical values
        lines = dict_file.readlines()
        best_hap = float(lines[4].split('\t')[2])
        worst_hap = float(lines[-1].split('\t')[2])
        avg_hap = (best_hap + worst_hap) / 2
        # Read all words
        for line in lines[4:]:
            # Get values
            values = line.split('\t')
            word = values[0].strip()
            happiness_absolute = float(values[2])
            # Count relative polarity
            happiness_relative = happiness_absolute - avg_hap
            # Add word to the labmt dict
            labmtlexicon[word] = round(happiness_relative, 5)
        # result
        dict_file.close()
        return labmtlexicon

    def _get_warriner_dictionary(self):
        # Open file
        dict_file = open(self.file_paths['input']+"sentiment_dicts/Ratings_Warriner_et_al.csv", 'r')
        warriner = {}
        # Skip header line
        dict_file.readline()
        # Counted values from Excel
        highest_v = 8.53    # vacation
        lowest_v = 1.26     # pedophile
        avg_valence = (highest_v + lowest_v) / 2
        # Read all words
        for line in dict_file:
            # Get values
            values = line.split(',')
            word = values[1].strip()
            absolute_v = float(values[2])   # valence overall mean (V.Mean.Sum)
            # Count relative valence
            relative_v = absolute_v - avg_valence
            # Add word to the warriner dict
            warriner[word] = round(relative_v, 5)
        # result
        dict_file.close()
        return warriner

    def _get_mcdonald_dictionary(self):
        # Open file
        dict_file = open(self.file_paths['input']+"sentiment_dicts/LoughranMcDonald_MasterDictionary_2014.csv", 'r')
        mcdonald = {}
        # Skip header line
        dict_file.readline()
        # Read all words
        for line in dict_file:
            # Get values
            values = line.split(';')
            word = values[0].strip().lower()
            # Has the word any polarity?
            neg_val = int(values[7])
            pos_val = int(values[8])
            if pos_val > 0:
                polarity = 1
            elif neg_val > 0:
                polarity = -1
            else:
                polarity = None
            # If it has, save it to tje mcdonald dict.
            if polarity:
                mcdonald[word] = polarity
        # result
        dict_file.close()
        return mcdonald

    def _get_henry_dictionary(self):
        """
        n-grams: no
        weights: no
        """
        henry = {}
        # Read positive words
        dict_file = open(self.file_paths['input']+"sentiment_dicts/henry-word-list/positive_lines.txt", 'r')
        for line in dict_file:
            henry[line.strip()] = 1
        dict_file.close()
        # Read negative words
        dict_file = open(self.file_paths['input']+"sentiment_dicts/henry-word-list/negative_lines.txt", 'r')
        for line in dict_file:
            henry[line.strip()] = -1
        dict_file.close()
        # result
        return henry

    def _get_hajek_dictionary(self):
        """
        n-grams: yes
        weights: no
        """
        hajek = {}
        # Read positive words
        dict_file = open(self.file_paths['input']+"sentiment_dicts/hajek-multi-list/positivni.txt", 'r')
        for line in dict_file:
            # Get term word(s)
            line_words = line.strip().split(' ')
            # Create term key
            if len(line_words) == 1:
                term_key = line_words[0].strip()
            else:
                term_key = tuple(word.strip() for word in line_words)
            # Save term to dict
            hajek[term_key] = 1
        dict_file.close()
        # Read negative words
        dict_file = open(self.file_paths['input']+"sentiment_dicts/hajek-multi-list/negativni.txt", 'r')
        for line in dict_file:
            # Get term word(s)
            line_words = line.strip().split(' ')
            # Create term key
            if len(line_words) == 1:
                term_key = line_words[0].strip()
            else:
                term_key = tuple(word.strip() for word in line_words)
            # Save term to dict
            hajek[term_key] = -1
        # result
        dict_file.close()
        return hajek

    def _get_lsd_dictionary(self):
        """
        n-grams: no
        weights: no
        """
        # Open file
        dict_file = open(self.file_paths['input']+"sentiment_dicts/LSD2015.lc3", 'r')
        lsdlexicon = {}
        # Read file
        for line_n, line_content in enumerate(dict_file):
            # Save negative terms
            if line_n > 1 and line_n < 2860:
                term_key = self._lsd_create_term_key_from_line(line_content)
                lsdlexicon[term_key] = -1
                continue
            # Save positive terms
            if line_n > 2860:
                term_key = self._lsd_create_term_key_from_line(line_content)
                lsdlexicon[term_key] = 1
        # result
        dict_file.close()
        return lsdlexicon

    def _lsd_create_term_key_from_line(self, line):
        # Get term word(s)
        line_words = line.strip().split(' ')
        # Create term key
        if len(line_words) == 1:
            term_key = line_words[0].strip()
        else:
            term_key = tuple(word.strip() for word in line_words)
        # result
        return term_key

    def _get_micrownop_dictionary(self):
        # NOT WORKING ON GROUP 1, 2
        # Open file
        dict_file = open(self.file_paths['input']+"sentiment_dicts/Micro-WNOp-data.txt", 'r')
        micrownop = {}
        regexp_term = re.compile('^(.+)#.+')
        # Read file
        for line in dict_file:
            # skip comment lines
            if line.startswith('#'):
                continue
            # Get values from line
            values = line.split('\t')
            # Choose synset polarity
            pos_score = float(values[0])
            neg_score = float(values[1])
            if pos_score > 0.0:
                polarity = pos_score
            elif neg_score > 0.0:
                polarity = - neg_score
            else:
                polarity = 0.0
            # Get individual terms
            terms = values[2].split(' ')
            for term in terms:
                # Get term string.
                term_string = regexp_term.match(term).group(1)
                # Add term to the sentiwordnet dict.
                micrownop[term_string] = polarity
        # result
        dict_file.close()
        return micrownop


