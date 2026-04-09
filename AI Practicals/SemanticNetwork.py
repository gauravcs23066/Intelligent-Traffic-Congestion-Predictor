isa = {
    "bird": "animal",
    "dog": "animal",
    "sparrow": "bird"
}
has = {
    "animal": ["cells"]
}
can_dict = {
    "bird": ["fly"],
    "dog": ["bark"]
}
def is_a(child, parent):
    while child:
        if child == parent:
            return True
        child = isa.get(child)
    return False
def has_property(entity, property_name):
    while entity:
        if entity in has and property_name in has[entity]:
            return True
        entity = isa.get(entity)
    return False
def can(entity, ability):
    while entity:
        if entity in can_dict and ability in can_dict[entity]:
            return True
        entity = isa.get(entity)
    return False
print("Is sparrow an animal? ->", is_a("sparrow", "animal"))
print("Can sparrow fly? ->", can("sparrow", "fly"))
print("Does sparrow have cells? ->", has_property("sparrow", "cells"))
print("Can dog bark? ->", can("dog", "bark"))
print("Is dog a bird? ->", is_a("dog", "bird"))
print("Can dog fly? ->", can("dog", "fly"))
print("Does bird bark? ->", can("bird", "bark"))
print("Does sparrow have wings? ->", has_property("sparrow", "wings"))