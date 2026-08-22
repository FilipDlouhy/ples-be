import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.template.loader import render_to_string

from apps.salons.time_slots import format_time

logger = logging.getLogger(__name__)


class MakerEmailService:
    """Sends the salon booking confirmation after the surrounding transaction commits."""

    def send_confirmation(self, *, reservation):
        """E-mail the customer which maker, time and service was booked."""
        time = format_time(reservation.time)
        message = EmailMultiAlternatives(
            subject=f"Reprezentační ples UTB {settings.BALL_YEAR} - Potvrzení rezervace",
            body=f"Máte rezervaci u paní {reservation.maker.name} na {time}. Vybraná služba je {reservation.service}.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[reservation.email],
        )
        html = render_to_string(
            "salons/emails/reservation.html",
            {
                "year": settings.BALL_YEAR,
                "maker": reservation.maker.name,
                "time": time,
                "service": reservation.service,
            },
        )
        message.attach_alternative(html, "text/html")
        transaction.on_commit(lambda: self._send(message))

    def _send(self, message):
        try:
            message.send()
        except Exception:
            logger.exception("Could not send email '%s' to %s", message.subject, message.to)
