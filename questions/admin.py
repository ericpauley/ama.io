from django.contrib import admin
from questions.models import AMASession, AMAQuestion, AMAAnswer, AMAVote

class SessionAdmin(admin.ModelAdmin):
    pass
admin.site.register(AMASession, SessionAdmin)

class QuestionAdmin(admin.ModelAdmin):
    fields = ["question", "score"]

    def queryset(self, request):
        qs = super(FixtureAdmin, self).queryset(request)
        return qs.annotate(num_fixture_metas=Count('fixturemeta')).annotate(score=Sum('votes__value'))
        
    def score(self, obj):
        return obj.score
    score.short_description = "Score"
    score.admin_order_field = "score"
admin.site.register(AMAQuestion, SessionAdmin)

class AnswerAdmin(admin.ModelAdmin):
    pass
admin.site.register(AMAAnswer, SessionAdmin)