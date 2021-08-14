import gender_guesser.detector as gender

d = gender.Detector(case_sensitive=False)  # to avoid creating many Detectors


# returns True if the given value (assumed to be coming from the protected attribute) is considered protected
def tuple_is_protected(tuple, dataset='datasets/Test'):
    if dataset == 'Amazon-Google':
        return ('microsoft' in str(tuple.left_manufacturer)) or \
               ('microsoft' in str(tuple.right_manufacturer))  # Amazon-Google
    elif dataset == 'Beer':
        return ('Red' in str(tuple.left_Beer_Name)) or ('Red' in str(tuple.right_Beer_Name))  # Beer
    elif dataset == 'DBLP-ACM':
        # main_author_fname_l = str(tuple.left_authors).split(" ")[0].replace('.','')
        # main_author_fname_r = str(tuple.right_authors).split(" ")[0].replace('.', '')
        last_author_fname_l = str(tuple.left_authors).split(",")[-1].strip().split(" ")[0].replace('.','')
        last_author_fname_r = str(tuple.left_authors).split(",")[-1].strip().split(" ")[0].replace('.', '')
        last_author_is_female = ('female' in d.get_gender(last_author_fname_l)) or \
                                ('female' in d.get_gender(last_author_fname_r))

        # print(main_author_fname_l, 'is detected as ', 'protected' if main_author_is_female else 'nonprotected')
        # unknown (name not found), andy (androgynous), male, female, mostly_male, or mostly_female
        return last_author_is_female  # DBLP-ACM
        # return (tuple.left_year > 2000) or (tuple.right_year > 2000)  # DBLP-ACM
    elif dataset == 'DBLP-GoogleScholar':
        # return ('acm' in str(tuple.left_venue)) or ('acm' in str(tuple.right_venue))  # DBLP-Scholar
        return ('vldb j' in str(tuple.left_venue)) or ('vldb j' in str(tuple.right_venue))  # DBLP-Scholar
    elif dataset == 'Fodors-Zagats':
        return ('asian' == str(tuple.left_entity_type)) or ('asian' == str(tuple.right_entity_type))  # Fodors-Zagats
    elif dataset == 'iTunes-Amazon':
        # return ('Rock' in str(tuple.left_Genre)) or ('Rock' in str(tuple.right_Genre))  # iTunes-Amazon
        # return (', 201' in str(tuple.left_Released)) or (', 201' in str(tuple.right_Released))  # iTunes-Amazon
        return ('Dance' in str(tuple.left_Genre)) or ('Dance' in str(tuple.right_Genre))  # iTunes-Amazon
        # main_author_fname_l = str(tuple.left_Artist_Name).split(" ")[0].replace('.', '')
        # main_author_fname_r = str(tuple.right_Artist_Name).split(" ")[0].replace('.', '')
        # main_author_is_female = ('female' in d.get_gender(main_author_fname_l)) or \
        #                         ('andy' == d.get_gender(main_author_fname_l)) or \
        #                         ('female' in d.get_gender(main_author_fname_r)) or \
        #                         ('andy' == d.get_gender(main_author_fname_r))
        # print(main_author_fname_l, 'is detected as ', 'protected' if main_author_is_female else 'nonprotected')
        # unknown (name not found), andy (androgynous), male, female, mostly_male, or mostly_female
        # return main_author_is_female
    elif dataset == 'Walmart-Amazon':
        return ('printers' in str(tuple.left_category)) or ('printers' in str(tuple.right_category))  # Walmart-Amazon
    else:
        return ', 201' not in tuple.right_Released  # datasets/test
