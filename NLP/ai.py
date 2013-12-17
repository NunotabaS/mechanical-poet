#!/usr/bin/env python\
# 世界はそんなに眩しいです
import paraphraser, autofilters

paraphraser = init_paraphraser ("data/paraphr.db")
filters = init_filters("data/filters.db")

def generate (filename):
    with open(filename, "r") as f:
        for line in f:
            successors = paraphraser.getSuccessors ( line );
            scores = [(s, filters.score(s)) for s in successors]
            
