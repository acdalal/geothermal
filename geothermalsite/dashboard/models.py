# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Channel(models.Model):
    dts_config = models.ForeignKey("DtsConfig", models.DO_NOTHING)
    channel_name = models.TextField()
    channel_length_m = models.FloatField()

    class Meta:
        managed = False
        db_table = "channel"


class DtsConfig(models.Model):
    dts_name = models.TextField()
    configuration_name = models.TextField()
    measurement_interval_s = models.FloatField(blank=True, null=True)
    step_increment_m = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "dts_config"


class DtsData(models.Model):
    measurement = models.ForeignKey("Measurement", models.DO_NOTHING)
    laf_m = models.FloatField()
    temperature_c = models.FloatField()
    elevation_m = models.FloatField()
    depth_m = models.FloatField()
    slope = models.FloatField()

    class Meta:
        managed = False
        db_table = "dts_data"


class Measurement(models.Model):
    channel = models.ForeignKey(Channel, models.DO_NOTHING)
    datetime_utc = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "measurement"
