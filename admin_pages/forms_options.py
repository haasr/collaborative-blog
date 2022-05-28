# Options classes for admin_pages.forms

class FontOptions:
    GOOGLE_FONTS = (
        ("""<link href="https://fonts.googleapis.com/css2?family=Arimo&display=swap" rel="stylesheet">&&Arimo""", """Arimo"""),
        ("""<link href="https://fonts.googleapis.com/css2?family=Barlow:wght@500&display=swap" rel="stylesheet">&&Barlow""", """Barlow"""),
        ("""<link href="https://fonts.googleapis.com/css2?family=Poppins&display=swap" rel="stylesheet">&&Poppins""", """Poppins"""),
        ("""<link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">&&Roboto""", """Roboto"""),
        ("""<link href="https://fonts.googleapis.com/css2?family=Metrophobic&display=swap" rel="stylesheet">&&Metrophobic""", """Metrophobic"""),
        ("""<link href="https://fonts.googleapis.com/css2?family=Montserrat&display=swap" rel="stylesheet">&&Montserrat""", """Montserrat"""),
        ("""<link href="https://fonts.googleapis.com/css2?family=Mulish&display=swap" rel="stylesheet">&&Mulish""", """Mulish"""),
        ("""<link href="https://fonts.googleapis.com/css2?family=Open+Sans&display=swap" rel="stylesheet">&&Open Sans""", """Open Sans"""),
        ("""<link href="https://fonts.googleapis.com/css2?family=Cousine&display=swap" rel="stylesheet">&&Cousine""", """Cousine"""),
        ("""<link href="https://fonts.googleapis.com/css2?family=Roboto+Mono&display=swap" rel="stylesheet">&&Roboto Mono""", """Roboto Mono"""),
        ("""<link href="https://fonts.googleapis.com/css2?family=Comic+Neue&display=swap" rel="stylesheet">&&Comic Neue""", """Comic Neue"""),
        ("""<link href="https://fonts.googleapis.com/css2?family=Sansita&display=swap" rel="stylesheet">&&Sansita""", """Sansita"""),
    )

class ImageOptions:
    PERCENTAGES = (
            ('width: 10%;', '10%'),
            ('width: 20%;', '20%'),
            ('width: 30%;', '30%'),
            ('width: 40%;', '40%'),
            ('width: 50%;', '50%'),
            ('width: 60%;', '60%'),
            ('width: 70%;', '70%'),
            ('width: 80%;', '80%'),
            ('width: 90%;', '90%'),
            ('width: 100%;', '100%'),
        )

    POSITIONS = (
        ('float: left;', 'float left'),
        ('float: right;', 'float right'),
        ('display: inline;', 'inline'),
        ('display: block;', 'block'),
        ('display: inline-block;', 'inline-block'),
    )

class TextOptions:
    TEXT_COLORS = (
        ('text-light', 'Light'),
        ('text-dark', 'Dark'),
    )

    HEADER_SIZES = (
        ('h1', 'Large'),
        ('h2', 'Medium'),
        ('h3', 'Small')
    )

class PostOptions:
    VISIBILITY = (
        ('private', 'Private (I can see & access)'),
        ('restrict', 'Restriced (I + collaborators can see & access)'),
        ('public', 'Public (All can see, restricted access)'),
    )