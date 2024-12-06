from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
from model.generate_raport import Report

def generate_report(report_model: Report):
    # Header
    report_model.setTitle('Raport')
    report_model.setFont('Comfortaa-Bold', 20)
    header = report_model.header if report_model.header else 'Raport Spotkania'
    report_model.drawCentredString(300, 750, header)
    report_model.line(30, 710, 550, 710)


    # Transcript
    text = report_model.beginText(40, 680)
    text.textLine('Transkrypt:')
    text.setFont('Comfortaa', 14)
    text.setLeading(18)
    transcript_lines = convert_text_to_lines(text_to_array(report_model.transcript))

    for line in transcript_lines:
        text.textLine(line)

    # Summary
    text.textLine(' ')
    text.textLine(' ')
    text.setFont('Comfortaa-Bold', 20)
    text.textLine('Streszczenie:')
    text.setFont('Comfortaa', 14)

    summary_lines = convert_text_to_lines(text_to_array(report_model.summary))
    for line in summary_lines:
        text.textLine(line)

    report_model.drawText(text)
    report_model.save()


def text_to_array(text: str):
    parts = text.split('\n')
    new_text = ' '.join(parts)
    parts = new_text.split(' ')
    return parts

def convert_text_to_lines(text_array, line_length=45):
    lines =  []
    new_line = []
    current_line_length = 0
    for word in text_array:
        if current_line_length < line_length:
            new_line.append(word)
            current_line_length += len(word)
        else:
            lines.append(' '.join(new_line))
            new_line = []
            current_line_length = 0
            new_line.append(word)
    lines.append(' '.join(new_line))

    return lines



if __name__ == "__main__":
    generate_report(Report('test', transcript="""Litwo! Ojczyzno moja! ty jesteś jak zdrowie.

Ile cię trzeba cenić, ten tylko się dowie,

Kto cię stracił. Dziś piękność twą w całej ozdobie

Widzę i opisuję, bo tęsknię po tobie.

 
Panno Święta, co Jasnej bronisz Częstochowy

I w Ostrej świecisz Bramie! Ty, co gród zamkowy

Nowogródzki ochraniasz z jego wiernym ludem!

Jak mnie dziecko do zdrowia powróciłaś cudem

(Gdy od płaczącej matki pod Twoję opiekę

Ofiarowany, martwą podniosłem powiekę

I zaraz mogłem pieszo do Twych świątyń progu

Iść za wrócone życie podziękować Bogu),

Tak nas powrócisz cudem na Ojczyzny łono.

Tymczasem przenoś moję duszę utęsknioną

Do tych pagórków leśnych, do tych łąk zielonych,

Szeroko nad błękitnym Niemnem rozciągnionych;

Do tych pól malowanych zbożem rozmaitem,

Wyzłacanych pszenicą, posrebrzanych żytem;"""))