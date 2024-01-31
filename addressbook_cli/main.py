import typer
from rich.console import Console
from typing_extensions import Annotated
from addressbook_cli.db import cursor, conn
from typing import List
from addressbook_cli.utils import render_rows

app = typer.Typer()
console = Console()


@app.command()
def ls():
    cursor.execute("SELECT * FROM addresses ORDER BY created_on DESC;")
    rows = cursor.fetchall()
    if len(rows) > 0:
        render_rows(rows)
    else:
        console.print("Addressbook is empty")
    conn.close()


@app.command()
def find(
        name: Annotated[str, typer.Option(help="name of person.")],
):
    cursor.execute("SELECT * FROM addresses WHERE name like '%'||?||'%'", (name,))
    rows = cursor.fetchall()
    if len(rows) > 0:
        render_rows(rows)
    else:
        console.print(f"No result with name: {name}")
    conn.close()


@app.command()
def add(
        phone: Annotated[str, typer.Option(help="Phone number of person.")],
        name: Annotated[str, typer.Option(help="name of person.")],
        email: Annotated[str, typer.Option(help="Email number of person.")] = " ",
):
    cursor.execute('INSERT INTO addresses (name, phone, email) VALUES (?, ?, ?)', (name, phone, email))
    conn.commit()
    id_ = cursor.lastrowid
    cursor.execute("SELECT * FROM addresses WHERE id = ?", (id_,))
    row = cursor.fetchone()
    render_rows([row])
    # console.print("New contact added ✨")
    message = typer.style(f"✨ New contact added", fg=typer.colors.BRIGHT_GREEN)
    typer.echo(message)
    conn.close()


@app.command()
def update(
        id_: str,
        name: Annotated[str, typer.Option(help="Contact's name")] = None,
        phone: Annotated[str, typer.Option(help="Contact's Phone number.")] = None,
        email: Annotated[str, typer.Option(help="Contact's Email address.")] = None
):
    cursor.execute("SELECT * FROM addresses WHERE id = ?", (id_,))
    row = cursor.fetchone()
    if row:
        id_, curr_name, curr_phone, curr_email, curr_created_on = row

        updated_name = name if name else curr_name
        updated_phone = phone if phone else curr_phone
        updated_email = email if email else curr_email

        cursor.execute("UPDATE addresses SET name = ?, phone = ?, email = ? WHERE id = ?",
                       (updated_name, updated_phone, updated_email, id_))
        conn.commit()
        render_rows([(id_, updated_name, updated_phone, updated_email, curr_created_on)])
        message = typer.style(f"✅️Contact ({id_}) has been updated", fg=typer.colors.BRIGHT_GREEN)
        typer.echo(message)
        conn.close()
    else:
        message = typer.style(f"😢Contact ({id_}) not found", fg=typer.colors.BRIGHT_RED)
        typer.echo(message)


@app.command()
def remove(ids: List[str]):
    if not ids:
        print("No provided id(s)")
        raise typer.Abort()
    else:
        confirm = typer.confirm(typer.style(f"🗑Continue with deletion?", fg=typer.colors.BRIGHT_YELLOW))
        if not confirm:
            message = typer.style(f"Closed without deleting", fg=typer.colors.BRIGHT_BLUE)
            typer.echo(message)
            raise typer.Abort()
        else:
            for id_ in ids:
                cursor.execute('DELETE FROM addresses WHERE id = ?', id_)
                conn.commit()
            message = typer.style(f"✅️Contact {ids} has been deleted", fg=typer.colors.BRIGHT_GREEN)
            typer.echo(message)
        conn.close()


@app.command()
def reset():
    cursor.execute("DROP TABLE IF EXISTS addresses")
    conn.commit()
    console.print(f"Contacts have been cleared")
    conn.close()


if __name__ == "__main__":
    app()
