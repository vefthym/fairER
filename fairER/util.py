import gender_guesser.detector as gender
import web.library.methods as methods

d = gender.Detector(case_sensitive=False)  # to avoid creating many Detectors


    # returns True if the given value (assumed to be coming from the protected attribute) is considered protected
    # if return_condition is True, the condition will be returned as string
def pair_is_protected(tuple=None, dataset=None, return_condition=False, explanation=0):
   
    if(return_condition):
        return default_conditions.get(dataset) if methods.protectedCond(dataset,0) is None else methods.protectedCond(dataset,0)
    else:
        try:
            if dataset == 'DBLP-ACM':
                last_author_fname_l = str(tuple.ltable_authors).split(
                    ",")[-1].strip().split(" ")[0].replace('.', '')
                last_author_fname_r = str(tuple.rtable_authors).split(
                    ",")[-1].strip().split(" ")[0].replace('.', '')
                last_author_is_female = ('female' in d.get_gender(last_author_fname_l)) or \
                    ('female' in d.get_gender(last_author_fname_r))

                return last_author_is_female
            else:
                return eval(default_conditions_w_exp[dataset]) if methods.protectedCond(dataset,1) is None else eval(methods.protectedCond(dataset,1))
        except AttributeError:
            if dataset == 'DBLP-ACM':
                last_author_fname_l = str(tuple.left_authors).split(
                    ",")[-1].strip().split(" ")[0].replace('.', '')
                last_author_fname_r = str(tuple.right_authors).split(
                    ",")[-1].strip().split(" ")[0].replace('.', '')
                last_author_is_female = ('female' in d.get_gender(last_author_fname_l)) or \
                    ('female' in d.get_gender(last_author_fname_r))

                return last_author_is_female
            else:
                return eval(default_conditions[dataset]) if methods.protectedCond(dataset,0) is None else eval(methods.protectedCond(dataset,0))



default_conditions = {'Amazon-Google': "('microsoft' in str(tuple.left_manufacturer)) or ('microsoft' in str(tuple.right_manufacturer))",
                      'Beer': "('Red' in str(tuple.left_Beer_Name)) or ('Red' in str(tuple.right_Beer_Name))",
                      'DBLP-ACM': "('female' in d.get_gender(last_author_fname_l)) or ('female' in d.get_gender(last_author_fname_r))",
                      'DBLP-GoogleScholar': "('vldb j' in str(tuple.left_venue)) or ('vldb j' in str(tuple.right_venue))",
                      'Fodors-Zagats': "('asian' == str(tuple.left_entity_type)) or ('asian' == str(tuple.right_entity_type))",
                      'iTunes-Amazon': "('Dance' in str(tuple.left_Genre)) or ('Dance' in str(tuple.right_Genre))",
                      'Walmart-Amazon': "('printers' in str(tuple.left_category)) or ('printers' in str(tuple.right_category))",
                      'D_W_15K_V1': "(comp_size(ent1) < 4) or (comp_size(ent2) < 4)",
                      'D_W_15K_V2': "(comp_size(ent1) < 4) or (comp_size(ent2) < 4)",
                      'D_Y_15K_V1': "(comp_size(ent1) < 4) or (comp_size(ent2) < 4)",
                      'D_Y_15K_V2': "(comp_size(ent1) < 4) or (comp_size(ent2) < 4)"}


default_conditions_w_exp = {'Amazon-Google': "('microsoft' in str(tuple.ltable_manufacturer)) or ('microsoft' in str(tuple.rtable_manufacturer))",
                            'Beer': "('Red' in str(tuple.ltable_Beer_Name)) or ('Red' in str(tuple.rtable_Beer_Name))",
                            'DBLP-ACM': "('female' in d.get_gender(last_author_fname_l)) or ('female' in d.get_gender(last_author_fname_r))",
                            'DBLP-GoogleScholar': "('vldb j' in str(tuple.ltable_venue)) or ('vldb j' in str(tuple.rtable_venue))",
                            'Fodors-Zagats': "('asian' == str(tuple.ltable_entity_type)) or ('asian' == str(tuple.rtable_entity_type))",
                            'iTunes-Amazon': "('Dance' in str(tuple.ltable_Genre)) or ('Dance' in str(tuple.rtable_Genre))",
                            'Walmart-Amazon': "('printers' in str(tuple.ltable_category)) or ('printers' in str(tuple.rtable_category))",
                            'D_W_15K_V1': "(comp_size(ent1) < 4) or (comp_size(ent2) < 4)",
                            'D_W_15K_V2': "(comp_size(ent1) < 4) or (comp_size(ent2) < 4)",
                            'D_Y_15K_V1': "(comp_size(ent1) < 4) or (comp_size(ent2) < 4)",
                            'D_Y_15K_V2': "(comp_size(ent1) < 4) or (comp_size(ent2) < 4)"}

