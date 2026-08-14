import datetime

from django.db import transaction

from apps.content.dtos import LandingPage, TicketsInfo
from common.exceptions import NotFoundError

TICKETS_ROLE = "tickets"

# Taken from the 2026 website: the contact for the presale and the contacts of the ball team
TICKETS_CONTACT = ("Hana Benešová", "benesova@sutb.cz", "")
TICKETS_RESERVATION_FROM = datetime.date(2026, 1, 20)
TEAM_CONTACTS = [
    ("Manažer plesu", "Bc. David Fiala", "fiala@sutb.cz", "+420 739 437 387"),
    ("Manažerka plesu", "Kristina Marečková", "mareckova@sutb.cz", "+420 720 182 609"),
    ("Produkce", "Bc. Lukáš Faksa", "faksa@sutb.cz", "+420 605 456 216"),
    ("Spolupráce a sponzoři", "Bc. Daniel Bušos", "busos@sutb.cz", "+420 731 926 176"),
    ("Propagace", "Tímea Patáková", "patakova@sutb.cz", "+420 735 389 035"),
]


class ContentService:
    """Content of the landing page: texts, contacts and ticket presale settings."""

    def __init__(self, *, content_repository, contact_repository, ticket_content_repository):
        self.content_repository = content_repository
        self.contact_repository = contact_repository
        self.ticket_content_repository = ticket_content_repository

    def get_landing(self):
        """Get texts, team contacts (without the ticket contact) and the ticket presale settings."""
        tickets = self.ticket_content_repository.get_first()
        if tickets is None:
            raise NotFoundError("The ticket settings of the landing page are not filled in.")
        return LandingPage(
            contents=self.content_repository.get_all(),
            contacts=self.contact_repository.list_excluding_role(TICKETS_ROLE),
            tickets=TicketsInfo(reservations_from=tickets.reservation_from, contact=tickets.contact),
        )

    @transaction.atomic
    def seed_landing(self):
        """Create the contacts and the ticket settings when there is no contact, return how many contacts were created."""
        if self.contact_repository.count() > 0:
            return 0
        name, email, phone = TICKETS_CONTACT
        tickets_contact = self.contact_repository.create(role=TICKETS_ROLE, name=name, email=email, phone=phone)
        self.ticket_content_repository.create(reservation_from=TICKETS_RESERVATION_FROM, contact=tickets_contact)
        for role, contact_name, contact_email, contact_phone in TEAM_CONTACTS:
            self.contact_repository.create(role=role, name=contact_name, email=contact_email, phone=contact_phone)
        return 1 + len(TEAM_CONTACTS)
