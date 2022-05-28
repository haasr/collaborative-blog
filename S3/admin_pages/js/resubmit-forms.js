function resendFormData(csrfToken, resultID, to, formName) {
    let formData = document.getElementById(resultID).innerHTML;

    $.ajax({
        url: '/admin_pages/failures/mail_send_failures/resend_form_email/',
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': csrfToken,
            'form_id': resultID.split('-')[1],
            'form_data': formData,
            'to': to,
            'form_name': formName
        },
        success: function(resp) {
            console.log('POST succeeded.')
            alert('Email successfully resent.')
            window.location.reload();
        },
        error: function(resp) {
            console.log('POST failed');
            if (resp.status == 400) {
                alert('Attempted to resend the email and failed')
            }
            else
                alert('Your request could not be submitted.')
        }
    })
}