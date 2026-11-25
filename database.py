
import subprocess
from config import DATABASE_NAME, MYSQL_COMMAND


def sql_quote(value):
    """Safely quote a string for a MySQL SQL statement."""
    value = str(value)

    value = value.replace("\\", "\\\\")
    value = value.replace("'", "''")
    value = value.replace("\0", "")

    return "'" + value + "'"


def execute_query(sql):
    """
    Execute SQL through the MySQL command-line client.
    Returns command output as text.
    """

    command = [
        MYSQL_COMMAND,
        f"--defaults-file={__import__('os').path.expanduser('~/.my.cnf')}",
        "--batch",
        "--raw",
        "--skip-column-names",
        f"--database={DATABASE_NAME}"
    ]

    try:
        result = subprocess.run(
            command,
            input=sql,
            text=True,
            capture_output=True,
            check=True
        )

        return result.stdout.strip()

    except FileNotFoundError:
        print("ERROR: MySQL command-line client was not found.")
        return None

    except subprocess.CalledProcessError as error:
        print("DATABASE ERROR:")
        print(error.stderr.strip())
        return None


def get_rows(sql):
    """Execute a SELECT query and return rows."""

    output = execute_query(sql)

    if output is None or output == "":
        return []

    return [
        line.split("\t")
        for line in output.splitlines()
    ]
