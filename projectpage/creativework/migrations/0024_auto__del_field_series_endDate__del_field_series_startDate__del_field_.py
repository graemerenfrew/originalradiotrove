# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Series.endDate'
        db.delete_column('series', 'endDate')

        # Deleting field 'Series.startDate'
        db.delete_column('series', 'startDate')

        # Deleting field 'Series.mainimg'
        db.delete_column('series', 'mainimg')

        # Deleting field 'Season.startDate'
        db.delete_column('seasons', 'startDate')

        # Deleting field 'Season.endDate'
        db.delete_column('seasons', 'endDate')

        # Deleting field 'EpisodeBase.image'
        db.delete_column('episodes', 'image')

        # Deleting field 'Thing.hackUrl'
        db.delete_column(u'creativework_thing', 'hackUrl')


    def backwards(self, orm):
        # Adding field 'Series.endDate'
        db.add_column('series', 'endDate',
                      self.gf('django.db.models.fields.DateField')(default=None),
                      keep_default=False)

        # Adding field 'Series.startDate'
        db.add_column('series', 'startDate',
                      self.gf('django.db.models.fields.DateField')(default=None),
                      keep_default=False)

        # Adding field 'Series.mainimg'
        db.add_column('series', 'mainimg',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Season.startDate'
        db.add_column('seasons', 'startDate',
                      self.gf('django.db.models.fields.DateField')(default=None),
                      keep_default=False)

        # Adding field 'Season.endDate'
        db.add_column('seasons', 'endDate',
                      self.gf('django.db.models.fields.DateField')(default=None),
                      keep_default=False)

        # Adding field 'EpisodeBase.image'
        db.add_column('episodes', 'image',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50),
                      keep_default=False)

        # Adding field 'Thing.hackUrl'
        db.add_column(u'creativework_thing', 'hackUrl',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=200),
                      keep_default=False)


    models = {
        u'creativework.contentsource': {
            'Meta': {'object_name': 'ContentSource', '_ormbases': [u'creativework.Thing']},
            'meta_description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'meta_keywords': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'thing_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['creativework.Thing']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'creativework.episodebase': {
            'Meta': {'ordering': "['-created']", 'object_name': 'EpisodeBase', 'db_table': "'episodes'", '_ormbases': [u'creativework.Thing']},
            'audioFileLocation': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'broadcastDate': ('django.db.models.fields.DateField', [], {'default': "'1970-01-01'"}),
            'episodeNumber': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'length': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'likes': ('django.db.models.fields.IntegerField', [], {}),
            'meta_description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'meta_keywords': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['creativework.Season']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            u'thing_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['creativework.Thing']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        u'creativework.genre': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Genre', 'db_table': "'genre'", '_ormbases': [u'creativework.Thing']},
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'meta_description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'meta_keywords': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'partOfParentGenres': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['creativework.ParentGenre']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            u'thing_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['creativework.Thing']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'creativework.parentgenre': {
            'Meta': {'ordering': "['-created']", 'object_name': 'ParentGenre', 'db_table': "'parentgenre'", '_ormbases': [u'creativework.Thing']},
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
            'audioFolder': ('django.db.models.fields.CharField', [], {'default': "'/'", 'max_length': '1000'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'meta_description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'meta_keywords': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'numberOfEpisodes': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'partOfSeries': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['creativework.Series']"}),
            'seasonNumber': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            u'thing_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['creativework.Thing']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'creativework.series': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Series', 'db_table': "'series'", '_ormbases': [u'creativework.Thing']},
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'likes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'meta_description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'meta_keywords': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'numberOfSeasons': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'partOfGenres': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['creativework.Genre']", 'symmetrical': 'False'}),
            'partOfParentGenres': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['creativework.ParentGenre']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            u'thing_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['creativework.Thing']", 'unique': 'True', 'primary_key': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'viewcount': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'creativework.thing': {
            'Meta': {'object_name': 'Thing'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['creativework']