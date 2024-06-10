from django.db import models
from django.urls import reverse
from import_export import resources

# Create your models here.


class trees_Database(models.Model):
    id = models.CharField(null=True, max_length=5)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    altitude_ft = models.FloatField(null=True)
    tree_id = models.CharField(
        primary_key=True, auto_created=False, max_length=5, null=False)
    zone = models.CharField(max_length=2, null=True)
    group_name = models.CharField(max_length=50, null=True)
    leaf_fall = models.CharField(max_length=50, null=True)
    common_name = models.CharField(max_length=255, null=True)
    genus = models.CharField(max_length=50, null=True)
    species_name = models.CharField(max_length=255, null=True)
    family_name = models.CharField(max_length=255, null=True)
    cbh = models.FloatField(null=True)
    dbh = models.FloatField(null=True)
    tree_height_ft = models.FloatField(null=True)
    canopy_radius_ft = models.FloatField(null=True)

    class Meta:
        db_table = 'trees_database'

    def __str__(self):
        return f"Tree: {self.tree_id}, {self.species_name}"

    def get_absolute_url(self):
        return reverse('home')


class TreeResource(resources.ModelResource):
    class Meta:
        model = trees_Database
        fields = ('id', 'latitude', 'longitude', 'altitude_ft' 'tree_id', 'zone', 'group_name', 'leaf_fall', 'common_name',
                  'genus', 'species_name', 'family_name', 'cbh', 'dbh', 'tree_height_ft', 'canopy_radius_ft')
        skip_unchanged = True  # skip unchanged rows
        use_bulk = True  # use bulk insert


class Comment(models.Model):
    tree_id = models.ForeignKey(
        trees_Database, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    moderated = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f"Comment: {self.tree_id}, Status - {self.moderated} "
