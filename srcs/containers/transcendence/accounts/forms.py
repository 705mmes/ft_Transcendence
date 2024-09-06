from django import forms
from django_otp.forms import OTPTokenForm as BaseOTPTokenForm
from django_otp.plugins.otp_totp.models import TOTPDevice

class OTPTokenForm(BaseOTPTokenForm):
    otp_device = forms.ModelChoiceField(
        queryset=TOTPDevice.objects.none(),
        widget=forms.HiddenInput,
        required=False
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['otp_device'].queryset = TOTPDevice.objects.filter(user=self.user)

    def clean(self):
        cleaned_data = super().clean()
        otp_token = cleaned_data.get('otp_token')
        otp_device = cleaned_data.get('otp_device')

        if otp_token and otp_device:
            # Verify the token
            if not otp_device.verify_token(otp_token):
                raise forms.ValidationError("Invalid OTP token")
        elif not otp_device:
            raise forms.ValidationError("OTP device not found for this user")

        return cleaned_data
