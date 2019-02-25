from typing import Sequence, Tuple, TypeVar, Set, List
from functools import reduce
from itertools import chain, combinations

T = TypeVar('T')
Obj = TypeVar('Obj')
Attr = TypeVar('Attr')

Relation = Sequence[Tuple[Obj, Attr]]
Concept = Tuple[Set[Obj], Set[Attr]]
Context = Tuple[Set[Obj], Set[Attr], Relation]

fst = lambda x: x[0]
snd = lambda x: x[1]


def common_attributes(A: Set[Obj], I: Relation) -> Set[Attr]:
    shared_attributes = [list(map(snd, list(filter(lambda x: fst(x) == a, I)))) for a in A]
    return reduce(set.intersection, list(map(set, shared_attributes))) if len(shared_attributes) else set()


def common_objects(B: Set[Attr], I: Relation) -> Set[Obj]:
    shared_objects = [list(map(fst, list(filter(lambda x: snd(x) == b, I)))) for b in B]
    return reduce(set.intersection, list(map(set, shared_objects))) if len(shared_objects) else set()


def extent_closure(A: Set[Obj], I: Relation) -> Set[Obj]:
    return common_objects(common_attributes(A, I), I)


def intent_closure(B: Set[Attr], I: Relation) -> Set[Attr]:
    return common_attributes(common_objects(B, I), I)


def powerset(s: Set[T]) -> List[Set[T]]:
    return list(map(set, chain.from_iterable(combinations(s, r) for r in range(len(s)+1))))


def is_concept(A: Set[Obj], B: Set[Attr], I: Relation) -> bool:
    return True if common_attributes(A, I) == B and common_objects(B, I) == A else False


def concepts(context: Context) -> List[Concept]:
    ca = [(a, common_attributes(a, context[2])) for a in powerset(context[0])]
    return list(filter(lambda x: common_objects(x[1], context[2]) == x[0], ca))


def lte(c0: Concept, c1: Concept) -> bool:
    return True if c0[0].issubset(c1[0]) and c1[1].issubset(c0[1]) else False


def join(concepts: Sequence[Concept], I: Relation) -> Concept:
    union_of_objects = extent_closure(reduce(set.union, list(map(fst, concepts))), I)
    intersection_of_attributes = reduce(set.intersection, list(map(snd, concepts)))
    return union_of_objects, intersection_of_attributes


def meet(concepts: Sequence[Concept], I: Relation) -> Concept:
    intersection_of_objects = reduce(set.intersection, list(map(fst, concepts)))
    union_of_attributes = intent_closure(reduce(set.union, list(map(snd, concepts))), I)
    return intersection_of_objects, union_of_attributes


animals = [('dog', 'pet'), ('dog', 'has_teeth'), ('dog', 'has_tail'), ('dog', 'eats_meat'),
           ('cat', 'pet'), ('cat', 'has_tail'), ('cat', 'eats_meat'), ('cat', 'worships_satan'),
           ('crocodile', 'has_teeth'), ('crocodile', 'eats_meat'),
           ('rabbit', 'pet'), ('rabbit', 'has_tail'),
           ('goat', 'worships_satan')]

print(concepts((set(list(map(fst, animals))), set(list(map(snd, animals))), animals)))
