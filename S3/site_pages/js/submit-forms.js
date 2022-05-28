function submitSubscribeForm(csrfToken) {
    $.ajax({
        url: '/forms/submit_subscribe_form/',
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': csrfToken,
            'sub_email': document.getElementById('id_subscriber_email').value,
            'fname': document.getElementById('id_subscriber_fname').value,
            'lname': document.getElementById('id_subscriber_lname').value
        },
        success: function() {
            console.log('POST succeeded.')
            alert('Thanks! You have subscribed.')
        },
        error: function() {
            console.log('POST failed.')
            alert('Your request could not be submitted.')
        }
    })
}

function submitEmailForm(csrfToken) {
    $.ajax({
        url: '/forms/submit_contact_email/',
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': csrfToken,
            'viewer_email': document.getElementById('id_viewer_email').value
        },
        success: function() {
            console.log('POST succeeded.')
            alert('Your request has been submitted.')
        },
        error: function() {
            console.log('POST failed.')
            alert('Your request could not be submitted.')
        }
    })
}

function submitContactForm(csrfToken) {
    $.ajax({
        url: '/forms/submit_contact_form/',
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': csrfToken,
            'fname': document.getElementById('id_fname').value,
            'lname': document.getElementById('id_lname').value,
            'email': document.getElementById('id_email').value,
            'comment': document.getElementById('id_comment').value
        },
        success: function() {
            console.log('POST succeeded.')
            alert('Your request has been submitted.')
        },
        error: function() {
            console.log('POST failed.')
            alert('Your request could not be submitted.')
        }
    })
}

function submitContribForm(csrfToken) {
    $.ajax({
        url: '/forms/submit_contrib_form/',
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': csrfToken,
            'fname': document.getElementById('id_fname').value,
            'lname': document.getElementById('id_lname').value,
            'email': document.getElementById('id_email').value,
            'uname': document.getElementById('id_uname').value,
            'about': document.getElementById('id_about').value,
        },
        success: function() {
            console.log('POST succeeded.')
            alert('Your request has been submitted.')
            window.location.replace('/')
        },
        error: function(){
            console.log('POST failed.')
            alert('Your request could not be submitted.')
        }
    })
}