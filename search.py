
class Searcher:

    def __init__(self):
        self.term_color = {}
        self.color_terms = {}

    def add_searches(self, termstring, color):
        terms = termstring.split()
        if color in self.color_terms:
            for term in self.color_terms[color]:
                self.term_color.pop(term)
        self.color_terms[color] = terms
        for term in terms:
            self.term_color[term] = color


    def matches(self, codestring):
        for term, color in self.term_color.iteritems():
            if term in codestring:
                start = codestring.index(term)
                end = len(term)
                yield start, end, color

# add a kind of search that highlights the entire line?
# e.g. to highlight comments ...
