# locations/migrations/0001_initial.py
from django.db import migrations, models


NIGERIAN_STATES = [
    {"name": "Abia", "capital": "Umuahia", "lat": 5.5249, "lon": 7.4943, "abbr": "AB"},
    {"name": "Adamawa", "capital": "Yola", "lat": 9.3233, "lon": 12.4381, "abbr": "AD"},
    {"name": "Akwa Ibom", "capital": "Uyo", "lat": 4.9757, "lon": 7.9361, "abbr": "AK"},
    {"name": "Anambra", "capital": "Awka", "lat": 6.2104, "lon": 7.0691, "abbr": "AN"},
    {"name": "Bauchi", "capital": "Bauchi", "lat": 10.3158, "lon": 9.8442, "abbr": "BA"},
    {"name": "Bayelsa", "capital": "Yenagoa", "lat": 4.9281, "lon": 6.2676, "abbr": "BY"},
    {"name": "Benue", "capital": "Makurdi", "lat": 7.7322, "lon": 8.5391, "abbr": "BE"},
    {"name": "Borno", "capital": "Maiduguri", "lat": 11.8469, "lon": 13.1571, "abbr": "BO"},
    {"name": "Cross River", "capital": "Calabar", "lat": 4.9602, "lon": 8.3405, "abbr": "CR"},
    {"name": "Delta", "capital": "Asaba", "lat": 5.4167, "lon": 6.1833, "abbr": "DE"},
    {"name": "Ebonyi", "capital": "Abakaliki", "lat": 6.3249, "lon": 8.1123, "abbr": "EB"},
    {"name": "Edo", "capital": "Benin City", "lat": 6.3340, "lon": 5.6037, "abbr": "ED"},
    {"name": "Ekiti", "capital": "Ado-Ekiti", "lat": 7.6210, "lon": 5.2192, "abbr": "EK"},
    {"name": "Enugu", "capital": "Enugu", "lat": 6.5244, "lon": 7.4795, "abbr": "EN"},
    {"name": "Gombe", "capital": "Gombe", "lat": 10.2897, "lon": 11.1673, "abbr": "GO"},
    {"name": "Imo", "capital": "Owerri", "lat": 5.4920, "lon": 7.0261, "abbr": "IM"},
    {"name": "Jigawa", "capital": "Dutse", "lat": 11.7992, "lon": 9.3509, "abbr": "JI"},
    {"name": "Kaduna", "capital": "Kaduna", "lat": 10.5105, "lon": 7.4165, "abbr": "KD"},
    {"name": "Kano", "capital": "Kano", "lat": 12.0022, "lon": 8.5920, "abbr": "KN"},
    {"name": "Katsina", "capital": "Katsina", "lat": 12.9815, "lon": 7.6006, "abbr": "KT"},
    {"name": "Kebbi", "capital": "Birnin Kebbi", "lat": 12.4509, "lon": 4.1999, "abbr": "KE"},
    {"name": "Kogi", "capital": "Lokoja", "lat": 7.7337, "lon": 6.6907, "abbr": "KO"},
    {"name": "Kwara", "capital": "Ilorin", "lat": 8.4966, "lon": 4.5421, "abbr": "KW"},
    {"name": "Lagos", "capital": "Ikeja", "lat": 6.5244, "lon": 3.3792, "abbr": "LA"},
    {"name": "Nasarawa", "capital": "Lafia", "lat": 8.5060, "lon": 8.5227, "abbr": "NA"},
    {"name": "Niger", "capital": "Minna", "lat": 9.6119, "lon": 6.5478, "abbr": "NI"},
    {"name": "Ogun", "capital": "Abeokuta", "lat": 7.1470, "lon": 3.3619, "abbr": "OG"},
    {"name": "Ondo", "capital": "Akure", "lat": 7.2571, "lon": 5.2058, "abbr": "ON"},
    {"name": "Osun", "capital": "Osogbo", "lat": 7.7710, "lon": 4.5576, "abbr": "OS"},
    {"name": "Oyo", "capital": "Ibadan", "lat": 7.3775, "lon": 3.9470, "abbr": "OY"},
    {"name": "Plateau", "capital": "Jos", "lat": 9.8965, "lon": 8.8583, "abbr": "PL"},
    {"name": "Rivers", "capital": "Port Harcourt", "lat": 4.8156, "lon": 7.0498, "abbr": "RI"},
    {"name": "Sokoto", "capital": "Sokoto", "lat": 13.0667, "lon": 5.2333, "abbr": "SO"},
    {"name": "Taraba", "capital": "Jalingo", "lat": 8.8937, "lon": 11.3596, "abbr": "TA"},
    {"name": "Yobe", "capital": "Damaturu", "lat": 11.7481, "lon": 11.9669, "abbr": "YO"},
    {"name": "Zamfara", "capital": "Gusau", "lat": 12.1704, "lon": 6.6641, "abbr": "ZA"},
    {"name": "Federal Capital Territory", "capital": "Abuja", "lat": 9.0579, "lon": 7.4951, "abbr": "FCT"},
]


def load_states(apps, schema_editor):
    State = apps.get_model("locations", "State")
    for s in NIGERIAN_STATES:
        State.objects.create(
            name=s["name"],
            capital=s["capital"],
            latitude=s["lat"],
            longitude=s["lon"],
            abbreviation=s.get("abbr"),
        )


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        # No dependencies needed for a fresh app
    ]

    operations = [
        migrations.CreateModel(
            name="State",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True)),
                ("capital", models.CharField(blank=True, max_length=100, null=True)),
                ("latitude", models.DecimalField(decimal_places=6, max_digits=9)),
                ("longitude", models.DecimalField(decimal_places=6, max_digits=9)),
                ("abbreviation", models.CharField(blank=True, max_length=5, null=True)),
            ],
            options={
                "verbose_name_plural": "States",
                "ordering": ["name"],
            },
        ),
        migrations.RunPython(load_states, reverse_code=migrations.RunPython.noop),
    ]