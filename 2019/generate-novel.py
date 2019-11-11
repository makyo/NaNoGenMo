import os
import random
import sys

import markovify


class Novel(object):
    """A generated novel in three parts."""

    def __init__(self, title, part_sources, chapter_intro_source,
                 max_paragraph_length=10, max_chapter_length=100,
                 chapters_per_part=10, intro_lines=8):
        self.title = title
        self.part_sources = map(self._create_model, part_sources)
        self.chapter_intro_source = self._create_model(chapter_intro_source)
        self.max_paragraph_length = max_paragraph_length
        self.max_chapter_length = max_chapter_length
        self.chapters_per_part = chapters_per_part
        self.intro_lines = intro_lines
        self.parts = []

    def generate(self):
        for source in self.part_sources:
            self.parts.append([
                self._generate_chapter(source)
                for i in range(0, self.chapters_per_part)])

    def _generate_chapter(self, source):
        intro = [self._make_sentence(self.chapter_intro_source)
                 for i in range(0, self.intro_lines)]
        num_paragraphs = random.randint(
            self.max_chapter_length / 4 * 3, self.max_chapter_length)
        body = [
            ' '.join([
                self._make_sentence(source)
                for i in range(0, random.randint(1, self.max_paragraph_length))
            ]) for i in range(0, num_paragraphs)]
        return {'intro': intro, 'body': body}

    def _make_sentence(self, source):
        sentence = None
        while sentence is None:
            sentence = source.make_sentence()
        return sentence

    def _create_model(self, corpus):
        return markovify.Text(corpus)

    def to_markdown(self):
        if len(self.parts) == 0:
            raise self.NotYetGenerated
        md = '# {}\n\n'.format(self.title)
        part_index = 1
        for part in self.parts:
            chapter_index = 1
            md += '## Part {}\n\n'.format(part_index)
            for chapter in part:
                md += '### Chapter {}\n\n'.format(chapter_index)
                for line in chapter['intro']:
                    md += '> {}  \n'.format(line)
                md += '\n'
                for paragraph in chapter['body']:
                    md += '{}\n\n'.format(paragraph)
                chapter_index += 1
            part_index += 1
        return md

    class NotYetGenerated(Exception):
        pass


def get_corpora(files):
    """Load a set of files into an array"""
    corpora = []
    for corpus in files:
        with open(corpus) as f:
            corpora.append(f.read())
    return corpora


if __name__ == '__main__':
    intro_corpus = get_corpora([sys.argv[2]])[0]
    corpora = get_corpora(sys.argv[3:])
    novel = Novel(sys.argv[1], corpora, intro_corpus)
    novel.generate()
    print(novel.to_markdown())
