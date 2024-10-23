import json
import subprocess

from termcolor import colored


def execute_script(script):
    stdout_array = []
    stderr = ''
    stdout = 'Script executed successfully'
    process = None
    try:
        # Esegui lo script usando il modulo subprocess
        process = subprocess.Popen(
            script, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            universal_newlines=True)

        for line in process.stdout:
            line = line.rstrip()  # Rimuove nuovi i caratteri di fine riga
            stdout_array.append(line)
            print(colored(line, 'green'))



    except subprocess.CalledProcessError as e:
        # Se lo script fallisce, ritorna l'errore
        stderr = e.stderr

    stderr = process.stderr.read()
    if process is not None and stderr:
        stdout = ""

    result = {
        "stdout": stdout,
        "stderr": stderr,
        "script": script
    }
    return json.dumps(result)
