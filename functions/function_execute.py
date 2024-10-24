import json
import subprocess
from termcolor import colored


def execute_script(script):
    stdout_array = []
    stderr = ''
    try:
        # Esegui lo script usando il modulo subprocess
        process = subprocess.Popen(
            script, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            universal_newlines=True
        )

        # Legge stdout e stderr
        for line in process.stdout:
            line = line.rstrip()  # Rimuove i caratteri di fine riga
            stdout_array.append(line)
            print(colored(line, 'green'))  # Output sul terminale colorato

        # Attende la fine del processo
        process.wait()

        # Controlla se c'è output su stderr
        stderr = process.stderr.read()
        if stderr:
            print(colored(stderr, 'red'))  # Stampa errori in rosso

    except OSError as e:
        stderr = f"Errore di esecuzione: {str(e)}"
        print(colored(stderr, 'red'))
    except Exception as e:
        stderr = f"Errore imprevisto: {str(e)}"
        print(colored(stderr, 'red'))

    # Risultato finale
    result = {
        "stdout": "\n".join(stdout_array),
        "stderr": stderr if stderr else "Nessun errore",
        "script": script
    }

    return json.dumps(result)