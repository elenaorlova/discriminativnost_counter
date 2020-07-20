import json
import numpy as np


class Answer:
    def __init__(self, id, task_results):
        self.id = id
        self.task_result = task_results
        self.number_of_tasks = len(task_results)
        self.correct_answer_percentage = 0


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


class Counter:
    @staticmethod
    def parcer(data):
        person_results = []
        convered_data = json.loads(data)
        results = convered_data['RESULTS']

        for person in results:
            for key, value in person.items():
                if value == 'N' or value == 'Z!' or value == 'X':
                    person[key] = -1
                elif value == 'Z':
                    person[key] = 0
        number_of_people = len(results)
        for i in range(number_of_people):
            person_info = list(results[i].values())
            person_results.append(Answer(person_info[0], np.array([int(x) for x in person_info[1:]])))
        return person_results

    @staticmethod
    def get_right_tasks_percent(test_data):
        for person in test_data:
            person.correct_answer_percentage = Counter.count_right_answers(person) / test_data[0].number_of_tasks
        return test_data

    @staticmethod
    def count_right_answers(person):
        return np.sum(np.array([x for x in person.task_result if x >= 0]))

    @staticmethod
    def get_high_group(data):
        data = sorted(data, key=lambda answer: answer.correct_answer_percentage)
        data_size = len(data)
        line = round(data_size * 0.3) - 1
        high_percentage = data[data_size - line].correct_answer_percentage
        high_data = [x for x in data if x.correct_answer_percentage >= high_percentage]
        return high_data

    @staticmethod
    def get_low_group(data):
        sorted_data = sorted(data, key=lambda answer: answer.correct_answer_percentage)
        data_size = len(sorted_data)
        line = round(data_size * 0.3) - 1
        low_percentage = sorted_data[0 + line].correct_answer_percentage
        low_data = [x for x in sorted_data if x.correct_answer_percentage <= low_percentage]
        return low_data

    @staticmethod
    def count_right_answers_in_tasks(data):
        tasks_a = []
        for i in range(data[0].number_of_tasks):
            task_summ = 0
            for person in data:
                if person.task_result[i] == 1:
                    task_summ += 1
            tasks_a.append(task_summ)
        return np.array(tasks_a)

    @staticmethod
    def count_wrong_answers_in_tasks(data):
        tasks_a = []
        for i in range(data[0].number_of_tasks):
            task_summ = 0
            for person in data:
                if person.task_result[i] == 0:
                    task_summ += 1
            tasks_a.append(task_summ)
        return np.array(tasks_a)

    @staticmethod
    def count_dc(high_group, low_group):
        dc = []
        a = Counter.count_right_answers_in_tasks(high_group)
        b = Counter.count_right_answers_in_tasks(low_group)
        c = Counter.count_wrong_answers_in_tasks(high_group)
        d = Counter.count_wrong_answers_in_tasks(low_group)
        for i in range(high_group[0].number_of_tasks):
            dc.append(a[i] / (a[i] + c[i]) - b[i] / (b[i] + d[i]))
        return np.array(dc)


fd = open("req.txt", "r")
# data - this is our request
data = fd.read()

# parce data
person_results = Counter.parcer(data)
# calculate percentage
test_data = Counter.get_right_tasks_percent(np.array(person_results))
# groups creation
high_group = Counter.get_high_group(test_data)
low_group = Counter.get_low_group(test_data)
# dc calculation
dc = Counter.count_dc(high_group, low_group)

# сериализация результатов в JSON
json_dump = json.dumps({'DC': dc}, cls=NumpyEncoder)
print(json_dump)