import os


class PredictModel:
    def __init__(self, model_name="tmp", cache_dir=None, *args, **kwargs):
        self.model_name = model_name
        self.cache_dir = cache_dir or f"{os.getcwd()}/.funmodel/"
        os.makedirs(self.cache_path, exist_ok=True)

    @property
    def cache_path(self):
        return f"{self.cache_dir}/{self.model_name}"

    def load(self, *args, **kwargs):
        pass

    def predict(self, *args, **kwargs):
        pass
