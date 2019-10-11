from django.urls import path
from .views import *


urlpatterns = [


        path('', home,name='home'),
        path('info', come_funziona,name='come-funziona'),
        path('contatti', contatti, name='contatti'),

        path('annuari', annuari, name='annuari-list'),
        path('annuario/<int:annuario_id>', annuario_detail, name='annuario-detail'),

        path('soggetti', soggetti, name='soggetti-list'),
        path('soggetti_ajax', soggetti_ajax, name='soggetti-list-ajax'),
        path('soggetto/<int:soggetto_id>', dettaglio_soggetto, name='soggetto-detail'),

        path('opere_soggetto/ajax',opere_soggetto_ajax,name='opere-soggetto-ajax'),

        path('relazioni',relazioni,name='relazioni'),
        path('rel_sog1_ajax',rel_sog1_ajax,name='rel-sog1-ajax'),
        path('rel_sog2_ajax',rel_sog2_ajax,name='rel-sog2-ajax'),
        path('sog1_r2_opere_ajax',sog1_r2_opere_ajax,name='sog1-r2-opere-ajax'),
        path('opere_s1_s2_ajax', opere_s1_s2_ajax, name='opere-s1-s2-ajax'),



    path('opera/<int:opera_id>', opera_detail, name='opera-detail'),
    path('get_img_json/<int:soggetto_id>/<int:annuario_id>', opere_soggetto_ajax, name='get-my-img'),


]