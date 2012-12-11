# -*- coding: utf-8 -*- 

from wtforms import Form, TextField, PasswordField, TextAreaField, validators

class RegistrationForm(Form):
    """
    Registration form validator.
    """
    team_name = TextField(u'Название команды', [
        validators.Required(message = u'Заполните поле'),
        validators.Length(min = 4, max = 25, message = u'От 4 до 25 символов')
    ])
    
    institution = TextField(u'Учебное заведение', [
        validators.Length(min = 3, max = 25, message = u'От 3 до 50 символов')
    ])
    
    team_members = TextAreaField(u'Список участников')
    
    password = PasswordField(u'Пароль', [
        validators.Required(message = u'Заполните поле'),
        validators.EqualTo(u'confirm', message = u'Пароли должны совпадать!')
    ])
    
    confirm = PasswordField(u'Повтор пароля', [
        validators.Required(message = u'Заполните поле'),
        validators.EqualTo(u'password', message='')
    ])
    