def import_mob(name, pagelimit=8000):
    """ Imports the named monsters' stat block from the www.aidedd.org website.
        Returns the fully parsed stat block to the Mob class.

        ~~~

         -  Please use a string with spaces as separators.

         -  If the entered name does not match a known mob in the aidedd data base the server does not return a
         detectable error, instead it generates a functioning, useless page. It's for this reason that import_mob
         instead has a lower bound for page sizes (8000 bytes). If you're having issues generating a known statblock
         then set'pagelimit' to 0. """

    from urllib import request
    from html.parser import HTMLParser
    import pickle

    name = name.replace(' ', '-').rstrip('1234567890').capitalize()

    try:
        page_request = request.urlopen("https://www.aidedd.org/dnd/monstres.php?vo=" + name)
    except Exception:
        raise Exception('something went wrong with that URL')
    html_byteslike = page_request.read()
    if html_byteslike.__sizeof__() < pagelimit:
        raise Exception('Page appears not to exist, better check your input and the page itself.')
    html_stringlike = html_byteslike.decode('UTF-8')

    class MyHTMLParser(HTMLParser):
        page_data = []

        def handle_data(self, data):
            self.page_data.append(data)

    parser = MyHTMLParser()
    parser.feed(html_stringlike)
    page_data = parser.page_data

    Gob = parser.page_data[page_data.index(name): page_data.index('DnD 5e Monsters')]
    # useful_data
    # Finally the data we're after, marked by the name of the mob in the start of the block.
    # End slice arbitrarily marks the end of the stat block.

    del page_request, html_byteslike, html_stringlike, parser, page_data     # Clean-up :3

    body = Gob[4].split()
    AC = Gob[6].split()
    HP = Gob[8].split()
    speed = Gob[10].split()
    stat_bloc = Gob[12:23:2]
    stat_bloc = [stat.split() for stat in Gob[12:23:2]]

    if Gob.count("Saving Throws"):
        ST = Gob[Gob.index("Saving Throws") + 1].split()
    else:
        ST = []

    if Gob.count("Skills"):
        Skills = Gob[Gob.index("Skills") + 1].split()
    else:
        Skills = []

    if Gob.count("Damage Immunities"):
        Dmg_I = Gob[Gob.index("Damage Immunities") + 1].split()
    else:
        Dmg_I = []

    if Gob.count("Damage Resistances"):
        Dmg_R = Gob[Gob.index("Damage Resistances") + 1].split()
    else:
        Dmg_R = []

    if Gob.count("Damage Vulnerabilities"):
        Dmg_V = Gob[Gob.index("Damage Vulnerabilities") + 1].split()
    else:
        Dmg_V = []

    if Gob.count("Condition Immunities"):
        Cond_I = Gob[Gob.index("Condition Immunities") + 1].split()
    else:
        Cond_I = []

    Senses = Gob[Gob.index("Senses") + 1].split(',')
    languages = Gob[Gob.index("Languages") + 1].split(',')
    CR = Gob[Gob.index("Challenge") + 1].split('(')

    chal_index = Gob.index("Challenge")
    act_index = Gob.index("ACTIONS")
    if act_index - chal_index > 2:
        Additional_Features_Name = Gob[chal_index + 2:act_index:2]
        Additional_Features_Text = Gob[chal_index + 3:act_index:2]
        Additional_Features = dict(zip(Additional_Features_Name, Additional_Features_Text))
        del Additional_Features_Name, Additional_Features_Text
    else:
        Additional_Features = {}

    if len(Gob[-2]) >= 30:
        additional_info = Gob.pop()

    if Gob.count("LEGENDARY ACTIONS"):
        LA_index = Gob.index("LEGENDARY ACTIONS")
        LA_name = Gob[LA_index + 2::2]
        LA_text = Gob[LA_index + 3::2]
        legendary_actions = dict(zip(LA_name, LA_text))
        Gob = Gob[:LA_index]
        del LA_index, LA_name, LA_text

    if Gob.count("REACTIONS"):
        r_index = Gob.index("REACTIONS")
        r_name = Gob[r_index + 1::2]
        r_text = Gob[r_index + 2::2]
        reactions = dict(zip(r_name, r_text))
        Gob = Gob[:r_index]
        del r_index, r_name, r_text

    actions = Gob[act_index + 1:]
    for string in reversed(actions):
        if string.startswith(':'):
            try:
                non_attack_actions = actions.pop(actions.index(string) + 1)
            except IndexError:
                pass
            finally:
                break

    # Next thingy goes on \n data processing ensues

    pickle_file = open(self.save_file_location + '.pickle', 'wb')  # Consider using pathlib instead.
    pickle.dump(self, pickle_file)
    pickle_file.close()
