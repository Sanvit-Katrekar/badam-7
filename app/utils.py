''' Utility functions defined here '''

def time_in_words(time: str) -> str:
    m, s = [int(val) for val in time.split(':')]
    time_taken = ""
    if m != 0:
        time_taken += f"{m}min "
    if s != 0:
        time_taken += f"{s}s"
    return time_taken.strip()
