import io
import os

from google.cloud import vision
from google.cloud.vision import types


class ProcessImage:
    file_name = None
    client = None
    image = None
    results = dict(objects=[], explicit_content=None)

    def __init__(self, file_name):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'apiKey.json'
        self.file_name = file_name
        self.client = vision.ImageAnnotatorClient()

    def get_vision_client(self):
        return self.client

    def read_image(self):
        if not self.file_name or not self.client:
            return None

        with io.open(self.file_name, 'rb') as image_file:
            content = image_file.read()

        self.image = types.Image(content=content)

        return self

    def _get_explicit_info(self, content):
        likelihood = [
            'Unknown', 'Very Unlikely', 'Unlikely', 'Possible',
            'Likely', 'Very Likely'
        ]
        return dict(
            adult=likelihood[content.adult],
            spoof=likelihood[content.spoof],
            medical=likelihood[content.medical],
            violence=likelihood[content.violence],
            racy=likelihood[content.racy]
        )

    def execute_detection(self):
        labels = self.client.label_detection(image=self.image)
        explicit_content = self.client.safe_search_detection(image=self.image)
        objects = labels.label_annotations
        print(explicit_content)
        # likeli_hoods = explicit_content.safe_search_annotation
        self.results['objects'] = [label.description for label in objects]
        self.results['explicit_content'] = self._get_explicit_info(explicit_content.safe_search_annotation)

        return self.results
