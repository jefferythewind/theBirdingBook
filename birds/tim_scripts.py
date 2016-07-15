import csv
from birds.models import SpeciesFile, Order, Family, Genus, Species, Subspecies

csv_file = str(SpeciesFile.objects.all()[0].species_list)

#COLUMNS
#0 - Order
#1 - Family Scientific
#2 - Family (English)
#3 - Genus
#4 - Species
#5 - SubSpecies


with open("birds/media/"+csv_file.split('/')[1], 'rU') as c:
    Order.objects.all().delete()
    Family.objects.all().delete()
    Genus.objects.all().delete()
    Species.objects.all().delete()
    Subspecies.objects.all().delete()
    reader = csv.reader(c, delimiter=',', quotechar='"')
    ini_rows = 4
    for row in reader:
        if ini_rows > 0:
            ini_rows -= 1
            continue
        if row[0]:
            new_order = Order(order=row[0])
            new_order.save()
        elif row[1]:
            new_fam = Family(order = new_order, family_scientific=row[1], family_english=row[2])
            new_fam.save()
        elif row[3]:
            new_genus = Genus(family = new_fam, genus=row[3])
            new_genus.save()
        elif row[4]:
            print row[4]
            new_species = Species(genus=new_genus, species=row[4], species_english=row[7])
            new_species.save()
        elif row[5]:
            print row[5]
            new_subspecies = Subspecies(species=new_species, subspecies=row[5])
            new_subspecies.save()
