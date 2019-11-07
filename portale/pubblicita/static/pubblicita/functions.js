
// Funzioni in dettaglio soggetto
function chart_maker_collaborazioni(data,selector){

    var soggetto = [];
    var numero = [];

    $.each(data, function( index, value ) {
        soggetto.push(value.soggetto__cognome + ' ' + value.soggetto__nome)
        numero.push(value.soggetto__id__count)
        });

    var options = {
                chart: {
                    height: 250,
                    type: 'bar',
                },
                plotOptions: {
                    bar: {
                        horizontal: true,
                    }
                },
                dataLabels: {
                    enabled: true
                },
                series: [{
                    data: numero
                }],
                xaxis: {
                    categories: soggetto,
                }
            }

    var chart = new ApexCharts(
                document.querySelector(selector),
                options
            );
    chart.render();
}
function chart_maker_tipi(data,selector){

    var tipi = [];
    var numero = [];

    $.each(data, function( index, value ) {
        console.log(value)
        tipi.push(value.opera__tipo__nome)
        numero.push(value.n_tipi)
        });

    var options = {
                chart: {
                    height: 250,
                    type: 'bar',
                },
                plotOptions: {
                    bar: {
                        horizontal: true,
                    }
                },
                dataLabels: {
                    enabled: true
                },
                series: [{
                    data: numero
                }],
                xaxis: {
                    categories: tipi
                }
            }

    var chart = new ApexCharts(
                document.querySelector(selector),
                options
            );
    chart.render();
}
function crea_grafici(AR,PH,AZ,AP,AD,TIPI){




        $( "#div_grafici" ).append( '<div id="chartTipi" class="col-md-8"></div>' );
        chart_maker_tipi(TIPI,'#chartTipi')
        $('#chartTipi').prepend('<h4>Tipologie</h4>')

        if (PH.length>0){
            $( "#div_grafici" ).append( '<div id="chartPH" class="col-md-8"></div>' );
            chart_maker_collaborazioni(PH,"#chartPH")
            $('#chartPH').prepend('<h4>Fotografi</h4>')
        }

        if (AR.length>0){

            $( "#div_grafici" ).append( '<div id="chartAR" class="col-md-8"></div>' );
            chart_maker_collaborazioni(AR,"#chartAR")
            $('#chartAR').prepend('<h4>Artisti</h4>')
        }
        if (AD.length>0){

            $( "#div_grafici" ).append( '<div id="chartAD" class="col-md-8"></div>' );
            chart_maker_collaborazioni(AD,"#chartAD")
            $('#chartAD').prepend('<h4>Art Director</h4>')
        }


        if (AZ.length>0){
            $( "#div_grafici" ).append( '<div id="chartAZ" class="col-md-8"></div>' );
            chart_maker_collaborazioni(AZ,"#chartAZ")
            $('#chartAZ').prepend('<h4>Committenti</h4>')
        }

        if (AP.length>0){
            $( "#div_grafici" ).append( '<div id="chartAP" class="col-md-8"></div>' );
            chart_maker_collaborazioni(AP,"#chartAP")
            $('#chartAP').prepend('<h4>Agenzia Pubblicitaria</h4>')
         }


}

// Funzioni in lista soggetti
function soggetto_list(data) {

   var data_list = JSON.parse(data);

   // svuoto div del sogg
   d3.select("#listaSoggetti")
      .selectAll("div")
      .remove()

   // creo nuovo elenco del sogg 1
   var div_s1 = d3.select("#listaSoggetti")
      .selectAll("div")
      .data(data_list)
      .enter()
      .append("div")
      .attr("class", "-content__item")
      .on("mouseover", function (d) {
         d3.select(this).style('background-color', "#e6f2ff")

      })
      .on("click", function (d) {
                 return get_images(d.id)
              })
      .on("mouseout", function (d) {
         d3.select(this).style('background-color', "#ffffff")
      })

   div_s1.append('a')
      .attr("href", function (d) { return url_soggetto_detail.replace('0', d.id) })
      .text(function (d) { return d.nome_completo })



   div_s1.append('span')
      .attr("class", "-badge")
      .text(function (d) { return d.my_ruoli })

   div_s1.append("span")
      .attr("class", "-badge")
      .text(function (d) { return d.opere_count })

}
function aggiorna_list(url,ruolo,annuario,ordinamento){
        ajax=$.ajax({
                    type: "POST",
                    url: url_soggetto_list_ajax,
                    data: {'ruolo_id':ruolo_id,'annuario_id':annuario_id,'ordinamento_id':ordinamento_id},
                    success: function( data ){
                          soggetto_list(data);
                        }
                    });
            }
function get_images(soggetto_id){

        if (ajax_imgs!=null){ ajax_imgs.abort();}
        ajax_imgs=$.ajax({
            type: "POST",
            url: url_opere_soggetto_ajax,
            data: {'soggetto_id':soggetto_id,'annuario_id':annuario_id,'ruolo_id':ruolo_id},
            success: function( data ){
                    $( '#immagini' ).html( data.html );
                }
            });
    }

//Funzioni in relazioni
var div_s1_curr
var div_s2_curr


function s1_list(data) {
   console.log('s1_list')
   var data_list = JSON.parse(data);

   // svuoto ul del sogg 1
   d3.select("#s1")
      .selectAll("div")
      .remove()

   // creo nuovo elenco del sogg 1
   var div_s1 = d3.select("#s1")
      .selectAll("div")
      .data(data_list.s1) // <---- s1

   div_s1.enter()
      .append("div")
      .attr('id', function (d, i) { return 's1-'+d.id })
      .text(function (d) { return d.nome_completo })
      .on("click", function (d, i) {

         if(typeof div_s1_curr == 'undefined') {div_s1_curr='s1-'+d.id}
         // resetta precedente div
         $('#'+div_s1_curr).css('background-color',"#ffffff")
         // aggiorn div_s1_curr colora div corrente
         div_s1_curr ='s1-'+d.id
          $('#'+div_s1_curr).css('background-color',"#e6f2ff")

         s1_selected = d.id
         aggiorna_lista_s2(d)

      })


}
function s2_list(data) {
   var data_list = JSON.parse(data);

   // svuoto ul del sogg 2
   d3.select("#s2")
      .selectAll("div")
      .remove()

   // creo nuovo elenco del sogg 2
   var div_s2 = d3.select("#s2")
      .selectAll("div")
      .data(data_list)


   div_s2.enter()
      .append("div")
      .attr('id', function (d, i) { return d.id })
      .text(function (d) { return d.nome_completo })
      .on("click", function (d, i) {


       if(typeof div_s2_curr == 'undefined') {div_s2_curr=d.id}
         // resetta precedente div
         $('#'+div_s2_curr).css('background-color',"#ffffff")
         // aggiorn div_s2_curr colora div corrente
         div_s2_curr = d.id
          $('#'+div_s2_curr).css('background-color',"#e6f2ff")

         aggiorna_lista_imm(d.id)

      })


}


function aggiorna_lista_s1(){

    console.log('aggiorna_list_s1')
    var post_data =  {'id_r1':id_r1,'id_r2':id_r2,'annuario_id':annuario_id};

    ajax_imgs=$.ajax({
            type: "POST",
            url: url_rel_sog1,
            data: post_data,
            success: function( data ){
                   s1_list(data);
                   s2_list(data);
                }
            });



}
function aggiorna_lista_s2(d){

    var s1_id = d.id;
    var post_data = {'s1_id':s1_id,'id_r2':id_r2,'annuario_id':annuario_id}

    ajax_imgs=$.ajax({
            type: "POST",
            url: url_s1_s2_op,
            data: post_data,
            success: function( data ){
                  s2_list(data);
                 },
            error: function(){console.log('Error')}
            });


    }
function aggiorna_lista_imm(s2){
    var post_data = {'s1_id':s1_selected,'s2_id':s2,'annuario_id':annuario_id}
    ajax_imgs=$.ajax({
            type: "POST",
            url: url_opere_s1_s2,
            data: post_data,
            success: function( data ){$( '#r' ).html( data.html ); }
            })
    }