from model import summary

def get_meeting_text_shortcut(input_text: str):
    context = f"Streść spotaknie z transkryptu, nie dodawaj nic od siebie, tylko streszczenie spotakania. Transkrypt:\n{input_text}"
    try:
        response = summary.llm.create_chat_completion(messages=[
            {
                "role": "user",
                "content": context
            }]
        )
    except ValueError:
        summary.double_n_ctx()
        response = get_meeting_text_shortcut(input_text)

    return response


def get_text_from_response(response) -> str:
    return response["choices"][0]["message"]["content"]

if __name__ == "__main__":
    text = 'Cześć dzień dobry Witam was bardzo serdecznie Ja mam na imię Mikołaj i zapraszam was na kolejny odcinek spotkania z transportem after bardzo bardzo bardzo bardzo bardzo bardzo Wietrzny dzień i słoneczny zarazem wybieramy się moimi na wycieczkę do Sieradza to jest jakieś 80 km za łodzią w stronę w stronę w stronę w stronę Wrocławia drogą S8 załadowali meble w Czosnowie meble takie powiedzmy bardziej wyposażenie warsztatowe o o niestety nie obyło się bez problemów bo Początkowo miało być palec 16 według wiedzy człowieka który mi dał tę robotę a się okazało że finalnie wyszło 8 palet z tym że dwie były bardzo niewymiarowe no i był spory problem z załadunkiem i żeby załadować te dwie palety na chłodnię to się namęczyłem dobre pół godziny dodatkowo na tej palecie zostały położone płyty to są takie no takie do do skręcania szafek takie takie takie takie takie fronty mam wrażenie i w żaden sposób nie zostało to zabezpieczone przez nadawcę dopiero tutaj załadowcza mi polecił wspierać to jednym pasem i i tyle ale ale sposób ułożenia tego na palecie tragiczny żeby tak dać to komuś do przewozu No ale co jedziemy trochę miałem pewne obawy A propos tej trasy bo tak wszystko na styk tutaj musisz być na załadunek na sztywno Bo odwołają transport później trochę mam stresa czy będę mieć aby na pewno z czym wrócić bo nic mi się nie udało znaleźć przed weekendem więc zobaczymy jak to wyjdzie finalnie poza tym że się opłaciłem na na załadunku to po cichu liczę że nie będzie że nie będzie tragedii i że ten dzień fajnie nam wyjdzie Trochę mnie martwi naprawdę potężny wiatr pod który będziemy jechać bo naprawdę może nam tą normę spalania podnieść do góry ale czasem bywa i tak nie jedziemy Za jakieś Turbo małe pieniądze Więc powiedzmy że jeżeli jeżeli jeżeli jeżeli jeżeli jeżeli będziemy się musieli zmagać z wiatrem to wyższa stawka będzie w pewien sposób rekompensować mamy jeszcze przed sobą tankowanie samochodu bo nie zdążyłem tego zrobić przed weekendem i na 190 km przed nami więc jak na moją jazdę to dosyć daleka trasa w jedną stronę no i zobaczymy co ten dzień przyniesie Mam nadzieję że będzie pozytywny uwaga uwaga dzisiaj Międzynarodówka bo opuszczamy miejscowość Czechy Moi drodzy Mam nadzieję że to było widać na kamerce bo się starałem'
    test = get_meeting_text_shortcut(text)
    print(test)
    test = get_text_from_response(test)
    print(test)