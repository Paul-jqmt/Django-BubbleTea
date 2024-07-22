from django.db import models

# Create your models here.
class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    name = models.TextField()
    surname = models.TextField()
    username = models.TextField()
    password = models.TextField()
    admin = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer'
    def __str__(self):
        return self.username



class DrinkBase(models.Model):
    base_id = models.AutoField(primary_key=True)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'drink_base'
    def __str__(self):
        return self.description

class DrinkFlavour(models.Model):
    flavour_id = models.AutoField(primary_key=True)
    description = models.TextField()
    base = models.ForeignKey(DrinkBase, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'drink_flavour'
    def __str__(self):
        return self.description


class DrinkPopping(models.Model):
    popping_id = models.AutoField(primary_key=True)
    description = models.TextField()
    base = models.ForeignKey(DrinkBase, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'drink_popping'
    def __str__(self):
        return self.description


class Product(models.Model):
    purchase_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, models.DO_NOTHING)
    base = models.ForeignKey(DrinkBase, models.DO_NOTHING)
    flavour = models.ForeignKey(DrinkFlavour, models.DO_NOTHING)
    popping = models.ForeignKey(DrinkPopping, models.DO_NOTHING)
    sugar = models.IntegerField()
    size = models.IntegerField()
    price = models.IntegerField()
    purchase_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'product'
    def __str__(self):
        return self.flavour.description + " " + self.base.description + " " + self.popping.description + " " + str(self.price)+ " €"
