from django import forms


def validate_not_empty(value):
    if value == '':
        raise forms.ValidationError(
            'Пост не может быть пустым :(',
            params={'value': value},
        )
