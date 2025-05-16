def check_guess(actual_word, guess):
    """
    Compare guess to actual_word and return a string with:
    'G' for correct letter in correct position (green),
    'Y' for correct letter in wrong position (yellow),
    'X' for incorrect letter (gray).
    Handles repeated letters properly.
    """
    result = ['X'] * len(guess)
    actual_word_chars = list(actual_word)
    
    # First pass: check for correct letters in correct positions (green)
    for i, letter in enumerate(guess):
        if letter == actual_word[i]:
            result[i] = 'G'
            actual_word_chars[i] = None  
    
    # Second pass: check for correct letters in wrong positions (yellow)
    for i, letter in enumerate(guess):
        if result[i] == 'G':
            continue  # Already handled
        if letter in actual_word_chars:
            result[i] = 'Y'
            actual_word_chars[actual_word_chars.index(letter)] = None  
    
    return ''.join(result)
