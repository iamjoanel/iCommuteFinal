import floppyforms as forms

from .models import (Path, Route, TrainPath)


class OsmLineStringWidget(forms.gis.BaseOsmWidget, forms.gis.LineStringWidget):
    template_name = "includes/custom_lonlat.html"
    map_srid = 900913
    default_lon = 121.032
    default_lat = 14.594
    default_zoom = 12
    is_linestring = True

    def get_context_data(self):
        ctx = super(OsmLineStringWidget, self).get_context_data()
        ctx.update({
                'lon': self.default_lon,
                'lat': self.default_lat,
                'zoom': self.default_zoom
            })
        return ctx


class PathForm(forms.ModelForm):
    class Meta:
        model = Path
        exclude = ('cost', 'distance',)
        widgets = {
            'origin_point': forms.TextInput(attrs={'placeholder': "Origin Point"}),
            'destination_point': forms.TextInput(attrs={'placeholder': "Destination Point"}),
            'time': forms.TextInput(attrs={'placeholder': "00:00:00"}),
            'path': OsmLineStringWidget
        }


class TrainPathForm(forms.ModelForm):
    class Meta:
        model = TrainPath
        exclude = ('cost', 'distance',)
        widgets = {
            'origin_station': forms.Select(),
            'destination_station': forms.Select(),
            'time': forms.TextInput(attrs={'placeholder': "00:00:00"}),
            'path': OsmLineStringWidget
        }


class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        exclude = ('total_distance', 'total_cost', 'origin_city', 'destination_city', 'is_approved',)
        widgets = {
            'origin': forms.TextInput(attrs={'placeholder': "Origin"}),
            'destination': forms.TextInput(attrs={'placeholder': "Destination"}),
            'path': forms.SelectMultiple(),
            'train_path': forms.SelectMultiple(),
        }

    class Media:
        css = {'all': ['admin/css/widgets.css']}
        js = ['/admin/jsi18n/']
