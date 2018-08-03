kill_method_dict = {
    'Null': 'Unknown',
    '0'  : 'Unknown',
    '1'  : 'Blunt force',
    '2'  : 'Gunshot',
    '3'  : 'Poinson-Non Medical',
    '4'  : 'Sharp force-stabbing',
    '5'  : 'Strangulation',
    '6'  : 'Poison-Medical',
    '7'  : 'Incendiary device',
    '8'  : 'Suffocation',
    '9'  : 'Gassed',
    '10' : 'Drowning',
    '11' : 'Fire',
    '12' : 'Starvation',
    '13' : 'Shaken Baby Syndrome',
    '14' : 'Sharp force-Chop',
    '15' : 'Hanging',
    '16' : 'Ordered hit',
    '17' : 'Staged accident',
    '18' : 'Vehicle hit',
    '19' : 'Thrown from cliff'
}

killed_with_hands = {
    '0' : 'No',
    '1' : 'Yes',
    'Null' : 'Unknown'
}

weapons = {
    '0' : 'None',
    '1' : 'Found at scene',
    '3': 'Brought with', # I don't know why they skipped 2
    'Null': 'Unknown'
}

gun = {
    '0' : 'None',
    '1' : 'Handgun',
    '2' : 'Rifle',
    '3' : 'Shotgun',
    '4' : 'Used (Type uknown)',
    'Null' : 'Unknown'
}
