
def get_interaction_output(prompt):
    generator_path = os.path.join(
        '.',
        'conv-ai',
        'interact.py'
    )
    length = 400
    command = f'py {generator_path} --model_type gpt2 --model_name_or_path gpt2 --prompt "{prompt}" --length {length}'
    output = subprocess.check_output(command, shell=True)
    return output