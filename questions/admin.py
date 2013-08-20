from django.contrib import admin
from questions.models import *

class SessionAdmin(admin.ModelAdmin):
    pass
admin.site.register(AMASession, SessionAdmin)

class MetaAdmin(admin.ModelAdmin):
    pass
admin.site.register(UserMeta, MetaAdmin)

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

class RequestAdmin(admin.ModelAdmin):
    pass
admin.site.register(Request, RequestAdmin)

class SessionViewAdmin(admin.ModelAdmin):
    fields = ['session', 'user']

    def timestamp(self, obj):
        return obj.timestamp

    timestamp.short_description = "timestamp"
    timestamp.admin_order_field = "timestamp"

    list_display = ('session', 'user', 'user_session', 'timestamp')
admin.site.register(SessionView, SessionViewAdmin)
