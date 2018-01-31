// recarregar página no fechamento de qualquer modal
$('.modal').on('hidden.bs.modal', function () {
    location.reload();
});

// selecionar todas as checkboxes ao selecionar a checkbox geral
$('input[name=select-all]').on('change', function () {
    if (this.checked) {
        $("table input[name=id]").each(function () {
            $(this).prop('checked', true);
        });
    } else {
        $("table input[name=id]").each(function () {
            $(this).prop('checked', false);
        });
    }
});

// ativar o botão de exclusão múltipla
$('table input[type=checkbox]').on('change', function () {
    if (this.checked) {
        $('.delete-selected').prop('disabled', false);
    }
});

// carrega as ids para deleção
$('#deleteRegisterModal').on('shown.bs.modal', function () {
    //location.reload();
});

$('#newRegisterModal').on('shown.bs.modal', function () {
    //location.reload();
    console.log($(this).find('.modal-body'));
});

$('#deleteRegisterModal #yes-btn').on('click', function () {
    ids = [];
    $("table input[name=id]:checked").each(function () {
        ids.push($(this).attr('value'));
    });
    console.log(JSON.stringify(ids));
    $.ajax({
        url: '/api'+window.location.pathname,
        method: 'DELETE',
        data: JSON.stringify(ids),
        contentType: 'application/json',
        success: function (data) {
            location.reload();
        },
        dataType: 'json'
    });
});

function get_associado() {
    matricula = $('[name=matricula]').val();
    console.log(matricula)
    $.ajax({
        url: '/api/associados/' + matricula,
        data: null,
        success: function (data) {
            console.log(data);
            $('[name=associado]').val(data.nome);
            $('[name=facilitador]').val(data.facilitador);
        },
        dataType: 'json'
    });
}

function submit_form() {
    $.ajax({
        url: '/api'+window.location.pathname,
        method: 'POST',
        data: $('form').serialize(),
        success: function (data) {
            show_alert('div.alert-success', data);
        },
        error: function (data) {
            show_alert('div.alert-danger', data.responseJSON);
        },
        dataType: 'json'
    });
}

function show_alert(alert, data) {
    $(alert).text(data.message).fadeTo(500, 1);
    window.setTimeout(function () {
        $(alert).fadeTo(500, 0).slideUp(500, function () {
            $(this).hide();
        });
    }, 5000);
}

$('.datetime-picker').datetimepicker({
    format: 'yyyy-mm-ddThh:ii',
    language: 'pt-BR',
    pickerPosition: 'top-right',
    autoclose: true,
    maxView: 2,
    startDate: new Date(new Date(new Date().setMonth(new Date().getMonth()-1)).setDate(15)),
    endDate: new Date(new Date().setDate(15)),
});
