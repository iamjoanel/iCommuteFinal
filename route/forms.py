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
        exclude = ('total_distance', 'total_cost', 'origin_city', 'destination_city', 'is_approved', 'created_by',)
        widgets = {
            'origin': forms.TextInput(attrs={'placeholder': "SM Mall of Asia, Pasay City", 'class': 'col_8'}),
            'destination': forms.TextInput(attrs={'placeholder': "SM Mall of Asia, Pasay City", 'class': 'col_8'}),
            'path': forms.SelectMultiple(attrs={'class': 'col_7'}),
            'train_path': forms.SelectMultiple(attrs={'class': 'col_7'}),
        }

    class Media:
        css = {'all': ['admin/css/widgets.css']}
        js = ['/admin/jsi18n/']

class SearchForm(forms.Form):
    origin = forms.CharField(widget=forms.TextInput(attrs={'type': "text", 'placeholder': "Origin", 'id': "origin", 'name': "origin", 'class': "text input"}))
    destination = forms.CharField(widget=forms.TextInput(attrs={'type': "text", 'placeholder': "Destination", 'id': "destination", 'name': "destination", 'class': "text input"}))

    def cleaned_origin(self):
        if self.cleaned_data['origin'] is None:
            raise forms.ValidationError("Some fields were left blank.")
        return self.cleaned_data['origin']

    def cleaned_destination(self):
        if self.cleaned_data['destination'] is None:
            raise forms.ValidationError("Some fields were left blank.")
        return self.cleaned_data['destination']
