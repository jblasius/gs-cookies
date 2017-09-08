    # selectedChoices = ChoiceObj('girls', session.get('selected'))
    # form = GirlLookupForm(obj=selectedChoices)

    # # Retrieve list of all girl names
    # girl_list = get_girl_names()
    # if girl_list == -1:
    #     flash('Error retrieving girl names.')
    #     return redirect(url_for('index'))

    # form.girls.choices = [(c, c) for c in sorted(girl_list.iterkeys())]

    # if form.validate_on_submit():
    #     session['selected'] = form.girls.data
        
    #     #TODO Save the selected user/girl combination(s) to the database

    #     return redirect(url_for('profile'))
    # else:
    #     print form.errors
    # return render_template('profile.html',
    #                        form=form,
    #                        title='My Account',
    #                        selected=session.get('selected'))
