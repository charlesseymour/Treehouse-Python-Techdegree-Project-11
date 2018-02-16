import json
from os import environ, path
import sys

import django

BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))

PROJECT_DIR = path.dirname(BASE_DIR)

sys.path.insert(0, PROJECT_DIR)


def main():
    try:
        from pugorugh.serializers import DogSerializer
    except ImportError:
        raise ImportError("DogSerializer not implemented in serializers.py")

    json_file = path.join(PROJECT_DIR,
                          'pugorugh',
                          'static',
                          'dog_details.json')

    with open(json_file, 'r') as file:
        data = json.load(file)
        serializer = DogSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)


if __name__ == '__main__':
    environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
    django.setup()
    main()
