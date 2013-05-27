# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from new_album.settings import MEDIA_ROOT
from PIL import Image as PImage
from string import join
from django.core.files import File
from os.path import join as pjoin
from tempfile import *
from django.conf import settings
import os

class Category(models.Model):

	name = models.CharField(max_length=100)
	number = models.IntegerField()
	status = models.BooleanField()
	img = models.ImageField(upload_to='photo/menu_img/')
	lang = models.CharField(max_length = 2)
	meta_key = models.TextField()
	meta_description = models.TextField()

	def __unicode__(self):
		return self.name


class Album(models.Model):
	lang = models.CharField(max_length = 2)
	title_album = models.CharField(max_length=60)
	menu_id = models.ForeignKey('Category')
	meta_key = models.TextField()
	meta_description = models.TextField()

	public = models.BooleanField(default=False)
	def images(self):
		lst = [x.image.name for x in self.image_set.all()]
		lst = ["<a href='/media/%s'>%s</a>" % (x, x.split('/')[-1]) for x in lst]
		return join(lst, ',')
	images.allow_tags = True

class Tag(models.Model):
	lang = models.CharField(max_length = 2)
	tag = models.CharField(max_length=50)
	def __unicode__(self):
		return self.tag


class Image(models.Model):
	lang = models.CharField(max_length = 2)
	title = models.CharField(max_length=60, blank=True, null=True)
	image = models.FileField(upload_to="images/")
	id_photo_gallery = models.BooleanField()
	main_photo = models.BooleanField()
	tags = models.ManyToManyField(Tag, blank=True)
	albums = models.ManyToManyField(Album, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	rating = models.IntegerField(blank=True, null=True)
	width = models.IntegerField(blank=True, null=True)
	height = models.IntegerField(blank=True, null=True)
	user = models.ForeignKey(User, null=True, blank=True)
	meta_key = models.TextField()
	meta_description = models.TextField()

	thumbnail2 = models.ImageField(upload_to="images/", blank=True, null=True)
	thumbnail = models.ImageField(upload_to="images/", blank=True, null=True)

	def save(self, *args, **kwargs):
		"""Save image dimensions."""
		super(Image, self).save(*args, **kwargs)
		im = PImage.open(pjoin(MEDIA_ROOT, self.image.name))
		self.width, self.height = im.size

		# large thumbnail
		fn, ext = os.path.splitext(self.image.name)
		im.thumbnail((128, 128), PImage.ANTIALIAS)
		thumb_fn = fn + "-thumb2" + ext
		tf2 = NamedTemporaryFile()
		im.save(tf2.name, "JPEG")
		self.thumbnail2.save(thumb_fn, File(open(tf2.name)), save=False)
		tf2.close()

		# small thumbnail

		fn, ext = os.path.splitext(self.image.name)
		im.thumbnail((40, 40), PImage.ANTIALIAS)
		thumb_fn = fn + "-thumb" + ext
		tf = NamedTemporaryFile()
		im.save(tf.name, "JPEG")
		self.thumbnail.save(thumb_fn, File(open(tf.name)), save=False)
		tf.close()

		super(Image, self).save(*args, **kwargs)


	def thumbnail3(self):
		return """<a href="/media/%s"><img border="0" alt="" src="/media/%s" height="40" /></a>""" % (
		(self.image.name, self.image.name))
	thumbnail3.allow_tags = True

# pokazat vtoruu kartinku v adminke
#	def thumbnail(self):
#		return """<a href="/media/%s"><img border="0" alt="" src="/media/%s" height="40" /></a>""" % (
#		(self.image.name, self.image.name))
#	thumbnail.allow_tags = True


	def size(self):
		""" Image size		"""
		return "%s x %s" % (self.width, self.height)

	def __unicode__(self):
		return self.image.name

	def tags_(self):
		lst = [x[1] for x in self.tags.values_list()]
		return str(join(lst, ','))

	def albums_(self):
		lst = [x[1] for x in self.albums.values_list()]
		return str(join(lst, ','))


class CategoryAdmin(admin.ModelAdmin):

#	list_display = ["meta_description"]
#	list_display = ["number"]
#	list_display = ["lang"]
#	list_display = ["meta_key"]
	list_display = ["name"]


class AlbumAdmin(admin.ModelAdmin):
#	search_fields = ["title"]
	list_display = ["title_album"]
#	list_display = ["lang"]
#	list_display = ["meta_key"]
#	list_display = ["meta_description"]


class TagAdmin(admin.ModelAdmin):
	list_display = ["tag"]
	list_display = ["lang"]


class ImageAdmin(admin.ModelAdmin):
	# search_fields = ["title"]
	list_display = ["__unicode__", "title", "user", "lang", "rating", "size",
					"tags_", "meta_key", "meta_description", "albums_",
					 "thumbnail3", "created"]
	list_filter = ["tags", "albums", "user"]

	def save_model(self, request, obj, form, change):
		obj.user = request.user
		obj.save()

admin.site.register(Album, AlbumAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Category, CategoryAdmin)
