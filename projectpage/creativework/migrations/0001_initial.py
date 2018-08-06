# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'URL'
        db.create_table(u'creativework_url', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'creativework', ['URL'])

        # Adding model 'Thing'
        db.create_table(u'creativework_thing', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'creativework', ['Thing'])

        # Adding model 'Genre'
        db.create_table('genre', (
            (u'thing_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['creativework.Thing'], unique=True, primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'creativework', ['Genre'])

        # Adding model 'Series'
        db.create_table('series', (
            (u'thing_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['creativework.Thing'], unique=True, primary_key=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
            ('numberOfSeasons', self.gf('django.db.models.fields.IntegerField')()),
            ('startDate', self.gf('django.db.models.fields.DateField')()),
            ('endDate', self.gf('django.db.models.fields.DateField')()),
            ('meta_keywords', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('meta_description', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'creativework', ['Series'])

        # Adding M2M table for field partOfGenres on 'Series'
        db.create_table('series_partOfGenres', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('series', models.ForeignKey(orm[u'creativework.series'], null=False)),
            ('genre', models.ForeignKey(orm[u'creativework.genre'], null=False))
        ))
        db.create_unique('series_partOfGenres', ['series_id', 'genre_id'])

        # Adding model 'Season'
        db.create_table('seasons', (
            (u'thing_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['creativework.Thing'], unique=True, primary_key=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
            ('numberOfEpisodes', self.gf('django.db.models.fields.IntegerField')()),
            ('startDate', self.gf('django.db.models.fields.DateField')()),
            ('endDate', self.gf('django.db.models.fields.DateField')()),
            ('seasonNumber', self.gf('django.db.models.fields.IntegerField')()),
            ('meta_keywords', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('meta_description', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'creativework', ['Season'])

        # Adding M2M table for field partOfSeries on 'Season'
        db.create_table('seasons_partOfSeries', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('season', models.ForeignKey(orm[u'creativework.season'], null=False)),
            ('series', models.ForeignKey(orm[u'creativework.series'], null=False))
        ))
        db.create_unique('seasons_partOfSeries', ['season_id', 'series_id'])

        # Adding model 'EpisodeBase'
        db.create_table('episodes', (
            (u'thing_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['creativework.Thing'], unique=True, primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
            ('image', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('meta_keywords', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('meta_description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('likes', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'creativework', ['EpisodeBase'])

        # Adding M2M table for field series on 'EpisodeBase'
        db.create_table('episodes_series', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('episodebase', models.ForeignKey(orm[u'creativework.episodebase'], null=False)),
            ('series', models.ForeignKey(orm[u'creativework.series'], null=False))
        ))
        db.create_unique('episodes_series', ['episodebase_id', 'series_id'])

        # Adding M2M table for field season on 'EpisodeBase'
        db.create_table('episodes_season', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('episodebase', models.ForeignKey(orm[u'creativework.episodebase'], null=False)),
            ('season', models.ForeignKey(orm[u'creativework.season'], null=False))
        ))
        db.create_unique('episodes_season', ['episodebase_id', 'season_id'])


    def backwards(self, orm):
        # Deleting model 'URL'
        db.delete_table(u'creativework_url')

        # Deleting model 'Thing'
        db.delete_table(u'creativework_thing')

        # Deleting model 'Genre'
        db.delete_table('genre')

        # Deleting model 'Series'
        db.delete_table('series')

        # Removing M2M table for field partOfGenres on 'Series'
        db.delete_table('series_partOfGenres')

        # Deleting model 'Season'
        db.delete_table('seasons')

        # Removing M2M table for field partOfSeries on 'Season'
        db.delete_table('seasons_partOfSeries')

        # Deleting model 'EpisodeBase'
        db.delete_table('episodes')

        # Removing M2M table for field series on 'EpisodeBase'
        db.delete_table('episodes_series')

        # Removing M2M table for field season on 'EpisodeBase'
        db.delete_table('episodes_season')


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
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            u'thing_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['creativework.Thing']", 'unique': 'True', 'primary_key': 'True'})
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'creativework.url': {
            'Meta': {'object_name': 'URL'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['creativework']