import sys
from io import StringIO

def execute_user_code(code, input_data):
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()

    try:
        namespace = {}
        input_lines = input_data.split('\n')
        input_iterator = iter(input_lines)
        
        def custom_input(prompt=''):
            try:
                return next(input_iterator)
            except StopIteration:
                raise EOFError("No more input available")

        namespace['input'] = custom_input

        exec(code, namespace)

        output = mystdout.getvalue()
        output = '\n'.join(line.rstrip() for line in output.splitlines())

        return output
    except Exception as e:
        return "Error"
    finally:
        sys.stdout = old_stdout