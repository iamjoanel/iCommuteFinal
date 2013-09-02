from django.contrib.gis.db import models
from django.contrib.auth.models import User


valid_modes = (
    ('Jeep', "Jeep"),
    ('Walk', "Walk"),
    ('Bus', "Bus"),
)

valid_mrt_stations = (
    ('Taft Avenue Station', 'Taft Avenue Station'),
    ('Magallanes Station', 'Magallanes Station'),
    ('Ayala Station', 'Ayala Station'),
    ('Buendia Station', 'Buendia Station'),
    ('Guadalupe Station', 'Guadalupe Station'),
    ('Boni Avenue Station', 'Boni Avenue Station'),
    ('Shaw Boulevard Station', 'Shaw Boulevard Station'),
    ('Ortigas Avenue Station', 'Ortigas Avenue Station'),
    ('Santolan Anapoils Station', 'Santolan Anapoils Station'),
    ('Cubao Station', 'Cubao Station'),
    ('GMA - Kamuning Station', 'GMA - Kamuning Station'),
    ('Quezon Avenue Station', 'Quezon Avenue Station'),
    ('North Avenue Station', 'North Avenue Station'),
)


class Path(models.Model):
    origin_point = models.CharField(max_length=100)
    destination_point = models.CharField(max_length=100)
    mode = models.CharField(max_length=50, choices=valid_modes)
    distance = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    cost = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    time = models.TimeField()
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    path = models.LineStringField(srid=900913)
    objects = models.GeoManager()

    class Meta:
        verbose_name = ('Path')
        verbose_name_plural = ('Paths')
        db_table = "paths"
        ordering = ['origin_point', 'destination_point',]

    def __unicode__(self):
        return "From %s To %s via %s" % (self.origin_point, self.destination_point, self.mode)

    def __repr__(self):
        return "From %s To %s via %s" % (self.origin_point, self.destination_point, self.mode)


class TrainPath(models.Model):
    origin_station = models.CharField(max_length=50, choices=valid_mrt_stations)
    destination_station = models.CharField(max_length=50, choices=valid_mrt_stations)
    distance = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    cost = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    time = models.TimeField()
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    path = models.LineStringField(srid=900913)
    objects = models.GeoManager()

    class Meta:
        verbose_name = ('TrainPath')
        verbose_name_plural = ('TrainPaths')
        db_table = "train_paths"

    def __unicode__(self):
        return "From %s To %s via Train" % (self.origin_station, self.destination_station)

    def __repr__(self):
        return "From %s To %s via Train" % (self.origin_station, self.destination_station)


class Route(models.Model):
    origin = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    origin_city = models.CharField(max_length=50, blank=True)
    destination_city = models.CharField(max_length=50, blank=True)
    total_distance = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    total_cost = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    path = models.ManyToManyField(Path, blank=True)
    train_path = models.ManyToManyField(TrainPath, blank=True)
    created_by = models.ForeignKey(User)
    is_approved = models.BooleanField(default=False, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ('Route')
        verbose_name_plural = ('Routes')
        db_table = "routes"


    def __unicode__(self):
        return "From %s,%s To %s,%s" % (self.origin, self.origin_city, self.destination, self.destination_city)

    def __repr__(self):
        return "From %s,%s To %s,%s" % (self.origin, self.origin_city, self.destination, self.destination_city)
