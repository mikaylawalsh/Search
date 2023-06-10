import pytest
import index

"""Tests tf and idf for a basic case, no links"""


def test_index_tf_idf():
    a = index.Indexer("xml-files/test_tf_idf.xml",
                      "txt-files/titles.txt", "txt-files/docs.txt", "txt-files/words.txt")
    assert a.id_title_dict == {1: "Page 1", 2: "Page 2", 3: "Page 3"}
    assert a.relevance_dict == {"dog": {1: 0.4054651081081644, 2: 0.4054651081081644},
                                "bit": {1: 0.4054651081081644, 3: 0.2027325540540822},
                                "man": {1: 1.0986122886681098},
                                "page": {1: 0.0, 2: 0.0, 3: 0.0},
                                "1": {1: 1.0986122886681098},
                                "ate": {2: 1.0986122886681098},
                                "chees": {2: 0.4054651081081644, 3: 0.4054651081081644},
                                "2": {2: 1.0986122886681098},
                                "3": {3: 0.5493061443340549}}
    assert a.links_dict == {1: set(), 2: set(), 3: set()}
    assert a.current == {1: 0.3333333333333333,
                         2: 0.3333333333333333, 3: 0.3333333333333333}


"""Tests page rank with pipe links, multiple links, and no links"""


def test_index_page_rank1():
    b = index.Indexer("xml-files/PageRankExample1.xml", "txt-files/titles2.txt",
                      "txt-files/docs2.txt", "txt-files/words2.txt")
    assert b.id_title_dict == {1: "A", 2: "B", 3: "C"}
    assert b.relevance_dict == {'b': {1: 0.4054651081081644, 2: 0.4054651081081644},
                                'c': {1: 0.4054651081081644, 3: 0.4054651081081644},
                                'f': {3: 1.0986122886681098}}
    assert b.links_dict == {1: {2, 3}, 2: set(), 3: {1}}
    assert b.current == {1: 0.4326427188659158,
                         2: 0.23402394780075067, 3: 0.33333333333333326}


"""Tests page rank with links to all different pages and with multiple links"""


def test_index_page_rank2():
    c = index.Indexer("xml-files/PageRankExample2.xml", "txt-files/titles4.txt",
                      "txt-files/docs4.txt", "txt-files/words4.txt")
    assert c.id_title_dict == {1: 'A', 2: 'B', 3: 'C', 4: 'D'}
    assert c.relevance_dict == {'c': {1: 0.28768207245178085, 3: 0.28768207245178085, 4: 0.28768207245178085},
                                'b': {2: 1.3862943611198906}}
    assert c.links_dict == {1: {3}, 2: {4}, 3: {4}, 4: {1, 3}}
    assert c.current == {1: 0.20184346250214996,
                         2: 0.03749999999999998,
                         3: 0.37396603749279056,
                         4: 0.3866905000050588}


"""Tests page rank with pipe links and links to oneself"""


def test_index_page_rank3():
    d = index.Indexer("xml-files/PageRankExample3.xml", "txt-files/titles5.txt",
                      "txt-files/docs5.txt", "txt-files/words5.txt")
    assert d.id_title_dict == {1: 'A', 2: 'B', 3: 'C', 4: 'D'}
    assert d.relevance_dict == {'f': {1: 1.3862943611198906},
                                'b': {2: 1.3862943611198906},
                                'c': {3: 0.6931471805599453, 4: 0.6931471805599453}}
    assert d.links_dict == {1: set(), 2: set(), 3: {4}, 4: {3}}
    assert d.current == {1: 0.05242784862611451,
                         2: 0.05242784862611451,
                         3: 0.4475721513738852,
                         4: 0.44757215137388523}


"""Tests page rank with multiple links from one page to another"""


def test_index_page_rank4():
    e = index.Indexer("xml-files/PageRankExample4.xml", "txt-files/titles6.txt",
                      "txt-files/docs6.txt", "txt-files/words6.txt")
    assert e.id_title_dict == {1: 'A', 2: 'B', 3: 'C', 4: 'D'}
    assert e.relevance_dict == {'c': {1: 0.28768207245178085, 3: 0.28768207245178085, 4: 0.28768207245178085},
                                'b': {2: 1.3862943611198906}}
    assert e.links_dict == {1: {3}, 2: {4}, 3: {4}, 4: {3}}
    assert e.current == {1: 0.0375, 2: 0.0375,
                         3: 0.46249999999999997, 4: 0.4624999999999999}


"""Tests page rank with metpages - original xml file"""


def test_metalink():
    f = index.Indexer("xml-files/test_metapage.xml", "txt-files/titles3.txt",
                      "txt-files/docs3.txt", "txt-files/words3.txt")
    assert f.id_title_dict == {1: 'first page', 2: 'Category:Computer Science'}
    assert f.relevance_dict == {'categori': {1: 0.0, 2: 0.0},
                                'comput': {1: 0.0, 2: 0.0},
                                'scienc': {1: 0.0, 2: 0.0},
                                'first': {1: 0.6931471805599453},
                                'page': {1: 0.6931471805599453},
                                'link': {2: 0.6931471805599453}}
    assert f.links_dict == {1: {2}, 2: set()}
    assert f.current == {1: 0.49999999999999994, 2: 0.49999999999999994}


"""Tests page rank and tf/idf with only one page in the xml file - original xml file"""


def test_one_page():
    g = index.Indexer("xml-files/one_page.xml", "txt-files/titles7.txt",
                      "txt-files/docs7.txt", "txt-files/words7.txt")
    assert g.id_title_dict == {1: 'first page'}
    assert g.relevance_dict == {'page': {1: 0.0},
                                'first': {1: 0.0}}
    assert g.links_dict == {1: set()}
    assert g.current == {1: 1}


"""Tests Indexer functions when none of the pages have titles - original xml file"""


def test_no_titles():
    h = index.Indexer("xml-files/no_titles.xml", "txt-files/titles8.txt",
                      "txt-files/docs8.txt", "txt-files/words8.txt")
    assert h.id_title_dict == {1: '', 4: ''}
    assert h.relevance_dict == {'page': {1: 0.0, 4: 0.0},
                                'titl': {1: 0.0, 4: 0.0},
                                'also': {4: 0.6931471805599453}}
    assert h.links_dict == {1: set(), 4: set()}
    assert h.current == {1: 0.49999999999999994, 4: 0.49999999999999994}


"""Tests Indexer functions when there is no titles or text in any pages - original xml file"""


def test_no_words_or_titles():
    i = index.Indexer("xml-files/no_words_or_titles.xml", "txt-files/titles9.txt",
                      "txt-files/docs9.txt", "txt-files/words9.txt")
    assert i.id_title_dict == {1: '', 4: '', 5: ''}
    assert i.relevance_dict == {}
    assert i.links_dict == {1: set(), 4: set(), 5: set()}
    assert i.current == {1: 0.3333333333333333,
                         4: 0.3333333333333333, 5: 0.3333333333333333}


"""Tests Indexer functions when there is titles, but no text on any page - original xml file"""


def test_no_words():
    j = index.Indexer("xml-files/no_words.xml", "txt-files/titles10.txt",
                      "txt-files/docs10.txt", "txt-files/words10.txt")
    assert j.id_title_dict == {1: 'title 1', 2: 'title 2'}
    assert j.relevance_dict == {'titl': {1: 0.0, 2: 0.0},
                                '1': {1: 0.6931471805599453},
                                '2': {2: 0.6931471805599453}}
    assert j.links_dict == {1: set(), 2: set()}
    assert j.current == {1: 0.49999999999999994, 2: 0.49999999999999994}


"""Tests Indexer functions when there is only one word in the file - original xml file"""


def test_one_word():
    k = index.Indexer("xml-files/one_word.xml", "txt-files/titles11.txt",
                      "txt-files/docs11.txt", "txt-files/words11.txt")
    assert k.id_title_dict == {1: 'title'}
    assert k.relevance_dict == {'titl': {1: 0.0}}
    assert k.links_dict == {1: set()}
    assert k.current == {1: 1}


"""Tests Indexer functions when there are no pages in the xml file - original xml file"""


def test_no_pages():
    l = index.Indexer("xml-files/no_pages.xml", "txt-files/titles12.txt",
                      "txt-files/docs12.txt", "txt-files/words12.txt")
    assert l.id_title_dict == {}
    assert l.relevance_dict == {}
    assert l.links_dict == {}
    assert l.current == {}


"""Tests page rank when a links to a page outside of the xml file - original xml file"""


def test_link_out_corpus():
    m = index.Indexer("xml-files/link_out_corpus.xml", "txt-files/titles13.txt",
                      "txt-files/docs13.txt", "txt-files/words13.txt")
    assert m.id_title_dict == {5: 'page number one', 4: 'page number two'}
    assert m.relevance_dict == {'link': {5: 0.0, 4: 0.0},
                                'corpu': {5: 0.6931471805599453},
                                'page': {5: 0.0, 4: 0.0},
                                'number': {5: 0.0, 4: 0.0},
                                'one': {5: 0.6931471805599453},
                                'two': {4: 0.6931471805599453}}
    assert m.links_dict == {5: set(), 4: set()}
    assert m.current == {5: 0.49999999999999994, 4: 0.49999999999999994}


"""Tests handling Captialization (same page as above but with caps)"""


def test_capitalization():
    m = index.Indexer("xml-files/Capitalization.xml", "txt-files/titles15.txt",
                      "txt-files/docs15.txt", "txt-files/words15.txt")
    assert m.id_title_dict == {5: 'page number one', 4: 'page number two'}
    assert m.relevance_dict == {'link': {5: 0.0, 4: 0.0},
                                'corpu': {5: 0.6931471805599453},
                                'page': {5: 0.0, 4: 0.0},
                                'number': {5: 0.0, 4: 0.0},
                                'one': {5: 0.6931471805599453},
                                'two': {4: 0.6931471805599453}}
    assert m.links_dict == {5: set(), 4: set()}
    assert m.current == {5: 0.49999999999999994, 4: 0.49999999999999994}


"""Tests handling Stemming (same page as above but with different words, same roots)"""


def test_stemming():
    m = index.Indexer("xml-files/Stemming.xml", "txt-files/titles14.txt",
                      "txt-files/docs14.txt", "txt-files/words14.txt")
    assert m.id_title_dict == {5: 'page number one', 4: 'page number two'}
    assert m.relevance_dict == {'link': {5: 0.0, 4: 0.0},
                                'corpu': {5: 0.6931471805599453},
                                'page': {5: 0.0, 4: 0.0},
                                'number': {5: 0.0, 4: 0.0},
                                'one': {5: 0.6931471805599453},
                                'two': {4: 0.6931471805599453}}
    assert m.links_dict == {5: set(), 4: set()}
    assert m.current == {5: 0.49999999999999994, 4: 0.49999999999999994}


def test_same_titles():
    n = index.Indexer("xml-files/same_titles.xml", "txt-files/same_titles.txt",
                      "txt-files/same_docs.txt", "txt-files/same_words.txt")
    assert n.id_title_dict == {1: 'dogs', 2: 'cats', 3: 'dogs'}
    assert n.relevance_dict == {'page': {1: 0.0, 2: 0.0, 3: 0.0},
                                'dog': {1: 0.4054651081081644, 3: 0.4054651081081644},
                                'cat': {2: 1.0986122886681098},
                                'anoth': {3: 0.5493061443340549}}
    assert n.links_dict == {1: set(), 2: set(), 3: set()}
    assert n.current == {1: 0.3333333333333333,
                         2: 0.3333333333333333, 3: 0.3333333333333333}
