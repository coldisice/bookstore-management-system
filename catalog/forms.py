from django import forms


class ImportBooksForm(forms.Form):
    excel_file = forms.FileField(
        label='Файл Excel (.xlsx)'
    )
