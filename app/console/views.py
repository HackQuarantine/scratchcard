from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.auth import hqauth as auth
from app.db import User, Credit, Claimed, Token, db
from app import config

from . import console

def is_code_avaliable(code):
    if code.unique == True:
        avaliable = db.session.query(Token).filter_by(type=code_id, owner=None)
        if avaliable is None:
            return False
    elif code.limit and code.limit > 0 and len(code.claimed) >= code.limit:
        return False
    return True
def query_codes(student_status=False):
    # hacky quick solution

    res = []
    if student_status == False:
        res = Credit.query.filter_by(student_only=False).all()
    else:
        # students get all 
        res = Credit.query.all()
    # hacky
    for i in res:
        i.avaliable = is_code_avaliable(i)
        i.is_claimed = False
        i.user_code = None
        for item in i.claimed:
            if item in current_user.claimed:
                i.is_claimed = True

        if i.is_claimed:
            if i.unique:
                token = Token.query.filter_by(owner=current_user.id).first()
                i.user_code = token.code
            else:
                i.user_code = i.code
    return res


@console.route('/')
@login_required
def consolepage():
    codes = query_codes(
        student_status=current_user.student_status
    )
    return render_template('codes.html', codes=codes)


# Claim a token
@console.route('/claim/<code_id>', methods=["POST"])
@login_required
def claim(code_id):
    try:
        # check if already have claimed this code
        user_claimed = db.session.query(Claimed).filter_by(owner=current_user.id,type=code_id).all()
        if user_claimed is not None and len(user_claimed) > 0:
            flash('You\'ve already claimed this code!', 'error')
            return redirect(url_for('console.consolepage'))

        code = db.session.query(Credit).filter_by(id=code_id).first_or_404()
        first = {
            'id': None
        }
        if code.unique == True:
            avaliable = db.session.query(Token).filter_by(type=code_id, owner=None)
            # Claim the token
            if avaliable is None:
                flash('We\'ve reached out limit on those codes!', 'error')
                return redirect(url_for('console.consolepage'))
            first = avaliable[0]
            first.owner = current_user.id
            db.session.add(first)
        if code.limit and code.limit > 0 and len(code.claimed) >= code.limit:
            flash('We\'ve reached out limit on those codes!', 'error')
            return redirect(url_for('console.consolepage'))

        # create the claimed object so we can log these actions
        claimed = Claimed()
        claimed.type = code_id
        claimed.owner = current_user.id
        claimed.token = first['id']

        db.session.add(claimed)
        db.session.commit()

    except Exception as e:
        print(e)
        db.session.rollback()
        flash('Failed to claim', 'error')
        return redirect(url_for('console.consolepage'))


    flash('You managed to claim a token!', 'success')
    return redirect(url_for('console.consolepage'))



@console.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if not current_user.is_admin():
        flash('Only admins are allowed to view this page', 'error')
        return redirect(url_for('home.homepage'))

    codes = query_codes(student_status=True)
    if request.method == 'POST':
        data = request.form
        # we need to validate the submission
        try:
            title = data.get('title')
            description = data.get('description')
            banner = data.get('banner_url')
            student_only = bool(data.get('student_only', False))
            if 'unique_code' in data and data['unique_code'] == 'on':
                obj = Credit()
                obj.title = title
                obj.banner = banner
                obj.description = description
                obj.student_only = student_only
                db.session.add(obj)
                # create the object + the token
                codes = data['codes'].split('\r\n')

                item = db.session.query(Credit.id).filter(Credit.title == obj.title).first()
                for code in codes:
                    if code == '':
                        continue
                    curr = Token()
                    curr.code = code
                    curr.type = item.id
                    db.session.add(curr)
            else:
                limit = data.get('limit')
                code = data.get('code')
                obj = Credit()
                obj.title = title
                obj.banner = banner
                obj.description = description
                obj.student_only = student_only
                obj.limit = limit
                obj.code = code
                db.session.add(obj)
            db.session.commit()

        except Exception as e:
            print(e)
            db.session.rollback()
            flash('Failed to added', 'error')
            return render_template('admin.html', codes=codes)

        flash('Added', 'success')

    return render_template('admin.html', codes=codes)


# Modify the code type.
# Currently low priority for implementation, so will hack on later.
@console.route('/admin/delete/<code_id>', methods=['GET', 'POST'])
@login_required
def delete_credit(code_id):
    if not current_user.is_admin():
        flash('Only admins are allowed to view this page', 'error')
        return redirect(url_for('home.homepage'))

    if request.method == 'POST':
        try:
            code = Credit.query.filter_by(id=code_id).first_or_404()
            ##db.session.delete(Claimed.query.filter_by(owner=code_id))
            #db.session.delete(Token.query.filter_by(owner=code_id))
            db.session.delete(code)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            flash('Failed to delete', 'error')
            return redirect(url_for('console.admin'))
        flash('Deleted', 'success')

    return redirect(url_for('console.admin'))
