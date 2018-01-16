import argparse
import json
import sys
from urllib.parse import urlparse
from pySBOLx.pySBOLx import XDocument

def load_alnum_id(id_data):
    if id_data.replace('_', '').replace('-', '').isalnum():
        return id_data.replace('-', '_')
    else:
        parsed_uri = urlparse(id_data)

        return parsed_uri.path[1:].replace('/', '_').replace('-', '_').replace('.', '_')

def load_activity(src_entity_data, doc, operator, replicate_id, entity_dict, act_dict, act_name=None, act_desc=None, dest_entity_data=None, custom=[]):
    try:
        src_entity_key = src_entity_data['sample']
    except:
        src_entity_key = src_entity_data

    try:
        src_entity = act_dict[src_entity_key]
    except:
        src_entity = entity_dict[src_entity_key]

    if dest_entity_data is None:
        act_dict[src_entity_key] = doc.create_activity(operator, replicate_id, [src_entity], act_name, act_desc, custom)
    else:
        try:
            dest_entity_key = dest_entity_data['uri']
        except:
            try:
                dest_entity_key = dest_entity_data['dest']
            except:
                dest_entity_key = dest_entity_data
        
        dest_entity = entity_dict[dest_entity_key]

        doc.create_activity(operator, replicate_id, [src_entity], act_name, act_desc, custom, dest_entity)

def load_src_dest_activity(entity_data, doc, operator, replicate_id, entity_dict, act_dict, act_name=None, act_desc=None):
    try:
        src_entity_data = entity_data['source']
    except:
        try:
            src_entity_data = entity_data['sample']['source']
        except:
            src_entity_data = entity_data['src']

    try:
        try:
            dest_entity_data = entity_data['destination']
        except:
            try:
                dest_entity_data = entity_data['sample']['destination']
            except:
                dest_entity_data = entity_data['dest']

        if isinstance(dest_entity_data, str):
            load_activity(src_entity_data, doc, operator, replicate_id, entity_dict, act_dict, act_name, act_desc, dest_entity_data)
        else:
            for dest_entity_datum in dest_entity_data:
                load_activity(src_entity_data, doc, operator, replicate_id, entity_dict, act_dict, act_name, act_desc, dest_entity_datum)
    except:
        dest_entity_data = entity_data['dests']

        for dest_entity_datum in dest_entity_data:
            load_activity(src_entity_data, doc, operator, replicate_id, entity_dict, act_dict, act_name, act_desc, dest_entity_datum)

def load_operator_activities(operator_data, doc, replicate_id, entity_dict, act_dict):
    operator = operator_data['type'].replace('-', '_')

    try:
        act_name = operator_data['name']
    except:
        act_name = None

    try:
        act_desc = operator_data['description']
    except:
        act_desc = None

    try:
        entity_data = operator_data['samples']
    except:
        try:
            entity_data = operator_data['transfer']
        except:
            entity_data = operator_data['distribute']

    for entity_datum in entity_data:
        try:
            load_src_dest_activity(entity_datum, doc, operator, replicate_id, entity_dict, act_dict, act_name, act_desc)
        except:
            load_activity(entity_datum, doc, operator, replicate_id, entity_dict, act_dict, act_name, act_desc)

def load_upload_activity(operator_data, doc, replicate_id, entity_dict, act_dict):
    operator = operator_data['type'].replace('-', '_')

    try:
        act_name = operator_data['name']
    except:
        act_name = None

    try:
        act_desc = operator_data['description']
    except:
        act_desc = None

    if operator == 'uploadData':
        entity_data = operator_data['samples']

        source_key = 'dest'
    else:
        entity_data = operator_data['measure']

        source_key = 'uri'

    custom = []

    try:
        custom.append(operator_data['manifest'])
        custom.append('manifest')
    except:
        pass

    try:
        custom.append(operator_data['instrument_configuration'])
        custom.append('instrument_configuration')
    except:
        pass

    for entity_datum in entity_data:
        activity = load_activity(entity_datum, doc, operator, replicate_id, entity_dict, act_dict, act_name, act_desc, entity_datum, custom)

def load_step_activities(step_data, doc, entity_dict, act_dict):
    operator_data = step_data['operator']
    
    replicate_id = repr(step_data['id'])

    try:
        load_upload_activity(operator_data, doc, replicate_id, entity_dict, act_dict)
    except:
        load_operator_activities(operator_data, doc, replicate_id, entity_dict, act_dict)

def load_sample(sample_data, doc, entity_dict, condition=None, src_samples=[]):
    try:
        sample_key = sample_data['sample']

        sample_id = load_alnum_id(sample_key)
    except:
        sample_key = sample_data

        sample_id = load_alnum_id(sample_key)

    if sample_key not in entity_dict:
        entity_dict[sample_key] = doc.create_sample(sample_id, condition, src_samples)
    
    return entity_dict[sample_key]

def load_src_sample(sample_data, doc, entity_dict):
    try:
        src_sample_data = sample_data['source']
    except:
        try:
            src_sample_data = sample_data['sample']['source']
        except:
            src_sample_data = sample_data['src']
    
    return load_sample(src_sample_data, doc, entity_dict)

def load_dest_samples(sample_data, doc, entity_dict, src_sample, condition=None):
    try:
        dest_sample_data = sample_data['destination']
    except:
        try:
            dest_sample_data = sample_data['sample']['destination']
        except:
            dest_sample_data = sample_data['dest']

    if isinstance(dest_sample_data, str):
        load_sample(dest_sample_data, doc, entity_dict, condition, [src_sample])
    else:
        for dest_sample_datum in dest_sample_data:
            load_sample(dest_sample_datum, doc, entity_dict, condition, [src_sample])
        
def load_src_dest_samples(sample_data, doc, entity_dict, condition=None):
    src_sample = load_src_sample(sample_data, doc, entity_dict)

    try:
        load_dest_samples(sample_data, doc, entity_dict, src_sample, condition)
    except:
        dest_sample_data = sample_data['dests']

        for dest_sample_datum in dest_sample_data:
            load_sample(dest_sample_datum['dest'], doc, entity_dict, condition, [src_sample])

def load_strains(condition_data, doc, entity_dict):
    strain_id = load_alnum_id(condition_data['strain'])

    return [doc.create_strain(strain_id, strain_id)]

def load_plasmids(condition_data, doc):
    plasmids = []

    for plasmid_data in condition_data['plasmids']:
        if isinstance(plasmid_data, str):
            plasmid_id = load_alnum_id(plasmid_data)

            plasmids.append([doc.create_plasmid(plasmid_id, plasmid_id)])
        else:
            sub_plasmids = []

            for plasmid_datum in plasmid_data:
                plasmid_id = load_alnum_id(plasmid_datum)

                sub_plasmids.append(doc.create_plasmid(plasmid_id, plasmid_id))

            plasmids.append(sub_plasmids)

    return plasmids

def load_inducers(condition_data, doc, unit_dict, om, mags, units):
    mags.append(repr(condition_data['amount']))

    symbol = condition_data['units']

    if symbol not in unit_dict:
        unit_dict[symbol] = doc.create_unit(symbol, om)

    units.append(unit_dict[symbol])

    inducer_id = load_alnum_id(condition_data['compound'])

    return [doc.create_inducer(inducer_id, inducer_id)]

def load_condition(condition_data, doc, entity_dict, unit_dict, om, plasmid=None):
    try:
        devices = load_strains(condition_data, doc, entity_dict)
    except:
        devices = []

    if plasmid is not None:
        if isinstance(plasmid, str):
            devices.append(plasmid)
        else:
            for plasm in plasmid:
                devices.append(plasm)

    try:
        src_sample = load_src_sample(condition_data, doc, entity_dict)

        sub_systems = doc.get_systems(src_sample.built)
    except:
        sub_systems = []

    mags = []
    units = []

    try:
        inputs = load_inducers(condition_data['inducer'], doc, unit_dict, om, mags, units)
    except:
        inputs = []

    if len(devices) > 0 or len(sub_systems) > 0 or len(inputs) > 0:
        return doc.create_system(devices, sub_systems, inputs, mags, units)
    else:
        return None

def load_experimental_data(operator_data, doc, exp, replicate_id, attachs, entity_dict):
    operator = operator_data['type'].replace('-', '_')

    if operator == 'uploadData':
        entity_data = operator_data['samples']

        source_key = 'dest'
    else:
        entity_data = operator_data['measure']

        source_key = 'uri'

    for entity_datum in entity_data:
        source = entity_datum[source_key]

        if source not in entity_dict:
            sample = load_sample(entity_datum, doc, entity_dict)

            attach_id = load_alnum_id(source)

            attachs.append(doc.create_attachment(attach_id, attach_id, source, replicate_id))

            entity_dict[source] = doc.create_experimental_data([attachs[-1]], sample, exp, operator, replicate_id)

def load_operator_entities(operator_data, doc, entity_dict, unit_dict, om):
    try:
        entity_data = operator_data['samples']
    except:
        try:
            entity_data = operator_data['transfer']
        except:
            entity_data = operator_data['distribute']

    try:
        plasmids = load_plasmids(operator_data, doc)
    except:
        plasmids = []

    for i in range(0, len(entity_data)):
        if i < len(plasmids):
            condition = load_condition(entity_data[i], doc, entity_dict, unit_dict, om, plasmids[i])
        else:
            condition = load_condition(entity_data[i], doc, entity_dict, unit_dict, om)

        try:
            load_src_dest_samples(entity_data[i], doc, entity_dict, condition)
        except:
            load_sample(entity_data[i], doc, entity_dict, condition)

def load_step_entities(step_data, doc, exp, attachs, entity_dict, unit_dict, om):
    operator_data = step_data['operator']

    try:
        load_experimental_data(operator_data, doc, exp, repr(step_data['id']), attachs, entity_dict)
    except:
        load_operator_entities(operator_data, doc, entity_dict, unit_dict, om)

def load_experiment(plan_data, doc):
    exp_id = load_alnum_id(plan_data['id'])

    return doc.create_experiment(exp_id, plan_data['name'])

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument('-hm', '--homespace')
    parser.add_argument('-op', '--om_path')
    parser.add_argument('-xp', '--xplan_path')
    parser.add_argument('-sp', '--sbol_path')
    parser.add_argument('-va', '--validate', action='store_true')
    args = parser.parse_args(args)

    doc = XDocument()

    doc.configure_options(args.homespace, args.validate, False)

    om = doc.read_om(args.om_path)

    plan_data = json.loads(open(args.xplan_path).read())

    exp = load_experiment(plan_data, doc)

    attachs = []

    entity_dict = {}
    unit_dict = {}
    
    for step_data in plan_data['steps']:
        load_step_entities(step_data, doc, exp, attachs, entity_dict, unit_dict, om)

    doc.add_top_levels([exp])
    doc.add_top_levels(attachs)
    # doc.add_top_levels(exp_data)
    doc.add_top_levels(list(entity_dict.values()))
    doc.add_top_levels(list(unit_dict.values()))
    
    act_dict = {}

    for step_data in plan_data['steps']:
        load_step_activities(step_data, doc, entity_dict, act_dict)

    doc.write(args.sbol_path)

    print('done')

if __name__ == '__main__':
    main()