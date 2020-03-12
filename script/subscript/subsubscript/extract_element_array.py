def GetTargetNumber(specified_obs_place, obsplace_dic):
    """
    Investigate observation number.
    """
    for comb_obs_place in obsplace_dic.items():
        key = comb_obs_place[0]
        value = comb_obs_place[1]
        if specified_obs_place == key:
            obs_number = value
        else:
            pass
    return obs_number


def GetTargetNumberList(obs_number, one_list):
    target_number_list = []
    for one_mat_element in one_list:
        target = one_mat_element[0]
        partner = one_mat_element[1]
        if target == obs_number:
            target_number_list.append(one_mat_element)
        else:
            pass
    return target_number_list


def TransformNumberToPlace(obsplace_dic, i, j):
    """
    Transform number to place for being corresponded number to observation place.
    """
    comb = []
    for obs_place in obsplace_dic.items():
        key = obs_place[0]
        value = obs_place[1]
        if i == value:
            comb.append(key)
        else:
            pass
    
    for obs_place in obsplace_dic.items():
        key = obs_place[0]
        value = obs_place[1]
        if j == value:
            comb.append(key)
        else:
            pass
    return tuple(comb)