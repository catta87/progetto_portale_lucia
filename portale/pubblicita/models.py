from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class ImmaginiAnnuario(models.Model):

    nome = models.CharField(max_length=100)
    img = models.ImageField()
    annuario = models.ForeignKey('Annuario',on_delete=models.CASCADE)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return '{}'.format(self.tipo,self.annuario.nome)

class TipoOpera(models.Model):

    nome = models.CharField(max_length=20,unique=True)
    sigla = models.CharField(max_length=3,blank=True,null=True)

    def __str__(self):
        return '{}'.format(self.nome)

class Ruolo(models.Model):

    nome = models.CharField(max_length=40,unique=True)
    sigla = models.CharField(max_length=3,blank=True,null=True)

    def __str__(self):
        return '{}'.format(self.nome)


def annuario_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/annuario_<nome>/<filename>
    return 'annuario_{0}/{1}'.format(instance.nome, filename)

def opera_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/annuario_<nome>/<filename>
    return 'opere_{0}/{1}'.format(instance.annuario.nome, filename)

class Annuario(models.Model):

    nome = models.CharField(max_length=10,unique=True)

    cover_img = models.ImageField(upload_to=annuario_directory_path,null=True,blank=True)

    giuria = models.TextField(null=True,blank=True)
    impaginazione = models.TextField(max_length=200,null=True,blank=True)
    intro_title = models.TextField(null=True,blank=True)
    intro_text = models.TextField(null=True,blank=True)
    intro_footer = models.TextField(null=True,blank=True)

    def __str__(self):
        return '{}'.format(self.nome)

class Soggetto(models.Model):

    nome_completo = models.CharField(max_length=100,unique=True)
    nome = models.CharField(max_length=100,blank=True,null=True)
    cognome = models.CharField(max_length=100,blank=True,null=True)
    citta = models.CharField(max_length=80,null=True,blank=True)

    def __str__(self):
        return '{}'.format(self.nome,self.cognome,self.citta)

class Opera(models.Model):
    img_nome = models.CharField(max_length=20,unique=True)
    img = models.ImageField(upload_to=opera_directory_path)
    thumbnail = ImageSpecField(source='img',processors=[ResizeToFill(100, 50)],
                               format='JPEG',options={'quality': 60})

    tipo = models.ForeignKey(TipoOpera,on_delete=models.CASCADE)
    annuario = models.ForeignKey(Annuario,on_delete=models.CASCADE)

    def __str__(self):
        return '{}-{}'.format(self.annuario.nome,self.id)

class Relazione(models.Model):

    annuario = models.ForeignKey(Annuario, on_delete=models.CASCADE)
    soggetto = models.ForeignKey(Soggetto,on_delete=models.CASCADE)
    opera = models.ForeignKey(Opera,on_delete=models.CASCADE)
    ruolo = models.ForeignKey(Ruolo,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return '{}-{}'.format(self.annuario.nome,self.id)

