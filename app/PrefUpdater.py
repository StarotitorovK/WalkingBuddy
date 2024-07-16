import queue
from typing import Dict
from pydantic import BaseModel, ConfigDict

Tags = Dict[str, float]


class Model(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed = True)


class MainPrefData(Model):
    """
    Info about user's preferences from his profile
    """

    person_id: int = 0
    old_tags: Tags
    cached_tags: queue.Queue[Tags]
    seen: int
    age: int = 18


class InputPrefData(Model):
    """
    Info about user's conversation with place object performance
    """

    person_id: int = 0
    tags: Tags
    rate: float


class PreparedPrefData(Model):
    """
    Prepared preferences for updating user's profile
    """

    tags: Tags


def get_main_pref_data(person_id: int) -> MainPrefData:
    """
    Get user's preferences from his profile
    """

    pass
    # return MainPrefData(person_id, {}, queue.Queue(), 0, 0)  # rewrite using pydantic


def prepare_pref_data(pref_data: InputPrefData) -> PreparedPrefData:
    """
    Prepare preferences for updating user's profile. Multiply weights of tags by rate
    """
    for key in pref_data.tags.keys():
        pref_data.tags[key] *= pref_data.rate
    return PreparedPrefData(tags=pref_data.tags)


def tags_recalc(prepared_pref_data: PreparedPrefData, main_pref_data: MainPrefData) -> MainPrefData:
    """
    Recalculate user's preferences based on his conversation with place object performance
    """
    if main_pref_data.cached_tags.full():  # if cache is full]
        old_record = main_pref_data.cached_tags.get()
        for key in old_record.keys():
            weight = main_pref_data.seen
            # calculate weighted mean of a tag
            main_pref_data.old_tags[key] = max((main_pref_data.old_tags[key] * weight + old_record[key]) / (weight + 1),
                                               0)
    main_pref_data.cached_tags.put(prepared_pref_data.tags)
    main_pref_data.seen += 1
    return main_pref_data
