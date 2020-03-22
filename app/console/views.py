from flask import render_template
from flask_login import login_required, current_user
from app.auth import hqauth as auth
from app import config

from . import console

@console.route('/')
@login_required
def consolepage():
    codes = [
        {
            'id':0,
            'name':'Algolia Pro Plan',
            'banner':'https://res.cloudinary.com/hilnmyskv/image/upload/q_auto/v1584543140/Algolia_com_Website_assets/images/shared/algolia_logo/logo-algolia-nebula-blue-full.svg',
            'description': 'Algolia is providing free pro plans to those working on COVID-19 Releated problems',
            'claimed': True,
            'code': 'test code2'
        },
        {
            'id':1,
            'name':'Free Domain from Domain.com',
            'banner':'https://www.domain.com/static/img/domaincom/logo.svg',
            'description': 'Get a free domain from Domain.com!',
            'claimed': False
        },
        {
            'id':0,
            'name':'Algolia Pro Plan',
            'banner':'https://res.cloudinary.com/hilnmyskv/image/upload/q_auto/v1584543140/Algolia_com_Website_assets/images/shared/algolia_logo/logo-algolia-nebula-blue-full.svg',
            'description': 'Algolia is providing free pro plans to those working on COVID-19 Releated problems',
            'claimed': True,
            'code': 'TEST CODE',
        },
    ]
    return render_template('codes.html', codes=codes)


# Claim a token
@console.route('/claim')
@login_required
def claim():
    # check if the user has already claimed a token

    # allocate them one
    return ''
