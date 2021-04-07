 function comenzar() {
     $('#comenzarGrabacion').hide();
     $('#detenerGrabacion').show();
     tos = [];
     mediaRecorder.start();
 }

 function detener() {
     $('#comenzarGrabacion').show();
     $('#detenerGrabacion').hide();
     mediaRecorder.stop();
 }
 navigator.mediaDevices.getUserMedia({
     audio: true
 }).then(stream => {
     mediaRecorder = new MediaRecorder(stream);
     mediaRecorder.ondataavailable = e => {
         tos.push(e.data);
         if (mediaRecorder.state == "inactive") {
             let blob = new Blob(tos, {
                 type: 'audio/webm'
             });
             grabacion.src = URL.createObjectURL(blob);
             grabacion.controls = true;
             var linkDescarga = $('#descargar')[0];
             linkDescarga.href = grabacion.src;
             var fechaHora = new Date().toLocaleString().replaceAll('/', '_').replaceAll(':', '_').replaceAll(' ', '_');
             linkDescarga.download = 'Tos_' + fechaHora + '.wav';
             linkDescarga.innerHTML = 'Descargar';
             var reader = new FileReader();
             reader.readAsDataURL(blob);
             reader.onloadend = function() {
                 var base64data = reader.result;
                 console.log("Grabación base64:", base64data);
                 $('#tos_base64').val(base64data);
                 $('#controles-grabacion').hide();
                 $('#form').show();
             }
         }
     }
 }).catch(e => console.log("Error al obtener permisos del micrófono:", e));

 function borrar() {
     $('#form').hide();
     $('#form')[0].reset();
     $("#resultado").hide();
     $('#controles-grabacion').show();
 }

 function enviar_tos() {
     var base64data = $('#tos_base64').val();
     var dict = {
         'tos_base64': base64data,
         'length': base64data.length,
         'opcionSi1': document.getElementById('opcionSi1').checked,
         'opcionSi2': document.getElementById('opcionSi2').checked,
         'opcionSi3': document.getElementById('opcionSi3').checked,
         'opcionSi4': document.getElementById('opcionSi4').checked,
         'opcionSi5': document.getElementById('opcionSi5').checked,
         'opcionSi6': document.getElementById('opcionSi6').checked,
         'opcionSi7': document.getElementById('opcionSi7').checked
     };
     // comentar/eliminar las líneas de abajo al conectarnos a un endpoint real
     /*dict = {
         'json': JSON.stringify(dict)
     };*/
     console.log("Envío:", dict);
     $.ajax({
         url: '/enviar_tos/',
         type: 'POST',
         contentType: 'application/json; charset=utf-8',
         dataType: 'json',
         data: JSON.stringify(dict)
     }).done(function(resp) {
         console.log("Respuesta:", resp);
         mostrar_resultado(resp);
     }).fail(function(e) {
         console.log("Error:", e);
     });
     return false;
 }

 function mostrar_resultado(resp) {
     $("#resultado pre").html(JSON.stringify(resp, null, 4));
     $("#resultado").show();
 }
 //Botón Resultado valida radio buttons
 const btn = document.querySelector('#btn');
 btn.onclick = function() {
     if (document.getElementById('opcionSi1').checked) {
         alert("\nUsted presenta síntomas compatibles con COVID-19. \n\nPara confirmar tu diagnóstico por favor acercarte a la Unidad DetectAR más cercana o llamá al 147 para solicitar ayuda de nuestro equipo");
     } else if (document.getElementById('opcionSi2').checked) {
         alert("\nUsted presenta síntomas compatibles con COVID-19. \n\nPara confirmar tu diagnóstico por favor acercarte a la Unidad DetectAR más cercana o llamá al 147 para solicitar ayuda de nuestro equipo");
     } else if (document.getElementById('opcionSi3').checked) {
         alert("\nUsted presenta síntomas compatibles con COVID-19. \n\nPara confirmar tu diagnóstico por favor acercarte a la Unidad DetectAR más cercana o llamá al 147 para solicitar ayuda de nuestro equipo");
     } else if (document.getElementById('opcionSi4').checked) {
         alert("\nUsted presenta síntomas compatibles con COVID-19. \n\nPara confirmar tu diagnóstico por favor acercarte a la Unidad DetectAR más cercana o llamá al 147 para solicitar ayuda de nuestro equipo");
     } else if (document.getElementById('opcionSi5').checked) {
         alert("\nUsted presenta síntomas compatibles con COVID-19. \n\nPara confirmar tu diagnóstico por favor acercarte a la Unidad DetectAR más cercana o llamá al 147 para solicitar ayuda de nuestro equipo");
     } else if (document.getElementById('opcionSi6').checked) {
         alert("\nUsted presenta síntomas compatibles con COVID-19. \n\nPara confirmar tu diagnóstico por favor acercarte a la Unidad DetectAR más cercana o llamá al 147 para solicitar ayuda de nuestro equipo");
     } else if (document.getElementById('opcionSi7').checked) {
         alert("\nUsted presenta síntomas compatibles con COVID-19. \n\nPara confirmar tu diagnóstico por favor acercarte a la Unidad DetectAR más cercana o llamá al 147 para solicitar ayuda de nuestro equipo");
     } else if (document.getElementById('opcionNo').checked) {
         alert("\nUsted no presenta síntomas compatibles con COVID-19\n\nRecordá usar barbijo cada vez que salís de tu casa y seguí las medidas de prevención")
     } else {
         alert("Por favor responda las preguntas")
     }
 }