from django import forms

class ZipField(forms.Field):
    def to_python(self, value):
        if not value:
            return ''
        return value
    def validate(self, value):
        try:
            zipnum = int(value)
        except:
            raise forms.ValidationError('Zip code can only include numbers')
        if len(value) != 5:
            raise forms.ValidationError('Zip code must be five digits long')

class SettingsForm(forms.Form):
    interests = forms.CharField(max_length=500,
                                widget=forms.HiddenInput, required=False)
    firstname = forms.CharField(max_length=30, required=False)
    lastname = forms.CharField(max_length=30, required=False)
    email = forms.EmailField()
    zipcode = ZipField(required=False)

