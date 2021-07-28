from typing import Dict, List, Set
from functools import reduce
from re import findall
from stemmer import PorterStemmer


class Processor:
    def __init__(self, raw_file: Dict[str, List[str]], stopwords: Set[str] = set()) -> None:
        self._raw = raw_file
        self._stemmer = PorterStemmer()
        self._stopwords = stopwords
        self._stem_to_words = {}

    def process(self) -> Dict[str, Set[str]]:
        all_bios = {name: self._process_bio(bio)
                    for name, bio in self._raw.items()}
        # Discard any word that appears in more than half of the texts.
        words_to_remove = set()
        for bio in all_bios.values():
            for word in bio:
                appearances = sum([1 for x in all_bios.values() if word in x])
                if appearances > len(all_bios) / 2:
                    words_to_remove.add(word)
        for bio in all_bios.keys():
            removed_bio = [word for word in all_bios[bio]
                           if word not in words_to_remove]
            all_bios[bio] = set(removed_bio)

        return all_bios

    def _process_bio(self, raw_bio: List[str]) -> Set[str]:
        bio = self._to_list(raw_bio)
        # Convert all words to lower case.
        # Discard all stop words and all words of fewer than three characters
        # Apply the Porter stemming algorithm to remove various kinds of inflections
        # (plural, tense markers, and so on).
        # Code for the Porter Stemming Algorithm in a variety of programming languages
        # can be found at http://tartarus.org/martin/PorterStemmer/.
        stemmed_bio = []
        for word in bio:
            word = word.lower()
            if len(word) > 3 and word not in self._stopwords:
                stemmed = self._stemmer.stem(word, 0, len(word)-1)
                self._stem_to_words[stemmed] = word
                stemmed_bio.append(stemmed)
        return set(stemmed_bio)

    def _to_list(self, raw_bio: List[str]) -> List[str]:
        # A word is a sequence of alphabetical characters a-z,A-Z.
        # Assume that any other character breaks a word.
        # Do not worry about non-standard characters
        split_bio = map(lambda x: findall('[a-zA-Z]+', x), raw_bio)
        return reduce(lambda x, y: x + y, split_bio)
    
    @property
    def stem_to_words(self) -> Dict[str, str]:
        return self._stem_to_words


if __name__ == '__main__':
    from parse import Parser
    parser = Parser('input.test')
    processor = Processor(parser.read_file(), set(['with', 'from', 'later']))
    print(processor.process())
