# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserMeta'
        db.create_table('questions_usermeta', (
            ('user', self.gf('annoying.fields.AutoOneToOneField')(to=orm['auth.User'], unique=True, related_name='meta', primary_key=True)),
            ('verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('questions', ['UserMeta'])

        # Adding model 'AMASession'
        db.create_table('questions_amasession', (
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, unique=True, primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], related_name='sessions')),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('subtitle', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('desc', self.gf('django.db.models.fields.TextField')()),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('data', self.gf('jsonfield.fields.JSONField')(blank=True, default={})),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('edited', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('questions', ['AMASession'])

        # Adding model 'SessionView'
        db.create_table('questions_sessionview', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questions.AMASession'], related_name='viewers')),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], related_name='views', null=True)),
            ('user_session', self.gf('django.db.models.fields.related.ForeignKey')(on_delete=models.SET_NULL, to=orm['sessions.Session'], related_name='views', null=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('questions', ['SessionView'])

        # Adding model 'AMAQuestion'
        db.create_table('questions_amaquestion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('asker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], related_name='own_questions')),
            ('target', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], related_name='asked_questions')),
            ('question', self.gf('django.db.models.fields.TextField')()),
            ('desc', self.gf('django.db.models.fields.TextField')(default='')),
            ('starred', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('data', self.gf('jsonfield.fields.JSONField')(blank=True, default={})),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questions.AMASession'], related_name='questions')),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('edited', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('questions', ['AMAQuestion'])

        # Adding model 'AMAAnswer'
        db.create_table('questions_amaanswer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['questions.AMAQuestion'], unique=True, related_name='answer')),
            ('response', self.gf('django.db.models.fields.TextField')()),
            ('data', self.gf('jsonfield.fields.JSONField')(blank=True, default={})),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('edited', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('questions', ['AMAAnswer'])

        # Adding model 'AMAVote'
        db.create_table('questions_amavote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], related_name='votes')),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questions.AMAQuestion'], related_name='votes')),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('edited', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('questions', ['AMAVote'])

        # Adding unique constraint on 'AMAVote', fields ['user', 'question']
        db.create_unique('questions_amavote', ['user_id', 'question_id'])

        # Adding model 'Request'
        db.create_table('questions_request', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('provider', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('desc', self.gf('django.db.models.fields.TextField')()),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(on_delete=models.SET_NULL, to=orm['questions.AMASession'], related_name='requests', null=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('edited', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('questions', ['Request'])

        # Adding unique constraint on 'Request', fields ['username', 'provider']
        db.create_unique('questions_request', ['username', 'provider'])

        # Adding model 'RequestVote'
        db.create_table('questions_requestvote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], related_name='request_votes')),
            ('request', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questions.Request'], related_name='votes')),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('edited', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('questions', ['RequestVote'])

        # Adding unique constraint on 'RequestVote', fields ['user', 'request']
        db.create_unique('questions_requestvote', ['user_id', 'request_id'])

        # Adding model 'Comment'
        db.create_table('questions_comment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questions.AMAQuestion'], related_name='comments')),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], related_name='comments')),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('edited', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('questions', ['Comment'])


    def backwards(self, orm):
        # Removing unique constraint on 'RequestVote', fields ['user', 'request']
        db.delete_unique('questions_requestvote', ['user_id', 'request_id'])

        # Removing unique constraint on 'Request', fields ['username', 'provider']
        db.delete_unique('questions_request', ['username', 'provider'])

        # Removing unique constraint on 'AMAVote', fields ['user', 'question']
        db.delete_unique('questions_amavote', ['user_id', 'question_id'])

        # Deleting model 'UserMeta'
        db.delete_table('questions_usermeta')

        # Deleting model 'AMASession'
        db.delete_table('questions_amasession')

        # Deleting model 'SessionView'
        db.delete_table('questions_sessionview')

        # Deleting model 'AMAQuestion'
        db.delete_table('questions_amaquestion')

        # Deleting model 'AMAAnswer'
        db.delete_table('questions_amaanswer')

        # Deleting model 'AMAVote'
        db.delete_table('questions_amavote')

        # Deleting model 'Request'
        db.delete_table('questions_request')

        # Deleting model 'RequestVote'
        db.delete_table('questions_requestvote')

        # Deleting model 'Comment'
        db.delete_table('questions_comment')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'questions.amaanswer': {
            'Meta': {'object_name': 'AMAAnswer'},
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'data': ('jsonfield.fields.JSONField', [], {'blank': 'True', 'default': '{}'}),
            'edited': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['questions.AMAQuestion']", 'unique': 'True', 'related_name': "'answer'"}),
            'response': ('django.db.models.fields.TextField', [], {})
        },
        'questions.amaquestion': {
            'Meta': {'object_name': 'AMAQuestion'},
            'asker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'related_name': "'own_questions'"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'data': ('jsonfield.fields.JSONField', [], {'blank': 'True', 'default': '{}'}),
            'desc': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'edited': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questions.AMASession']", 'related_name': "'questions'"}),
            'starred': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'related_name': "'asked_questions'"})
        },
        'questions.amasession': {
            'Meta': {'object_name': 'AMASession'},
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'data': ('jsonfield.fields.JSONField', [], {'blank': 'True', 'default': '{}'}),
            'desc': ('django.db.models.fields.TextField', [], {}),
            'edited': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'related_name': "'sessions'"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'primary_key': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'questions.amavote': {
            'Meta': {'object_name': 'AMAVote', 'unique_together': "(('user', 'question'),)"},
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'edited': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questions.AMAQuestion']", 'related_name': "'votes'"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'related_name': "'votes'"}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'questions.comment': {
            'Meta': {'object_name': 'Comment'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'edited': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questions.AMAQuestion']", 'related_name': "'comments'"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'related_name': "'comments'"})
        },
        'questions.request': {
            'Meta': {'object_name': 'Request', 'unique_together': "(('username', 'provider'),)"},
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {}),
            'edited': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'provider': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'on_delete': 'models.SET_NULL', 'to': "orm['questions.AMASession']", 'related_name': "'requests'", 'null': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'questions.requestvote': {
            'Meta': {'object_name': 'RequestVote', 'unique_together': "(('user', 'request'),)"},
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'edited': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'request': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questions.Request']", 'related_name': "'votes'"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'related_name': "'request_votes'"}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'questions.sessionview': {
            'Meta': {'object_name': 'SessionView'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questions.AMASession']", 'related_name': "'viewers'"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'related_name': "'views'", 'null': 'True'}),
            'user_session': ('django.db.models.fields.related.ForeignKey', [], {'on_delete': 'models.SET_NULL', 'to': "orm['sessions.Session']", 'related_name': "'views'", 'null': 'True'})
        },
        'questions.usermeta': {
            'Meta': {'object_name': 'UserMeta'},
            'user': ('annoying.fields.AutoOneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'related_name': "'meta'", 'primary_key': 'True'}),
            'verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'sessions.session': {
            'Meta': {'object_name': 'Session', 'db_table': "'django_session'"},
            'expire_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'session_data': ('django.db.models.fields.TextField', [], {}),
            'session_key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True'})
        }
    }

    complete_apps = ['questions']