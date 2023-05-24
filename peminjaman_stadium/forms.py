from django import forms

class PesanStadiumForm(forms.Form):
    stadium = forms.CharField()
    tanggal = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#tanggal'
        })
    )

