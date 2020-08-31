import configparser

conf = configparser.ConfigParser()

# socket class parameters
conf['socket'] = {}
socket_conf = conf['socket']
socket_conf['overall_width'] = '18.0'
socket_conf['overall_height'] = '18.0'
socket_conf['keyswitch_width'] = '14.4'
socket_conf['keyswitch_height'] = '14.4'
socket_conf['plate_thickness'] = '4.0'
socket_conf['hot_swap'] = 'False'





with open('default_config.ini', 'w') as configfile:
    conf.write(configfile)
