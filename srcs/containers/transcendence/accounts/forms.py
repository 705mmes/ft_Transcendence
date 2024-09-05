# forms.py
from django import forms
from django_otp.forms import OTPTokenForm as BaseOTPTokenForm
from django_otp.plugins.otp_totp.models import TOTPDevice

class OTPTokenForm(BaseOTPTokenForm):
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(user=user, *args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        otp_token = cleaned_data.get('otp_token')

        if otp_token:
            # Ensure the user is provided
            if self.user is None:
                raise forms.ValidationError("User not specified")

            # Retrieve the user's TOTP device
            try:
                device = TOTPDevice.objects.get(user=self.user, name='default')
            except TOTPDevice.DoesNotExist:
                raise forms.ValidationError("TOTP device does not exist for this user")

            if not device.verify_token(otp_token):
                raise forms.ValidationError("Invalid OTP token")
        
        return cleaned_data
