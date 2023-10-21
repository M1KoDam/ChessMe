def encode_chessboard(chessboard):
    encode_result = ""

    for w in range(8):
        for h in range(8):
            cur_figure = chessboard.square[w][h]
            cur_figure_icon = " " if cur_figure is None else cur_figure.get_icon()

            encode_result += f"{letter_translation[w]}{number_translation[h]}:{cur_figure_icon}, "
    return encode_result[:-2]


letter_transcription = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
number_transcription = {'8': 0, '7': 1, '6': 2, '5': 3, '4': 4, '3': 5, '2': 6, '1': 7}

letter_translation = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
number_translation = {0: '8', 1: '7', 2: '6', 3: '5', 4: '4', 5: '3', 6: '2', 7: '1'}
