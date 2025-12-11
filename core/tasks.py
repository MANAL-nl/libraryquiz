from django.utils import timezone
from .models import Loan
import datetime
from background_task import background


@background(schedule=0)
def check_loans_task():
    now = timezone.now()

    # Prêts expirés
    expired_loans = Loan.objects.filter(returned=False, status="en cours", due_date__lte=now)
    for loan in expired_loans:
        loan.status = "en train de retourner"
        loan.save()

    # Prêts "en train de retourner" depuis +20 secondes
    finish_loans = Loan.objects.filter(
        returned=False,
        status="en train de retourner",
        due_date__lte=now - datetime.timedelta(seconds=20)
    )
    for loan in finish_loans:
        loan.mark_returned()  # retour automatique, livre disponible maintenant
