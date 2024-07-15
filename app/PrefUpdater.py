import queue
from typing import Dict

Tags = Dict[str, float]


class MainPrefData:
    """
    Info about user's preferences from his profile
    """

    def __init__(self, person_id: int, old_tags: Tags, cached_tags: queue.Queue[Tags], seen: int, age: int):
        self.person_id = person_id
        self.cached_tags = cached_tags
        self.old_tags = old_tags
        self.seen = seen
        self.age = age


class InputPrefData:
    """
    Info about user's conversation with place object performance
    """

    def __init__(self, person_id: int, rate: float, tags: Tags):
        self.person_id = person_id
        self.tags = tags
        self.rate = rate


class PreparedPrefData:
    """
    Prepared preferences for updating user's profile
    """

    def __init__(self, tags: Tags):
        self.tags = tags


def get_main_pref_data(person_id: int) -> MainPrefData:
    """
    Get user's preferences from his profile
    """
    return MainPrefData(person_id, {}, queue.Queue(), 0, 0)


def prepare_pref_data(pref_data: InputPrefData) -> PreparedPrefData:
    """
    Prepare preferences for updating user's profile. Multiply weights of tags by rate

    Now rate may be -1, 0.5 or 1. It's not good. We should have a rate for each user. So, I'll leave it as is.
    """
    for key in pref_data.tags.keys():
        pref_data.tags[key] *= pref_data.rate
    return PreparedPrefData(pref_data.tags)


def tags_recalc(prepared_pref_data: PreparedPrefData, main_pref_data: MainPrefData) -> MainPrefData:
    """
    Recalculate user's preferences based on his conversation with place object performance
    """
    if main_pref_data.cached_tags.full():  # if cache is full
        old_record = main_pref_data.cached_tags.get()
        for key in old_record.keys():
            weight = main_pref_data.seen
            # calculate weighted mean of a tag
            main_pref_data.old_tags[key] = (main_pref_data.old_tags[key] * weight + old_record[key]) / (weight + 1)
    main_pref_data.cached_tags.put(prepared_pref_data.tags)
    main_pref_data.seen += 1
    return main_pref_data
