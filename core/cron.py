from django.utils import timezone
from django.core.mail import send_mail
from .models import Loan

def check_loans():
    now = timezone.now()

    # 1. Trouver les prêts expirés depuis moins de 20 secondes (message email)
    expired_loans = Loan.objects.filter(
        returned=False,
        due_date__lte=now,
        status="en cours"
    )

    for loan in expired_loans:
        # envoyer email
        send_mail(
            "Délai terminé - Retour du livre",
            f"Le délai pour retourner le livre '{loan.book.title}' est dépassé.\n"
            "Vous avez maintenant 20 secondes pour le rendre.",
            "ton_email@gmail.com",
            [loan.user.email],
        )

        loan.status = "en train de retourner"
        loan.save()

    # 2. Ensuite : les prêts "en train de retourner" depuis +20 secondes → retourner
    finish_loans = Loan.objects.filter(
        returned=False,
        status="en train de retourner",
        due_date__lte=now - timezone.timedelta(seconds=20)
    )

    for loan in finish_loans:
        loan.returned = True
        loan.status = "retourné"
        loan.save()

        # rétablir le stock
        book = loan.book
        book.stock += 1
        book.save()
