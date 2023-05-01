# load model - look if there is a model saved in the model repository
# init model - make a model if there is no model saved in the model repository
#  - get data
# - if there is no data, make data
# - if there is data, load data
#  - train model
# - pure ModelService

# - test/train?


class ModelRepositoryInterface:
    pass


class ModelService:
    def __int__(self, model_repository: ModelRepositoryInterface):
        self.model_repository = model_repository

    def load_model(self):
        pass

    def init_model(self):
        pass
