import os
import re
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import PyPDF2

class Command(BaseCommand):
    help = 'Import users from a PDF file containing: S. No., Name of the Student, Roll Number, Personal Email ID'

    def add_arguments(self, parser):
        parser.add_argument('--pdf', type=str, help='Path to the PDF file containing user data.')

    def handle(self, *args, **options):
        pdf_path = options['pdf']
        if not pdf_path or not os.path.exists(pdf_path):
            self.stdout.write(self.style.ERROR("Please provide a valid PDF file path using --pdf"))
            return

        try:
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                raw_text = ""
                for page in reader.pages:
                    page_text = page.extract_text()
                    raw_text += page_text + "\n"
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error reading PDF: {e}"))
            return

        # Split the extracted text into lines for debugging.
        lines = raw_text.splitlines()
        self.stdout.write("Extracted lines:")
        for i, line in enumerate(lines, start=1):
            self.stdout.write(f"{i}: {line}")

        # Define a regex pattern.
        # This pattern expects:
        #   Group 1: S. No. (one or more digits)
        #   Group 2: Name (lazy match, can contain spaces)
        #   Group 3: Roll Number (non-space sequence)
        #   Group 4: Email (non-space characters, with an @ in it)
        pattern = re.compile(r'^(\d+)\s+(.*?)\s+(\S+)\s+(\S+@\S+)$')
        user_count = 0

        for line in lines:
            line = line.strip()
            # Skip header or empty lines
            if not line or "S. No." in line or "Name of the Student" in line or "Roll Number" in line or "Personal Email ID" in line:
                continue

            match = pattern.match(line)
            if match:
                s_no = match.group(1)
                name = match.group(2)
                rollno = match.group(3)
                email = match.group(4)

                # Check if a user with this username already exists.
                if User.objects.filter(username=name).exists():
                    self.stdout.write(self.style.WARNING(f"User '{name}' already exists. Skipping."))
                    continue

                # Create the user using the roll number as password.
                user = User(username=name, email=email)
                user.set_password(rollno)  # Hash the roll number as password.
                user.save()
                user_count += 1
                self.stdout.write(self.style.SUCCESS(f"Created user: {name} (Roll No: {rollno})"))
            else:
                # If the line did not match, print it for debugging.
                self.stdout.write(self.style.WARNING(f"Line did not match: {line}"))

        self.stdout.write(self.style.SUCCESS(f"Imported {user_count} users from the PDF."))
