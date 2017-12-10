import json


class JsonSaver:
    @staticmethod
    def save(path, items):
        with open(path, 'w', encoding='utf8') as outfile:
            for item in items:
                d_json = json.dumps(item, ensure_ascii=False)
                outfile.write(d_json + ',' + '\n')
