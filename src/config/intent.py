from discord import Intents


def remove_unused_intent(intents: Intents) -> Intents:
    intents.typing = False
    intents.presences = False
    return intents


def get_full_intents() -> Intents:
    return remove_unused_intent(Intents.all())
