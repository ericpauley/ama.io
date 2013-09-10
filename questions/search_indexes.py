import datetime
from haystack import indexes
from questions.models import AMASession

class AMASessionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    owner = indexes.CharField(model_attr='user')
    start_time = indexes.DateTimeField(model_attr='start_time')
    end_time = indexes.DateTimeField(model_attr='end_time')

    def get_model(self):
        return AMASession

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
