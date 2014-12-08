from django import forms
from dispatcher.models import Contact, AlarmLoop


class ContactForm(forms.ModelForm):

    loops_choices = []
    loops = forms.MultipleChoiceField(
        required=True,
        label="Schleifen",
        help_text="Schleifen bei denen diese Einsatzkraft alarmiert werden soll (STRG fuer Mehrfachauswahl).",
        choices=loops_choices)

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

    def update_loop_choices(self, department):
        # get loops that are valid for a contact and add them to form
        self.fields["loops"].choices = [
            (l.id, l.loop) for l in AlarmLoop.objects.filter(
                department=department)]
