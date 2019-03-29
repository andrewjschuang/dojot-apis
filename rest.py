import requests
import json

dojot_host='http://localhost:8000'

def login(dojot_host=dojot_host, username='admin', passwd='admin'):
    data = {'username': username, 'passwd': passwd}
    r = requests.post(dojot_host + '/auth', json=data)
    if r.status_code == requests.codes.ok:
        return json.loads(r.text)['jwt']
    else:
        return json.loads(r.text)

def get_templates(jwt, dojot_host=dojot_host):
    headers = {'Authorization': 'Bearer ' + jwt}
    r = requests.get(dojot_host + '/template', headers=headers)
    return json.loads(r.text)

def get_devices(jwt, dojot_host=dojot_host):
    headers = {'Authorization': 'Bearer ' + jwt}
    r = requests.get(dojot_host + '/device', headers=headers)
    return json.loads(r.text)

def create_template(jwt, template, dojot_host=dojot_host):
    headers = {
        'Authorization': 'Bearer ' + jwt,
        'Content-Type': 'application/json'
    }
    r = requests.post(dojot_host + '/template', headers=headers, json=template)
    return json.loads(r.text)

def create_device(jwt, device, dojot_host=dojot_host):
    labels = [x['label'] for x in device['templates']]
    dojot_templates = get_templates(jwt, dojot_host)['templates']
    templates = [x for x in dojot_templates if x['label'] in labels]
    ids = [x['id'] for x in templates]
    attrs = [x['static_attrs'] for x in device['templates']][0]
    
    headers = {
        'Authorization': 'Bearer ' + jwt,
        'Content-Type': 'application/json'
    }

    for t in templates:
        for tt in t['attrs']:
            if tt['label'] in attrs.keys():
                tt['static_value'] = attrs[tt['label']]

    static_attrs = []
    for i in templates:
        for j in i['attrs']:
            static_attrs.append(j)

    data = {
        'templates': ids,
        'label': device['label'],
        'attrs': static_attrs
    }
    
    r = requests.post(dojot_host + '/device', headers=headers, json=data)
    return json.loads(r.text)

def get_history(jwt, device_id, attrs=[], n=1, dojot_host=dojot_host):
    headers = {'Authorization': 'Bearer ' + jwt}
    r = requests.get(dojot_host + '/history/device/' + device_id + '/history?lastN=' + str(n), headers=headers)
    return json.loads(r.text)

def delete_device(jwt, device_id, dojot_host=dojot_host):
    headers = {'Authorization': 'Bearer ' + jwt}
    r = requests.delete(dojot_host + '/device/' + device_id, headers=headers)
    return json.loads(r.text)

def delete_all_devices(jwt, dojot_host=dojot_host):
    headers = {'Authorization': 'Bearer ' + jwt}
    pagination = True
    while pagination is True:
        r = get_devices(jwt, dojot_host)
        for device in r['devices']:
            delete_device(jwt, device['id'], dojot_host)
        pagination = r['pagination']['has_next']
    return True

def get_users(jwt, dojot_host=dojot_host):
    headers = {'Authorization': 'Bearer ' + jwt}
    r = requests.get(dojot_host + '/auth/user', headers=headers)
    return json.loads(r.text)

def get_user(jwt, user, dojot_host=dojot_host):
    headers = {'Authorization': 'Bearer ' + jwt}
    r = requests.get(dojot_host + '/auth/user/' + user, headers=headers)
    return json.loads(r.text)

def create_user(jwt, user, dojot_host=dojot_host):
    headers = {'Authorization': 'Bearer ' + jwt}
    r = requests.post(dojot_host + '/auth/user', headers=headers, json=user)
    return json.loads(r.text)

def configure_user(jwt, user, dojot_host=dojot_host):
    headers = {'Authorization': 'Bearer ' + jwt}
    r = requests.put(dojot_host + '/auth/user/' + user['username'], headers=headers, json=user)
    return json.loads(r.text)

def delete_user(jwt, user, dojot_host=dojot_host):
    headers = {'Authorization': 'Bearer ' + jwt}
    r = requests.delete(dojot_host + '/auth/user/' + user, headers=headers)
    return json.loads(r.text)

def get_tenants(jwt, dojot_host=dojot_host):
    headers = {'Authorization': 'Bearer ' + jwt}
    r = requests.get(dojot_host + '/auth/admin/tenants', headers=headers)
    return json.loads(r.text)

def get_flows(jwt, dojot_host=dojot_host):
    headers = {'Authorization': 'Bearer ' + jwt}
    r = requests.get(dojot_host + '/flows/v1/flow', headers=headers)
    return json.loads(r.text)

def get_flow(jwt, flow, dojot_host=dojot_host):
    headers = {'Authorization': 'Bearer ' + jwt}
    r = requests.get(dojot_host + '/flows/v1/flow/' + flow, headers=headers)
    return json.loads(r.text)

def configure_flow(jwt, flow, dojot_host=dojot_host):
    headers = {'Authorization': 'Bearer ' + jwt}
    r = requests.put(dojot_host + '/flows/v1/flow/' + flow['id'], headers=headers)
    return json.loads(r.text)

def delete_flow(jwt, flow, dojot_host=dojot_host):
    headers = {'Authorization': 'Bearer ' + jwt}
    r = requests.delete(dojot_host + '/flows/v1/flow/' + flow, headers=headers)
    return json.loads(r.text)

def delete_all_flows(jwt, dojot_host=dojot_host):
    headers = {'Authorization': 'Bearer ' + jwt}
    r = requests.delete(dojot_host + '/flows/v1/flow', headers=headers)
    return json.loads(r.text)

def add_node(jwt, node, dojot_host=dojot_host):
    headers = {'Authorization': 'Bearer ' + jwt}
    r = requests.post(dojot_host + '/flows/v1/node', headers=headers, json=node)
    return json.loads(r.text)

def delete_node(jwt, node, dojot_host=dojot_host):
    headers = {'Authorization': 'Bearer ' + jwt}
    r = requests.delete(dojot_host + '/flows/v1/node/' + node, headers=headers)
    return json.loads(r.text)
