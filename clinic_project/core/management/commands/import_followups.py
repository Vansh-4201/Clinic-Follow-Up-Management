import csv
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from core.models import FollowUp


class Command(BaseCommand):
    help = "Import followups from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument("--csv", required=True, help="Path to CSV file")
        parser.add_argument("--username", required=True, help="Username of creator")

    def handle(self, *args, **options):
        csv_path = options["csv"]
        username = options["username"]

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stderr.write("User does not exist.")
            return

        clinic = user.userprofile.clinic

        created = 0
        skipped = 0

        with open(csv_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                try:
                    patient_name = row["patient_name"].strip()
                    phone = row["phone"].strip()
                    due_date = row["due_date"].strip()

                    if not patient_name or not phone or not due_date:
                        raise ValueError("Missing required field")

                    due_date = timezone.datetime.strptime(
                        due_date, "%Y-%m-%d"
                    ).date()

                    FollowUp.objects.create(
                        clinic=clinic,
                        created_by=user,
                        patient_name=patient_name,
                        phone=phone,
                        due_date=due_date,
                        language=row.get("language", "en"),
                        notes=row.get("notes", ""),
                    )

                    created += 1

                except Exception:
                    skipped += 1
                    continue

        self.stdout.write(
            f"Import completed: {created} created, {skipped} skipped"
        )
