from php import Php


def test_http_build_query_pass():
    assert(Php.http_build_query({"alpha": "bravo"}) == "alpha=bravo&")
    assert(Php.http_build_query({"charlie": ["delta", "echo", "foxtrot"]}) == "charlie[1]=echo&charlie[0]=delta&charlie[2]=foxtrot&")
    assert(Php.http_build_query({"golf": ["hotel", {"india": "juliet", "kilo": ["lima", "mike"]}, "november", "oscar"]}) == "golf[1][india]=juliet&golf[1][kilo][1]=mike&golf[1][kilo][0]=lima&golf[0]=hotel&golf[3]=oscar&golf[2]=november&")


def test_parse_ini_file_pass():

    ini_file = "/tmp/python-php-test.ini"
    ini = """
        [section alpha]
        bravo = 7
        charlie = "delta"
        echo[] = 1
        echo[] = 2
        echo[] = 3

        [section foxtrot]
        golf[hotel] = 1
        golf[juliet] = 2
        golf[kilo] = "3"
    """.replace("    ", "")

    with open(ini_file, "w") as f:
        f.write(ini)

    stripped = Php.parse_ini_file(ini_file, strip_quotes=True)
    unstripped = Php.parse_ini_file(ini_file)

    assert(stripped == {'section foxtrot': {'golf': {'kilo': '3', 'hotel': '1', 'juliet': '2'}}, 'section alpha': {'bravo': '7', 'echo': ['1', '2', '3'], 'charlie': 'delta'}})
    assert(unstripped == {'section foxtrot': {'golf': {'kilo': '"3"', 'hotel': '1', 'juliet': '2'}}, 'section alpha': {'bravo': '7', 'echo': ['1', '2', '3'], 'charlie': '"delta"'}})
