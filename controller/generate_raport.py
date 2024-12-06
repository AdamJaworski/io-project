from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
from model.generate_raport import Report
from typing import Optional

FONT        = 'SpaceMono-Regular' #'Comfortaa'
FONT_BOLD   = 'SpaceMono-Bold'    #'Comfortaa-Bold'
HEADER_SIZE = 18
FONT_SIZE   = 12
LEADING     = 15
TEXT_FOOTER = 70

def generate_report(report_model: Report):
    # Header
    report_model.setTitle('Raport')
    report_model.setFont(FONT_BOLD, HEADER_SIZE)
    header = report_model.header if report_model.header else 'Raport Spotkania'
    report_model.drawCentredString(300, 750, header)
    report_model.line(30, 710, 550, 710)
    report_model.line(30, 50, 550, 50)

    # Transcript
    text = report_model.beginText(40, 680)
    text.textLine('Transkrypt:')
    text.setFont(FONT, FONT_SIZE)
    text.setLeading(LEADING)
    transcript_lines = convert_text_to_lines(text_to_array(report_model.transcript))

    current_y = 660
    for line in transcript_lines:
        text.textLine(justification(line))
        current_y -= LEADING
        if current_y < TEXT_FOOTER:
            # save text
            report_model.drawText(text)

            # Create new page
            set_new_page(report_model)

            # set new text
            text_start = 750
            text = report_model.beginText(40, text_start)
            text.setFont(FONT, FONT_SIZE)
            text.setLeading(LEADING)

            # Reset Y
            current_y = text_start

    # Summary
    text.textLine(' ')
    text.textLine(' ')
    text.setFont(FONT_BOLD, HEADER_SIZE)
    text.textLine('Streszczenie:')
    text.setFont(FONT, FONT_SIZE)

    summary_lines = convert_text_to_lines(text_to_array(report_model.summary))
    for line in summary_lines:
        text.textLine(justification(line))

    report_model.drawText(text)
    report_model.save()

def set_new_page(report_model: Report, page_type: Optional[str] = None):
    report_model.showPage()
    if not page_type:
        report_model.line(30, 770, 550, 770)
        report_model.line(30, 50, 550, 50)


def text_to_array(text: str):
    parts = text.split('\n')
    new_text = ' '.join(parts)
    parts = new_text.split(' ')
    return parts

def convert_text_to_lines(text_array, length_of_words_in_line = 50):
    lines =  []
    new_line = []

    for word in text_array:
        if len(''.join(new_line)) > length_of_words_in_line:
            lines.append(' '.join(new_line))
            new_line = []

        new_line.append(word)


    lines.append(' '.join(new_line))
    return lines


def justification(text_line: str, target_len = 70):
    """ As it would be nice for each line of text to have to same length this func was created.
        It multiplies number of spaces between each world to make line heave ~65 symbols"""

    # If its last lane it's pointless to add so many spaces
    if len(text_line) < 40:
        return text_line

    start = 1
    while len(text_line) < target_len:
        start += 1
        text_line = (' '*start).join(text_line.split(' '*(start-1)))

    # Jeśli długość linijki przeskoczy 65 trzeba to zredukować w dół
    if len(text_line) > target_len:
        above_the_limit = len(text_line) - target_len
        text = text_line.split(' '*(start))
        part1 = (' '*start).join(text[:len(text) - above_the_limit])
        part2 = (' '*(start - 1)).join(text[-above_the_limit:])
        text_line = f"{part1}{' '*(start - 1)}{part2}"
    return text_line

if __name__ == "__main__":
    generate_report(Report('test', transcript='To jest przykładowy tekst do przetestowania rapotru. To jest drugie zdanie. Trzecie zdanie będzie dłuższe od poprzednie by stworzyć trochę różnorodności  w długości linijek. Czwarte zdanie będzie natomiast krótkie bo już nie mam pomysłu co tutaj wpisać. Niestety cały czas trochę brakuje mi znaków dlatego dopisuję również piąte zdanie i teraz mam nadzieję że z takim długim tekstem będę w stanie pracować i dostosuję opdowiednio wszystkie parametry. '*30))