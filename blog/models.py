from django.db import models

class nodes(models.Model):
    sample_time = models.DateTimeField()
    location = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)


class temperature(models.Model):
    alarmTemp = models.BooleanField()
    temp = models.DecimalField(max_digits=4, decimal_places=2)
    nodes = models.ForeignKey(nodes, on_delete=models.CASCADE)
    def __str__(self):
        return "Node number: " + str(self.nodes.nodenumber) + " temp: " + str(self.temp*100)

class humidity(models.Model):
    alarmHum = models.BooleanField()
    humidity = models.DecimalField(max_digits=4, decimal_places=2)
    nodes = models.ForeignKey(nodes, on_delete=models.CASCADE)

class AirQuality(models.Model):
    alarm_air_quality = models.BooleanField()
    air_quality_ppm = models.DecimalField(max_digits=6, decimal_places=2)
    nodes = models.ForeignKey(nodes, on_delete=models.CASCADE)
