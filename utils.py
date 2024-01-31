from rich.console import Console
from rich.table import Table
console = Console()


# table header
table = Table("ID", "Name", "Phone", "Email address", "Created")


def render_rows(rows):
    for id_, name, phone, email, created_on in rows:
        table.add_row(str(id_), name, str(phone), email, created_on)
    console.print(table)
