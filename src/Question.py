import os
import json
import random
from src import Google_API, Google_datastore


class Question:

    def __init__(self, path):
        self.path = path

    def get_questions(self):
        # with open(self.path) as f:
        #     questions_json = json.load(f)
        # return questions_json['questions']
        ds = Google_datastore.Datastore()
        qns = ds.get_data()
        questions = [{"id": qn.id, "image": qn['image'], "label": qn['label'], "question": qn['question'],
                      "audio": qn['audio']} for qn in qns]
        return questions

    def random_questions(self, count):
        all_qns = [qn for qn in self.get_questions()]
        res_qns = []
        qns = 0
        while qns < count and len(all_qns) > 3:
            random.shuffle(all_qns)
            candidates = all_qns[:4]
            qn = random.choice(candidates)
            qn_id = qn['id']
            qn_str = qn['question']
            qn_options = [c['image'] for c in candidates]
            qn_answer = candidates.index(qn)+1
            candidates.remove(qn)
            all_qns.remove(qn)
            res_qns.append({
                "id": qn_id,
                "question": qn_str,
                "images": qn_options,
                "answer": qn_answer
            })
            qns += 1
        return res_qns

    @staticmethod
    def speech_answer(speech, answer):
        results = Google_API.speech_text(speech.read())
        return len(set.intersection(set(results), set({answer}))) > 0

    @staticmethod
    def create_questions(ds):
        q_id = 1
        qns = []
        src_qns = ds.get_data()
        src_qns = [{"id": qn.id} for qn in src_qns]
        ds.delete_data(src_qns)
        for file in os.listdir("resources/images"):
            if file.endswith(".jpg"):
                label = Google_API.annotate_image(os.path.join("resources/images", file))['labels'][0].description
                qn_str = "Which of the following images has {}"
                qn_str = qn_str.format(("an " if label.lower()[0] in ["a", "e", "i", "o", "u"] else "a ") + label)
                qn = {
                    "id": q_id,
                    "image": file,
                    "label": label,
                    "question": qn_str,
                    "audio": str(q_id)+".mp3"
                }
                qns.append(qn)
                q_id += 1
        Question.write_questions(qns, ds)
        Question.generate_questions_audio(qns)

    @staticmethod
    def write_questions(questions, ds):
        # with open(os.path.join('resources', 'questions.json'), 'w') as outfile:
        #     json.dump({"questions": questions}, outfile)
        [ds.add_data(q) for q in questions]


    @staticmethod
    def generate_questions_audio(questions):
        questions_dict = {}
        for q in questions:
            questions_dict[q['id']] = q['question']
        if questions_dict:
            Google_API.text_speech(questions_dict)
