from django.db import models
from django.contrib.auth.models import User


class Unit(models.Model):
    name = models.CharField(max_length=200)


class Condition(models.Model):
    name = models.CharField(max_length=200)
    Unit = models.ManyToManyField(Unit)


class Equipment(models.Model):
    name = models.CharField(max_length=200)
    Unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    Condition = models.ForeignKey(Condition, on_delete=models.CASCADE)


class Header(models.Model):
    name = models.CharField(max_length=100)
    hitung = models.BooleanField(default=True)
    Equipment = models.ForeignKey(Equipment,on_delete=models.CASCADE)



class MonitoringRow(models.Model):
    Equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    tanggal = models.DateField()
    waktu = models.TimeField(null=True)


class MonitoringData(models.Model):
    MonitoringRow = models.ForeignKey(MonitoringRow, on_delete=models.CASCADE)
    Header = models.ForeignKey(Header, on_delete=models.CASCADE)
    nilai = models.DecimalField(max_digits=10,decimal_places=2)

    @property
    def level(self):
        nlevel = 0
        standard = self.Header.standard_set.first()
        if self.nilai >= standard.batas_danger:
            nlevel = 4
        elif self.nilai >= standard.batas_warning:
            nlevel = 3
        elif self.nilai >= standard.batas_normal:
            nlevel = 2
        else :
            nlevel = 1
        return nlevel




class Standard(models.Model):
    Header = models.ForeignKey(Header, on_delete=models.CASCADE)
    batas_normal = models.DecimalField(max_digits=10,decimal_places=2)
    batas_warning = models.DecimalField(max_digits=10,decimal_places=2)
    batas_danger = models.DecimalField(max_digits=10,decimal_places=2)