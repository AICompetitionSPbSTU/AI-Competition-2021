def run_external(path):
    with open(path, "r") as rnf:
        exec(rnf.read())


run_external('media/hello_world.py')
