from wtforms import Form, StringField, SelectField, DateField, validators


class RegistrationForm(Form):
    name = StringField(u'Name', [validators.Length(min=5, max=20), validators.input_required()])
    gender = SelectField(u'Gender', choices=[
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Unknown')
    ], default='U')
    birthday = DateField(u'Birthday', [validators.input_required()], format='%m/%d/%Y')
    country = SelectField(u'Country', choices=[
        ('CN', 'China'),
        ('US', 'United States'),
        ('ZZ', 'Unspecified')
    ], default='ZZ')
