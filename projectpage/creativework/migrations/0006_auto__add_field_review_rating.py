# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Review.rating'
        db.add_column('review', 'rating',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Review.rating'
        db.delete_column('review', 'rating')


    models = {
        u'creativework.episodebase': {
            'Meta': {'ordering': "['-created']", 'object_name': 'EpisodeBase', 'db_table': "'episodes'", '_ormbases': [u'creativework.Thing']},
            'image': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'likes': ('django.db.models.fields.IntegerField', [], {}),
            'meta_description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'meta_keywords': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'season': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['creativework.Season']", 'symmetrical': 'False'}),
            'series': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['creativework.Series']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            u'thing_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['creativework.Thing']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'creativework.genre': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Genre', 'db_table': "'genre'", '_ormbases': [u'creativework.Thing']},
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'meta_description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'meta_keywords': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            u'thing_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['creativework.Thing']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'creativework.resourceurl': {
            'Meta': {'object_name': 'ResourceURL'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'creativework.review': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Review', 'db_table': "'review'", '_ormbases': [u'creativework.Thing']},
            'helpful': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_flagged': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'meta_description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'meta_keywords': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'reviewtext': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'series': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['creativework.Series']", 'unique': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            u'thing_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['creativework.Thing']", 'unique': 'True', 'primary_key': 'True'}),
            'unelpful': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'creativework.season': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Season', 'db_table': "'seasons'", '_ormbases': [u'creativework.Thing']},
            'endDate': ('django.db.models.fields.DateField', [], {}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'meta_description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'meta_keywords': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'numberOfEpisodes': ('django.db.models.fields.IntegerField', [], {}),
            'partOfSeries': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['creativework.Series']", 'symmetrical': 'False'}),
            'seasonNumber': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'startDate': ('django.db.models.fields.DateField', [], {}),
            u'thing_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['creativework.Thing']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'creativework.series': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Series', 'db_table': "'series'", '_ormbases': [u'creativework.Thing']},
            'endDate': ('django.db.models.fields.DateField', [], {}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'meta_description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'meta_keywords': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'numberOfSeasons': ('django.db.models.fields.IntegerField', [], {}),
            'partOfGenres': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['creativework.Genre']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'startDate': ('django.db.models.fields.DateField', [], {}),
            u'thing_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['creativework.Thing']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'creativework.thing': {
            'Meta': {'object_name': 'Thing'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'hackUrl': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['creativework']