from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from .models import *
from django.db.models import Count
from django.contrib.postgres.aggregates import ArrayAgg
from pprint import pprint
from django.template.loader import render_to_string
import json


from django.views.decorators.csrf import csrf_exempt

# STUPIDE
def home(request):

    template = 'pubblicita/home.html'
    context = {}
    return render(request,template,context)

def come_funziona(request):

    template = 'pubblicita/come_funziona.html'
    context = {}
    return render(request,template,context)

def contatti(request):
    template = 'pubblicita/contatti.html'
    context = {}
    return render(request, template, context)

# FACILI
def annuari(request):

    template = 'pubblicita/annuario_list.html'
    annuari = Annuario.objects.all()
    context = {'annuari':annuari.order_by('nome')}
    return render(request, template, context)

def annuario_detail(request,annuario_id):

    template = 'pubblicita/annuario_detail.html'
    annuario = Annuario.objects.get(id=annuario_id)

    annuari_id_list =list(Annuario.objects.all().order_by('nome').values('id','nome'))

    this_id = annuario.id

    next_id = prev_id = None

    l = len(annuari_id_list)
    for index, obj in enumerate(annuari_id_list):
        print(index,obj)
        if obj['id'] == this_id:

            if index > 0:
                prev_id = annuari_id_list[index - 1]
                try:
                    prev_id = prev_id['id']
                except:
                    prev_id = None
            if index < (l - 1):
                next_id = annuari_id_list[index + 1]
                try:
                    next_id = next_id['id']
                except:
                    next_id = None

    context = {'annuario': annuario,"prev":prev_id, "next":next_id}
    print(context)

    return render(request, template, context)


# COMPLESSE
def soggetti(request):


    template = 'pubblicita/soggetto_list.html'
    ruoli = Ruolo.objects.all().values('id', 'nome')
    annuari = Annuario.objects.all().values('id', 'nome').order_by('nome')
    ordini = [{'id': 'A', 'nome': 'Alfabetico'},
              {'id': 'N+', 'nome': 'Decrescente'},
              {'id': 'N-', 'nome': 'Crescente'}]



    opts = {'ruolo': 0, 'annuario': 0, 'ordine': 'A'}



    soggetti = Soggetto.objects.all()\
        .annotate(my_ruoli=ArrayAgg('relazione__ruolo__sigla', distinct = True))\
        .annotate(opere_count=Count('relazione__opera__id',distinct=True)).order_by('nome_completo')



    context = {'soggetti': soggetti, 'ruoli':ruoli, 'annuari':annuari, 'ordini':ordini,'opts':opts}

    return render(request, template, context)

@csrf_exempt
def soggetti_ajax(request): # TEST

    ruolo = int(request.POST['ruolo_id'])
    annuario = int(request.POST['annuario_id'])
    ordine = request.POST['ordinamento_id']
    nome = ''
    print(request.POST)
    if not nome == '':
        soggetti = Soggetto.objects.filter(nome_completo__icontains=nome)

    else:
        if ruolo == annuario == 0:
            soggetti = Soggetto.objects.all()

        elif ruolo == 0 and (annuario > 0):
            soggetti = Soggetto.objects.filter(relazione__annuario_id=annuario).distinct()
        elif (annuario == 0) and (ruolo > 0):
            soggetti = Soggetto.objects.filter(relazione__ruolo_id=ruolo).distinct()
        else:
            soggetti = Soggetto.objects.filter(relazione__ruolo_id=ruolo).filter(relazione__annuario_id=annuario).distinct()


    soggetti = soggetti.annotate(my_ruoli=ArrayAgg('relazione__ruolo__sigla', distinct = True))\
                .annotate(opere_count=Count('relazione__opera__id',distinct=True))


    if ordine == 'A':
        soggetti = soggetti.order_by('nome_completo')
    elif ordine == 'N+':
        soggetti = soggetti.order_by('-opere_count')
    elif ordine == 'N-':
        soggetti = soggetti.order_by('opere_count')

    soggetti = soggetti.values('id','nome','cognome','nome_completo','my_ruoli','opere_count')


    return JsonResponse(json.dumps(list(soggetti)), safe=False)

def dettaglio_soggetto(request,soggetto_id):


    template = 'pubblicita/soggetto_detail.html'

    soggetto = Soggetto.objects.get(id=soggetto_id)


    ruoli = Relazione.objects.filter(soggetto__id=soggetto.id).values('ruolo__sigla').annotate(n_ruoli=Count('ruolo'))
    tipi = Relazione.objects.filter(soggetto__id=soggetto.id).values('opera__tipo__nome').annotate(n_tipi=Count('opera__tipo'))



    opere_img =  Opera.objects.filter(id__in=Relazione.objects.filter(soggetto__id=soggetto.id).order_by('relazione__annuario__nome').values('opera__id'))
    opere = Opera.objects.filter(id__in=Relazione.objects.filter(soggetto__id=soggetto.id)
                                 .values('opera__id')).order_by('annuario__nome')

    az_soggetti = Relazione.objects.filter(opera__id__in=opere)\
        .exclude(soggetto__id=soggetto.id)\
        .filter(ruolo__sigla='AZ')\
        .values('soggetto__id','soggetto__nome','soggetto__cognome')\
        .annotate(Count('soggetto__id')).order_by('-soggetto__id__count')[:5]


    ar_soggetti = Relazione.objects.filter(opera__id__in=opere)\
                        .exclude(soggetto__id=soggetto.id)\
                        .filter(ruolo__sigla='AR')\
                        .values('soggetto__id','soggetto__nome','soggetto__cognome')\
                        .annotate(Count('soggetto__id')).order_by('-soggetto__id__count')[:5]


    ph_soggetti = Relazione.objects.filter(opera__id__in=opere)\
                        .exclude(soggetto__id=soggetto.id)\
                        .filter(ruolo__sigla='PH')\
                        .values('soggetto__id','soggetto__nome','soggetto__cognome')\
                        .annotate(Count('soggetto__id')).order_by('-soggetto__id__count')[:5]

    ad_soggetti = Relazione.objects.filter(opera__id__in=opere) \
                      .exclude(soggetto__id=soggetto.id) \
                      .filter(ruolo__sigla='AD') \
                      .values('soggetto__id', 'soggetto__nome','soggetto__cognome') \
                      .annotate(Count('soggetto__id')).order_by('-soggetto__id__count')[:5]

    ap_soggetti = Relazione.objects.filter(opera__id__in=opere) \
                      .exclude(soggetto__id=soggetto.id) \
                      .filter(ruolo__sigla='AP') \
                      .values('soggetto__id', 'soggetto__nome','soggetto__cognome') \
                      .annotate(Count('soggetto__id')).order_by('-soggetto__id__count')[:5]


    context = {'soggetto': soggetto,
               'AZ': json.dumps(list(az_soggetti)),
               'AR': json.dumps(list(ar_soggetti)),
               'PH': json.dumps(list(ph_soggetti)),
               'AD': json.dumps(list(ad_soggetti)),
               'AP': json.dumps(list(ap_soggetti)),
               'ruoli': ruoli,
               'tipi': json.dumps(list(tipi)),
               'opere': opere_img
               }
    pprint(opere_img)
    return render(request, template, context)


def opera_detail(request,opera_id):
    if request.is_ajax():
        mimetype = 'application/json'
        opera = Opera.objects.get(id=opera_id)
        html = render_to_string('pubblicita/opera_detail.html', {'opera': opera})
        return HttpResponse(json.dumps({'html': html}), mimetype)

@csrf_exempt
def opere_soggetto_ajax(request):

    if request.is_ajax():
        if request.method == 'POST':
            mimetype = 'application/json'
            soggetto_id= request.POST['soggetto_id']
            annuario_id= request.POST['annuario_id']


            soggetto = Soggetto.objects.get(id=soggetto_id)
            relazioni = Relazione.objects.filter(soggetto__id=soggetto_id)

            if annuario_id != '0':
                relazioni = relazioni.filter(annuario__id=annuario_id)


            opere = Opera.objects.filter(id__in=relazioni.values('opera__id')).distinct().order_by('annuario__nome')


            html = render_to_string('pubblicita/opera_list.html', {'opere':opere,'soggetto':soggetto})

            res = {'html': html}


            return HttpResponse(json.dumps(res), mimetype)


def relazioni(request):

    template = 'pubblicita/relazioni.html'

    ruoli = Ruolo.objects.all().values()
    annuari = Annuario.objects.all().values().order_by('nome')
    soggetti = Soggetto.objects.all().values('nome_completo','id')

    s2 = []
    for s in list(soggetti):
        for k in s.keys():
            if s[k]=='':
               s[k] = ""
        s2.append(s)


    context = {'soggetti':json.dumps(list(s2)),'ruoli':ruoli,'annuari':annuari}

    return render(request,template,context,)




@csrf_exempt
def rel_sog2_ajax(request):

    annuario = int(request.POST['annuario_id'])
    ruolo_1 = int(request.POST['id_r1'])

    if ruolo_1 != 0 and annuario != 0:

        soggetti = Soggetto.objects.filter(relazione__ruolo__id=ruolo_1).filter(relazione__annuario__id=annuario)\
            .values('nome_completo','id').distinct()

    elif ruolo_1 != 0 and annuario == 0:
        soggetti = Soggetto.objects.filter(relazione__ruolo__id=ruolo_1)\
            .values('nome_completo', 'id').distinct()
    elif ruolo_1 != 0 and annuario == 0:
        soggetti = Soggetto.objects.filter(relazione__annuario__id=annuario)\
            .values('nome_completo', 'id').distinct()
    else:
        soggetti = Soggetto.objects.all().values('nome_completo', 'id').distinct()


    return JsonResponse(json.dumps(list(soggetti)),safe=False)

@csrf_exempt
def rel_sog1_ajax(request):

    annuario = int(request.POST['annuario_id'])
    ruolo_1 = int(request.POST['id_r1'])
    ruolo_2 = int(request.POST['id_r2'])


    if annuario != 0:
        opera = Opera.objects.filter(annuario__id=annuario)
    else:
        opera = Opera.objects.all()

    if ruolo_1 != 0:
        opera1 = opera.filter(relazione__ruolo__id=ruolo_1)
    else:
        opera1 = opera

    if ruolo_2 != 0:
        opera2 = opera.filter(relazione__ruolo__id=ruolo_2)
    else:
        opera2 = opera

    opera = opera1.intersection(opera2).values('id').distinct()

    if ruolo_1!=0:
        soggetto1 = Soggetto.objects.filter(relazione__opera__id__in=opera).filter(relazione__ruolo__id=ruolo_1).values().distinct('id')
    else:
        soggetto1 = Soggetto.objects.filter(relazione__opera__id__in=opera).values().distinct('id')

    if ruolo_2 != 0:
        soggetto2 = Soggetto.objects.filter(relazione__opera__id__in=opera).filter(
            relazione__ruolo__id=ruolo_2).values().distinct('id')
    else:
        soggetto2 = Soggetto.objects.filter(relazione__opera__id__in=opera).values().distinct('id')


    result = {'s1':list(soggetto1),
              's2':list(soggetto2)}

    return JsonResponse(json.dumps(result),safe=False)

@csrf_exempt
def sog1_r2_opere_ajax(request):

    s1 = int(request.POST['s1_id'])
    r2_id = int(request.POST['id_r2'])
    annuario = int(request.POST['annuario_id'])

    opera=Opera.objects.filter(relazione__soggetto__id=s1)
    if annuario!=0:
        opera = opera.filter(annuario__id=annuario)

    soggetto = Soggetto.objects.filter(relazione__opera__id__in=opera.values('id'))
    if r2_id !=0:
        soggetto = soggetto.filter(relazione__ruolo__id=r2_id)

    s2 = soggetto.exclude(id=s1).distinct()\
        .annotate(my_opere=ArrayAgg('relazione__opera__id',distinct=True)).values("id","nome_completo")#,"my_opere")#.values('id','nome_completo','relazione__opera__id')


    return JsonResponse(json.dumps(list(s2)), safe=False)

@csrf_exempt
def opere_s1_s2_ajax(request):

    mimetype = 'application/json'

    s1 = int(request.POST['s1_id'])
    s2 = int(request.POST['s2_id'])
    annuario = int(request.POST['annuario_id'])

    opere1 = Opera.objects.filter(relazione__soggetto__id=s1)

    opere2 = Opera.objects.filter(relazione__soggetto__id=s2)

    opere = opere1 & opere2

    if annuario!=0:
        opere = opere.filter(relazione__annuario__id=annuario)

    opere = opere.distinct()

    html = render_to_string('pubblicita/opera_list.html', {'opere': opere})

    res = {'html': html}

    return HttpResponse(json.dumps(res), mimetype)

