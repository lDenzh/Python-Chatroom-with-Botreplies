import random


# Bot functions

def yoda(a, b=None):
    return "Yoda > {} we must".format(a + "ing")


def luke(a, b=None):
    if b is None:
        return "Luke > Not sure about {}. Don't I get a choice?".format(a + "ing")
    return "Luke > Sure, both {} and {} seems ok to me".format(a, b + "ing")

def obiwan(a, b=None):
    alternatives = ["reading", "talking", "sleeping", "fighting", "playing", "training"]
    b = random.choice(alternatives)
    response = f"Obi-Wan > Yes, {a}ing is an option. Or we could do some {b}."
    return response

def vader(a, b=None):
    action = a + "ing"
    bad_things = ["fighting", "killing", "choking", "conquering"]
    nice_things = ["cooking", "sleeping", "cuddling", "killing", "working", "flying", "reading", "playing"]

    if action in bad_things:
        return "Darth Vader > Yes! Time for {}!".format(action)
    elif action in nice_things:
        return "Darth Vader > What? {} is a waste of time!".format(action)
    return "Darth Vader > It doesn't interest me at all"
