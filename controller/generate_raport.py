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
    report_model.bookmarkPage("Transkrypt")
    report_model.addOutlineEntry("Transkrypt", "Transkrypt", level=0)
    text.textLine("Transkrypt:")
    transcript_lines = convert_text_to_lines(text_to_array(report_model.transcript))

    write_lines_to_report(report_model, transcript_lines, text, 660)


    # Summary
    set_new_page(report_model, 'main')
    report_model.bookmarkPage("Streszczenie")
    report_model.addOutlineEntry("Streszczenie", "Streszczenie", level=0)
    text = report_model.beginText(40, 680)
    text.textLine('Streszczenie:')

    summary_lines = convert_text_to_lines(text_to_array(report_model.summary))
    write_lines_to_report(report_model, summary_lines, text, 660)

    report_model.save()

def set_new_page(report_model: Report, page_type: Optional[str] = 'text'):
    report_model.showPage()

    if page_type=='text':
        report_model.line(30, 770, 550, 770)
        report_model.line(30, 50, 550, 50)

    if page_type=='main':
        report_model.setFont(FONT_BOLD, HEADER_SIZE)
        header = report_model.header if report_model.header else 'Raport Spotkania'
        report_model.drawCentredString(300, 750, header)
        report_model.line(30, 710, 550, 710)
        report_model.line(30, 50, 550, 50)

def write_lines_to_report(report_model, lines_to_write, current_text_instance, starting_y):
    current_text_instance.setFont(FONT, FONT_SIZE)
    current_text_instance.setLeading(LEADING)

    current_y = starting_y
    for line in lines_to_write:
        current_text_instance.textLine(justification(line))
        current_y -= LEADING
        if current_y < TEXT_FOOTER:
            # save text
            report_model.drawText(current_text_instance)

            # Create new page
            set_new_page(report_model)

            # set new text
            text_start = 740
            current_text_instance = report_model.beginText(40, text_start)
            current_text_instance.setFont(FONT, FONT_SIZE)
            current_text_instance.setLeading(LEADING)

            # Reset Y
            current_y = text_start

    report_model.drawText(current_text_instance)

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
    generate_report(Report('test', transcript='To jest przykładowy tekst do przetestowania rapotru. Jeśli tworzysz streszcznie tego tekstu napisz swój tekst na conajmniej 300 znaków. To jest drugie zdanie. Trzecie zdanie będzie dłuższe od poprzednie by stworzyć trochę różnorodności  w długości linijek. Czwarte zdanie będzie natomiast krótkie bo już nie mam pomysłu co tutaj wpisać. Niestety cały czas trochę brakuje mi znaków dlatego dopisuję również piąte zdanie i teraz mam nadzieję że z takim długim tekstem będę w stanie pracować i dostosuję opdowiednio wszystkie parametry. '*30))