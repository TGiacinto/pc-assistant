import json
import subprocess

from termcolor import colored


def execute_script(script):
    try:
        # Esegui lo script usando il modulo subprocess
        result = subprocess.run(
            script,  # Lo script da eseguire (può essere un comando o uno script Python)
            shell=True,  # Utilizza la shell per eseguire il comando
            check=True,  # Solleva un'eccezione se il comando fallisce
            stdout=subprocess.PIPE,  # Cattura lo stdout (output standard)
            stderr=subprocess.PIPE,  # Cattura lo stderr (errori)
            text=True  # Interpreta l'output come stringa
        )

        stdout = result.stdout
        stderr = result.stderr
        stdout = colored(stdout, 'green')
        print(stdout)
        if stdout != '':
            stdout = "Script Eseguito correttamente"

    except subprocess.CalledProcessError as e:
        # Se lo script fallisce, ritorna l'errore
        stdout = e.stdout
        stderr = e.stderr

    result = {
        "stdout": stdout,
        "stderr": stderr,
        "script": script
    }
    return json.dumps(result)
