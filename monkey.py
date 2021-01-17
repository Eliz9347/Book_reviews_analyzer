# This Python file uses the following encoding: utf-8

from monkeylearn import MonkeyLearn

MONKEY_API_KEY = ""  # нужно вставить api_key


class Monkey:
    def __init__(self, data):

        ml = MonkeyLearn(MONKEY_API_KEY)
        model_id = 'cl_pi3C7JiL'
        result = ml.classifiers.classify(model_id, data)
        res = result.body
        res1 = res[0]['classifications'][0]['tag_name']
        res2 = res[0]['classifications'][0]['confidence']
        self.full_res = res1 + ": " + str(res2)

    def get_res(self):
        return self.full_res
