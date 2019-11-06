import pandas as pd
from pprint import pprint
import os, sys
from glob import glob

import pandas as pd

from pprint import pprint
import docxpy



proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portale.settings")
sys.path.append(proj_path)
# This is so my local_settings.py gets loaded.
os.chdir(proj_path)
# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()



ruoli = ['AD','AZ','AR','PH','ST','UP','AP','CW']
societa=['AP','AZ','ST','UP']
persone=['AD','AR','CW','PH']

RUOLI = {'AZ':'Azienda', 'AR':'Artista', 'PH':'Fotografo', 'ST':'Stampatore',
         'AD':'Art Director', 'UP':'Ufficio Pubblicitario', 'AP':'Agenzia Pubblicitaria', 'CW':'Copywriter'}
TIPI = { 'Manifesto':'MF', 'Annuncio':'AN', 'Opuscolo' :'OP', 'Pieghevole':'PG','Editoria':'ED'}



def soggetto_reader(idx,df,ruolo):

    sogg_c1 = str(df.loc[idx, 'Cognome/nome societa']).split('#')
    sogg_c2 = str(df.loc[idx, 'Nome/citta']).split('#')
    sogg_c3 = str(df.loc[idx, 'citta']).split('#')

    l_c1 = len(sogg_c1)
    l_c2 = len(sogg_c2)
    l_c3 = len(sogg_c3)

    l_max = max(l_c1,l_c2,l_c3)

    if l_max>1:
        if len(sogg_c1)<l_max:
            n = l_max - len(sogg_c1)
            for k in range(n):
                sogg_c1.append(None)

        if len(sogg_c2)<l_max:
            n = l_max - len(sogg_c2)
            for k in range(n):
                sogg_c2.append(None)

        if len(sogg_c3)<l_max:
            n = l_max-len(sogg_c3)
            for k in range(n):
                sogg_c3.append(None)

    soggetti = []

    for i in range(l_max):

        if sogg_c1[i] == 'nan' or sogg_c1[i] is None:
            sogg_c1[i] = ""
        else:
            sogg_c1[i] = sogg_c1[i].strip()

        if sogg_c2[i] == 'nan' or sogg_c2[i] is None:
            sogg_c2[i] = ""
        else:
            sogg_c2[i] = sogg_c2[i].strip()

        if sogg_c3[i] == 'nan' or sogg_c3[i] is None:
            sogg_c3[i] = ""
        else:
            sogg_c3[i] = sogg_c3[i].strip()


        if (sogg_c1[i] == "") and (sogg_c2[i] == "") and (sogg_c3[i] == ""):
            continue

        if ruolo in persone:
            rec = {'nome': sogg_c2[i], 'cognome': sogg_c1[i],
                   'citta': sogg_c3[i],'ruolo_sigla':ruolo, 'ruolo_nome':RUOLI[ruolo]}
        else:
            rec = {'nome': sogg_c1[i], 'cognome':'','citta': sogg_c2[i],
                   'ruolo_sigla':ruolo, 'ruolo_nome':RUOLI[ruolo]}


        soggetti.append(rec)

    return soggetti

def reader(src,img_base_src):
    sog_df = pd.read_excel(src, sheet_name='SOGGETTI', index_col=[2])
    rel_df = pd.read_excel(src, sheet_name='RELAZIONI')
    relazioni = []

    for r in rel_df.index:
        opera = {'annuario': rel_df.loc[r, 'OP_anno'],
                 'img': rel_df.loc[r, 'OP_img'],
                 'src': os.path.join(img_base_src,rel_df.loc[r, 'OP_IMG_PATH']),
                 'tipo_nome': rel_df.loc[r, 'OP_tipo'].capitalize(),
                 'tipo_sigla': TIPI[rel_df.loc[r, 'OP_tipo'].capitalize()],
                 'soggetti': []
                 }

        for ruolo in ruoli:
            ruolo_id = rel_df.loc[r, ruolo]
            soggetti = soggetto_reader(ruolo_id, sog_df, ruolo)

            opera['soggetti'] += soggetti

        relazioni.append(opera)

    return  relazioni

def upload_soggetto(sog_dict):

    nome = sog_dict['nome']
    cognome = sog_dict['cognome']
    citta = sog_dict['citta']
    try:
        nome = nome.strip()
    except:
        nome = nome

    try:
        cognome = cognome.strip()
    except:
        cognome = cognome
    try:
        citta = citta.strip()
    except:
        citta = citta


    nome_completo = '{} {}'.format(cognome,nome,).strip()

    try:
        soggetto_obj = Soggetto.objects.get(nome_completo=nome_completo)
    except:

        if cognome is None:
            soggetto_obj = Soggetto(nome=nome,
                                    nome_completo=nome_completo)
            soggetto_obj.save()
        else:
            soggetto_obj = Soggetto(nome=nome, cognome=cognome,
                                    nome_completo=nome_completo)
            soggetto_obj.save()

        if not citta is None:
            soggetto_obj.citta = citta.strip()
            soggetto_obj.save()





    ruolo_nome = sog_dict['ruolo_nome']
    ruolo_sigla = sog_dict['ruolo_sigla']
    ruolo_obj,_ = Ruolo.objects.get_or_create(nome=ruolo_nome,sigla=ruolo_sigla)



    return soggetto_obj,ruolo_obj



def upload(rel_dict):

    annuario = rel_dict['annuario']
    annuario_obj,_ = Annuario.objects.get_or_create(nome=annuario)

    tipo_nome = rel_dict['tipo_nome']
    tipo_sigla = rel_dict['tipo_sigla']
    tipo_obj, _ = TipoOpera.objects.get_or_create(nome=tipo_nome,sigla=tipo_sigla)

    img = rel_dict['img']
    src = rel_dict['src']

    img_nome_file = "{}_{}.jpg".format(annuario, img)
    img_nome_univoco = "{}_{}".format(annuario, img)

    try:
        opera_obj = Opera.objects.get(img_nome=img_nome_univoco)
    except:
        opera_obj = Opera(tipo=tipo_obj,
                          annuario=annuario_obj,
                          img_nome=img_nome_univoco)


        with open(src, 'rb') as img:
                opera_obj.img.save(img_nome_file, img, True)


    print(opera_obj.id,opera_obj,img, src)




    for sog_dict in rel_dict['soggetti']:
        soggetto_obj, ruolo_obj = upload_soggetto(sog_dict)


        relazione_obj, created = Relazione.objects.get_or_create(annuario=annuario_obj,
                                                           opera=opera_obj,
                                                           soggetto=soggetto_obj,
                                                           ruolo=ruolo_obj)
        print(relazione_obj,created)


def extract_text_intro(file):
    text = docxpy.process(file)
    parts = text.split('\n')

    giuria = ''
    impaginazione = ''
    intro_title = ''
    intro_text = ''
    intro_footer = ''

    for linea in parts:
        if 'Giuria' in linea: giuria = linea
        elif 'Titolo' in linea: intro_title=linea
        elif 'Copertina' in linea: impaginazione=linea
        elif 'Autore' in linea:intro_footer = linea
        elif len(linea)>1:intro_text=linea


    res = {'giuria' :giuria,
    'impaginazione':impaginazione,
    'intro_title':intro_title,
    'intro_text':intro_text,
    'intro_footer':intro_footer}

    return res


def upload_annuari(annuario_data):


    for annuario in os.listdir(annuario_data):
        if '.DS_Store' in annuario:continue
        ann_imgs = []
        annuario_folder = os.path.join(annuario_data,annuario)
        for file in os.listdir(annuario_folder):
            if file.startswith('.'): continue
            annuario_file = os.path.join(annuario_folder, file)
            if '.docx' in file:
                text = extract_text_intro(annuario_file)
            elif 'cover' in file:
                cover_src = os.path.join(annuario_folder, file)
                cover_img_file = 'cover_{}'.format(annuario)
            else:
                nome = 'img_ann_{}_{}.jpg'.format(annuario,file.split('.')[0])
                src = os.path.join(annuario_folder,file)
                ann_imgs.append({'nome':nome,'src':src})
        print(annuario)

        ann_obj,_ = Annuario.objects.get_or_create(nome=annuario)

        ann_obj.giuria = text['giuria']
        ann_obj.impaginazione = text['impaginazione']
        ann_obj.intro_title = text['intro_title']
        ann_obj.intro_text = text['intro_text']
        ann_obj.intro_footer = text['intro_footer']
        with open(cover_src, 'rb') as img:
            ann_obj.cover_img.save(cover_img_file, img, True)

        annuario_id = ann_obj.id


        for im in ann_imgs:
            im_obj,_ = ImmaginiAnnuario.objects.get_or_create(nome=im['nome'],annuario_id=annuario_id)

            with open(im['src'], 'rb') as img:
                ann_obj = im_obj.img.save(im['nome'], img, True)













        continue




        print(annuario)
        if '.DS' in annuario: continue

        ann_obj = Annuario.objects.get(nome=annuario)
        annuario_folder = os.path.join(annuario_data,annuario)


        for file in os.listdir(annuario_folder):
            if 'cover' in file:
                src = os.path.join(annuario_folder,file)
                img_file = 'cover_{}'.format(annuario)
                with open(src, 'rb') as img:
                    ann_obj.cover_img.save(img_file, img, True)





if __name__ == '__main__':

    from pubblicita.models import *
    import os

    BASE_PATH = r'/Users/cristian/Desktop'


    src=os.path.join('MATERIALI SITO-1/relazioni.xlsx')
    imgs_base_src = os.path.join('MATERIALI SITO-1/OPERE')
    annuario_data = os.path.join('MATERIALI SITO-1/ANNUARI')

    data = reader(src, imgs_base_src)
    for opera in data:
        upload(opera)

    upload_annuari(annuario_data)