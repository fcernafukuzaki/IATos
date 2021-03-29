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
                type: 'audio/wav'
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

$(document).ready(function() {
    $('#enviar').click(enviar_tos);
});

function enviar_tos(e) {
    e.preventDefault();
    var base64data = $('#tos_base64').val();
    var dict = {
        'tos_base64': base64data,
        'length': base64data.length
    };
    // comentar/eliminar las líneas de abajo al conectarnos a un endpoint real
    dict = {
        'json': JSON.stringify(dict)
    };
    console.log("Envío:", dict);
    $.ajax({
        url: '/echo',
        type: 'POST',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        data: dict
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