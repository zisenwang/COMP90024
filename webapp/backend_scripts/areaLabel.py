# l stands for longtitude
# a stands for altitude
# return the suburban name of given bounding box
def areaLabel(l,a):
    if (l >= 144.9267 and l <= 144.9869 and a >= -37.7802 and a <= -37.7325):
        return 'Brunswick - Coburg'
    if (l >= 144.8889 and l <= 144.9404 and a >= -37.7897 and a <= -37.7346):
        return 'Essendon'
    if (l >= 144.9027 and l <= 144.9914 and a >= -37.8507 and a <= -37.7754):
        return 'Melbourne City'
    if (l >= 144.9792 and l <= 145.0368 and a >= -37.7856 and a <= -37.7503):
        return 'Darebin - South'
    if (l >= 144.9588 and l <= 145.0453 and a >= -37.8345 and a <= -37.7735):
        return 'Yarra'
    if (l >= 144.9833 and l <= 145.0327 and a >= -37.8663 and a <= -37.8296):
        return 'Stonnington - West'
    if (l >= 144.8974 and l <= 145.0105 and a >= -37.8917 and a <= -37.8200):
        return 'Port Phillip'
    if (l >= 144.9993 and l <= 145.1067 and a >= -37.8759 and a <= -37.7769):
        return 'Boroondara'
    if (l >= 145.0671 and l <= 145.1841 and a >= -37.8025 and a <= -37.7340):
        return 'Manningham - West'
    if (l >= 145.0951 and l <= 145.1696 and a >= -37.8620 and a <= -37.7922):
        return 'Whitehorse - West'
    if (l >= 144.9850 and l <= 145.0553 and a >= -37.9964 and a <= -37.8838):
        return 'Bayside'
    if (l >= 144.9970 and l <= 145.0882 and a >= -37.9388 and a <= -37.8602):
        return 'Glen Eira'
    if (l >= 145.0277 and l <= 145.0922 and a >= -37.8930 and a <= -37.8374):
        return 'Stonnington - East'
    if (l >= 145.0344 and l <= 145.1563 and a >= -38.0850 and a <= -37.9330):
        return 'Kingston'
    if (l >= 144.9703 and l <= 145.0754 and a >= -37.7557 and a <= -37.6910):
        return 'Darebin - North'
    if (l >= 145.0789 and l <= 145.5800 and a >= -37.7417 and a <= -37.4093):
        return 'Nillumbik - Kinglake'
    if (l >= 145.0278 and l <= 145.1437 and a >= -37.7851 and a <= -37.6826):
        return 'Banyule'
    if (l >= 144.8807 and l <= 145.2658 and a >= -37.7000 and a <= -37.2629):
        return 'Whittlesea - Wallan'
    if (l >= 144.8016 and l <= 144.9347 and a >= -37.7761 and a <= -37.6982):
        return 'Keilor'
    if (l >= 144.4577 and l <= 144.9212 and a >= -37.5677 and a <= -37.1751):
        return 'Macedon Ranges'
    if (l >= 144.8862 and l <= 144.9853 and a >= -37.7360 and a <= -37.6909):
        return 'Moreland - North'
    if (l >= 144.6236 and l <= 144.8705 and a >= -37.6649 and a <= -37.4819):
        return 'Sunbury'
    if (l >= 144.7600 and l <= 144.9778 and a >= -37.7104 and a <= -37.5021):
        return 'Tullamarine - Broadmeadows'
    if (l >= 145.1909 and l <= 145.3476 and a >= -37.9649 and a <= -37.8330):
        return 'Knox'
    if (l >= 145.1678 and l <= 145.2970 and a >= -37.8118 and a <= -37.7024):
        return 'Manningham - East'
    if (l >= 145.2133 and l <= 145.3187 and a >= -37.8439 and a <= -37.7618):
        return 'Maroondah'
    if (l >= 145.1569 and l <= 145.2167 and a >= -37.8652 and a <= -37.8012):
        return 'Whitehorse - East'
    if (l >= 145.2869 and l <= 145.8784 and a >= -37.9750 and a <= -37.5260):
        return 'Yarra Ranges'
    if (l >= 145.3640 and l <= 145.7651 and a >= -38.3325 and a <= -37.8577):
        return 'Cardinia'
    if (l >= 145.2265 and l <= 145.3854 and a >= -38.0796 and a <= -37.9419):
        return 'Casey - North'
    if (l >= 145.2149 and l <= 145.4307 and a >= -38.2485 and a <= -38.0170):
        return 'Casey - South'
    if (l >= 145.0795 and l <= 145.2519 and a >= -38.0777 and a <= -37.9240):
        return 'Dandenong'
    if (l >= 145.0825 and l <= 145.2201 and a >= -37.9401 and a <= -37.8533):
        return 'Monash'
    if (l >= 144.7444 and l <= 144.8559 and a >= -37.8228 and a <= -37.6629):
        return 'Brimbank'
    if (l >= 144.7514 and l <= 144.9155 and a >= -37.9000 and a <= -37.8138):
        return 'Hobsons Bay'
    if (l >= 144.8392 and l <= 144.9165 and a >= -37.8270 and a <= -37.7558):
        return 'Maribyrnong'
    if (l >= 144.3336 and l <= 144.7682 and a >= -37.8105 and a <= -37.5464):
        return 'Melton - Bacchus Marsh'
    if (l >= 144.4441 and l <= 144.8274 and a >= -38.0046 and a <= -37.7810):
        return 'Wyndham'

    return 'Unknown'
