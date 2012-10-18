# -*- coding: utf-8 -*- 

from wtforms import Form, TextField, PasswordField, TextAreaField, validators

class RegistrationForm(Form):
    team_name = TextField('Название команды', [
        validators.Required(message = 'Заполните поле'),
        validators.Length(min = 4, max = 25, message = 'От 4 до 25 символов')
    ])
    
    institution = TextField('Учебное заведение', [
        validators.Required(message = 'Заполните поле'),
        validators.Length(min = 3, max = 25, message = 'От 3 до 50 символов')
    ])
    
    team_members = TextAreaField('Список участников', [
        validators.Required(message = 'Заполните поле'),
     ])
    
    password = PasswordField('Пароль', [
        validators.Required(message = 'Заполните поле'),
        validators.EqualTo('confirm', message='Пароли должны совпадать!')
    ])
    
    confirm = PasswordField('Повтор пароля', [
        validators.Required(message = 'Заполните поле'),
        validators.EqualTo('password', message='')
    ])
    