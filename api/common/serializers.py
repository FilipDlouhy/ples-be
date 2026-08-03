from rest_framework import serializers


class LaravelSerializer(serializers.Serializer):
    """Serializer whose missing-field error reads like Laravel: "The name field is required."."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            message = f"The {name} field is required."
            field.error_messages["required"] = message
            field.error_messages["null"] = message
            if "blank" in field.error_messages:
                field.error_messages["blank"] = message
