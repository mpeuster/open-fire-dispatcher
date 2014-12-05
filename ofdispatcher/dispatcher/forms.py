from django import forms
from dispatcher.models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = (
            "firstname",
            "secondname",
            "mail1",
            "sms1",
            "active",
            "test"
        )

        labels = {
            "firstname": "Vorname",
            "secondname": "Nachname",
            "mail1": "E-Mail Adresse",
            "sms1": "Handynummer",
            "active": "Aktiviert",
            "test": "Testalarmierungen",
        }

        help_texts = {
            "mail1": "Die E-Mail Adresse an die der Alarm versendet wird.",
            "sms1": "Die Handynummer an die der Alarm versendet wird.",
            "active": "Alarmierungen werden nur an als 'Aktiviert' markierte Einsatzkraefte versendet",
            "test": "Die monatliche Testalarmierungen an diese Einsatzkraft versenden.",
        }
