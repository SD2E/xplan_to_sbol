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

        if parsed_uri.hostname == 'hub.sd2e.org':
            return parsed_uri.path.split('/')[-2]
        else:
            path = parsed_uri.path[1:].replace('/', '_').replace('-', '_').replace('.', '_')

            fragment = parsed_uri.fragment.replace('/', '_').replace('-', '_').replace('.', '_')

            if len(path) > 0 and len(fragment) > 0:
                return ''.join([path, '_', fragment])
            elif len(path) > 0:
                return path
            else:
                return fragment

def load_build_activity(src_entity_keys, doc, operator, act_dict, act_name=None, act_desc=None, dest_sample_key=None, custom=[]):
    src_entities = []

    temp_act_dict = {}

    for src_entity_key in src_entity_keys:
        if isinstance(src_entity_key, str):
            try:
                if src_entity_key not in temp_act_dict:
                    src_entities.append(act_dict[src_entity_key])
                    temp_act_dict[src_entity_key] = src_entities[-1]
            except:
                src_entities.append(load_sample(src_entity_key, doc))

    if dest_sample_key is None:
            act = doc.create_activity(operator, src_entities, act_name, act_desc, custom)

            act_dict[src_entity_key] = act
    else:
        dest_sample = load_sample(dest_sample_key, doc)

        act = doc.create_activity(operator, src_entities, act_name, act_desc, custom, dest_sample)

def load_src_dest_build_activity(sample_data, doc, operator, act_dict, act_name=None, act_desc=None):
    src_sample_data = load_src_sample_data(sample_data)

    dest_sample_data = load_dest_sample_data(sample_data)

    if isinstance(src_sample_data, str) and isinstance(dest_sample_data, str):
        load_build_activity([src_sample_data], doc, operator, act_dict, act_name, act_desc, dest_sample_data)
    elif isinstance(src_sample_data, str):
        for dest_sample_datum in dest_sample_data:
            load_build_activity([src_sample_data], doc, operator, act_dict, act_name, act_desc, load_dest_sample_key(dest_sample_datum))
    elif isinstance(dest_sample_data, str):
        load_build_activity(src_sample_data, doc, operator, act_dict, act_name, act_desc, dest_sample_data)
    else:
        for dest_sample_datum in dest_sample_data:
            load_build_activity(src_sample_data, doc, operator, act_dict, act_name, act_desc, load_dest_sample_key(dest_sample_datum))

def load_operator_activities(operator_data, doc, act_dict, om):
    operator = operator_data['type'].replace('-', '_')

    try:
        act_name = operator_data['name']
    except:
        act_name = None
    try:
        act_desc = operator_data['description']
    except:
        act_desc = None

    sample_data = load_sample_data(operator_data)

    for sample_datum in sample_data:
        try:
            load_src_dest_build_activity(sample_datum, doc, operator, act_dict, act_name, act_desc)
        except:
            load_build_activity([load_src_sample_key(sample_datum)], doc, operator, act_dict, act_name, act_desc)

def load_channels(operator_data):
    channel_data = operator_data['channels']

    channels = []

    for channel_datum in channel_data:
        channel = {}
        channel['display_id'] = load_alnum_id(channel_datum.calibration_file)
        channel['calibration_file'] = channel_datum.calibration_file
        channel['name'] = channel_datum.name

    return channels

def load_upload_activity(operator_data, doc, exp_data_dict, act_dict):
    operator = operator_data['type'].replace('-', '_')

    if operator == 'uploadData':
        entity_data = operator_data['samples']
    else:
        entity_data = load_measurement_data(operator_data)

    try:
        act_name = operator_data['name']
    except:
        act_name = None
    try:
        act_desc = operator_data['description']
    except:
        act_desc = None

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

    try:
        channels = load_channels(operator_data)
    except:
        channels = []

    for entity_datum in entity_data:
        src_sample_key = load_src_sample_key(entity_datum)

        try:
            src_sample = act_dict[src_sample_key]
        except:
            src_sample = load_sample(src_sample_key, doc)

        dest_exp_data = exp_data_dict[repr(load_file_paths(entity_datum))]

        if len(channels) > 0:
            act_dict[src_sample_key] = doc.create_flow_cytometry_activity(operator, channels, [src_sample], act_name, act_desc, custom, dest_exp_data)
        else:
            act_dict[src_sample_key] = doc.create_activity(operator, [src_sample], act_name, act_desc, custom, dest_exp_data)

def load_step_activities(step_data, doc, exp_data_dict, act_dict, om):
    operator_data = step_data['operator']

    try:
        load_upload_activity(operator_data, doc, exp_data_dict, act_dict)
    except:
        load_operator_activities(operator_data, doc, act_dict, om)

def load_src_sample_key(sample_data):
    try:
        sample_key = sample_data['source']
    except:
        try:
            sample_key = sample_data['sample']
        except:
            sample_key = sample_data

    return sample_key.replace('https', 'http')

def load_dest_sample_key(sample_data):
    try:
        sample_key = sample_data['dest']
    except:
        sample_key = sample_data

    return sample_key.replace('https', 'http')

def load_sample(sample_key, doc, condition=None, src_samples=[], measures=[]):
    sample_id = load_alnum_id(sample_key)

    return doc.create_sample(sample_id, condition, src_samples, measures)

def load_src_sample_data(sample_data):
    try:
        src_sample_data = sample_data['sources']
    except:
        try:
            src_sample_data = sample_data['source']
        except:
            try:
                src_sample_data = sample_data['sample']['source']
            except:
                try:
                    src_sample_data = sample_data['resource']
                except:
                    src_sample_data = sample_data['src']

    return src_sample_data

def load_dest_sample_data(sample_data):
    try:
        dest_sample_data = sample_data['destinations']
    except:
        try:
            dest_sample_data = sample_data['destination']
        except:
            try:
                dest_sample_data = sample_data['sample']['destination']
            except:
                try:
                    src_sample_data = sample_data['resource']
                    dest_sample_data = sample_data['sample']
                except:
                    try:
                        dest_sample_data = sample_data['dests']
                    except:
                        dest_sample_data = sample_data['dest'] 

    return dest_sample_data

def load_src_samples(sample_data, doc):
    src_samples = []

    src_sample_data = load_src_sample_data(sample_data)

    if isinstance(src_sample_data, str):
        src_samples.append(load_sample(src_sample_data, doc))
    else:
        for src_sample_datum in src_sample_data:
            if isinstance(src_sample_datum, str):
                src_samples.append(load_sample(src_sample_datum, doc))

    return src_samples

def load_dest_samples(sample_data, doc, src_samples, condition=None, measures=[]):
    dest_sample_data = load_dest_sample_data(sample_data)

    if isinstance(dest_sample_data, str):
        load_sample(dest_sample_data, doc, condition, src_samples, measures)
    else:
        for dest_sample_datum in dest_sample_data:
            load_sample(load_dest_sample_key(dest_sample_datum), doc, condition, src_samples, measures)
        
def load_src_dest_samples(sample_data, doc, condition=None, measures=[]):
    src_samples = load_src_samples(sample_data, doc)

    load_dest_samples(sample_data, doc, src_samples, condition, measures)

def load_strains(condition_data, doc):
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

def load_unit(entity_data, doc, om):
    try:
        return doc.create_unit(om, entity_data['units'])
    except:
        name = entity_data.split(':')[1]

        return doc.create_unit(om=om, name=name)

def load_inducers(condition_data, doc, om, measures):
    inducer_data = condition_data['inducer']

    inducer_id = load_alnum_id(inducer_data['compound'])

    try:
        unit = load_unit(inducer_data, doc, om)
        measures[inducer_id] = {'id': None, 'mag': float(inducer_data['amount']), 'unit': unit}
    except:
        measures[inducer_id] = {'id': None, 'mag': float(inducer_data['amount']), 'unit': None}

    return [doc.create_inducer(inducer_id, inducer_id)]

def load_condition(condition_data, doc, om, plasmid=None):
    try:
        devices = load_strains(condition_data, doc)
    except:
        devices = []

    if plasmid is not None:
        if isinstance(plasmid, str):
            devices.append(plasmid)
        else:
            for plasm in plasmid:
                devices.append(plasm)

    sub_systems = []
    try:
        src_samples = load_src_samples(condition_data, doc)

        for src_sample in src_samples:
            for sub_system in doc.get_systems(src_sample.built):
                sub_systems.append(sub_system)
    except:
        pass

    measures = {}
    try:
        inputs = load_inducers(condition_data, doc, om, measures)
    except:
        inputs = []

    if len(sub_systems) == 1 and len(devices) == 0 and len(inputs) == 0:
        return sub_systems[0]
    elif len(devices) > 0 or len(sub_systems) > 1 or len(inputs) > 0:
        return doc.create_system(devices, sub_systems, inputs, measures)
    else:
        return None

def load_file_paths(entity_data):
    try:
        file_paths = entity_data['files']
    except:
        try:
            file_paths = entity_data['uris']
        except:
            try:
                file_paths = entity_data['file']
            except:
                try:
                    file_paths = entity_data['uri']
                except:
                    file_paths = entity_data['dest']

    if isinstance(file_paths, str):
        return [file_paths]
    else:
        return file_paths

def load_measurement_data(operator_data):
    try:
        measure_data = operator_data['measurements']
    except:
        measure_data = operator_data['measure']

    return measure_data

def load_experimental_data(operator_data, doc, replicate_id, exp, exp_data_dict):
    operator = operator_data['type'].replace('-', '_')

    if operator == 'uploadData':
        entity_data = operator_data['samples']
    else:
        entity_data = load_measurement_data(operator_data)

    for entity_datum in entity_data:
        sample = load_sample(load_src_sample_key(entity_datum), doc)

        file_paths = load_file_paths(entity_datum)

        attachs = []

        for file_path in file_paths:
            attach_id = load_alnum_id(file_path)

            attachs.append(doc.create_attachment(display_id=attach_id, source=file_path, name=attach_id))

        file_key = repr(file_paths)

        if file_key not in exp_data_dict:
            exp_data_dict[file_key] = doc.create_experimental_data(attachs, sample, exp, operator, replicate_id)

def load_sample_data(operator_data):
    try:
        entity_data = operator_data['transformations']
    except:
        try:
            entity_data = operator_data['samples']
        except:
            try:
                entity_data = operator_data['transfer']
            except:
                try:
                    entity_data = operator_data['distribute']
                except:
                    entity_data = operator_data['transform']

    return entity_data

def load_sample_measures(sample_data, doc, measure_ids, om):
    measures = []

    for measure_id in measure_ids:
        try:
            measure_data = sample_data[measure_id]

            if isinstance(measure_data, str):
                mag = measure_data.split(':')[0]
                try:
                    unit = load_unit(measure_data, doc, om)
                    measures.append({'id': measure_id, 'mag': float(mag), 'unit': unit})
                except:
                    measures.append({'id': measure_id, 'mag': float(mag), 'unit': None})
            else:
                measures.append({'id': measure_id, 'mag': measure_data, 'unit': None})
        except:
            pass

    return measures

def load_operator_samples(operator_data, doc, om):
    sample_data = load_sample_data(operator_data)

    try:
        plasmids = load_plasmids(operator_data, doc)
    except:
        plasmids = []

    for i in range(0, len(sample_data)):
        if i < len(plasmids):
            condition = load_condition(sample_data[i], doc, om, plasmids[i])
        else:
            condition = load_condition(sample_data[i], doc, om)

        measures = load_sample_measures(sample_data[i], doc, ['od600', 'volume'], om)

        try:
            load_src_dest_samples(sample_data[i], doc, condition, measures)
        except:
            load_sample(load_src_sample_key(sample_data[i]), doc, condition)

def load_step_entities(step_data, doc, exp, exp_data_dict, om):
    operator_data = step_data['operator']

    try:
        load_experimental_data(operator_data, doc, repr(step_data['id']), exp, exp_data_dict)
    except:
        load_operator_samples(operator_data, doc, om)

def load_experiment(plan_data, doc):
    exp_id = load_alnum_id(plan_data['id'])

    return doc.create_experiment(exp_id, plan_data['name'])

# def load_experiment_collection(plan_data, prob_doc, exp_doc):
#     exp_collect_id = load_alnum_id(plan_data['id'])

#     return prob_doc.create_collection(exp_collect_id, plan_data['name'])

def convert_xplan_to_sbol(plan_data, exp_space, om_path, validate):
    exp_doc = XDocument()

    om = exp_doc.read_om(om_path)

    exp_data_dict = {}

    exp_doc.configure_options(exp_space, validate, False)

    exp = load_experiment(plan_data, exp_doc)

    for step_data in plan_data['steps']:
        load_step_entities(step_data, exp_doc, exp, exp_data_dict, om)
    
    act_dict = {}

    for step_data in plan_data['steps']:
        load_step_activities(step_data, exp_doc, exp_data_dict, act_dict, om)

    return exp_doc

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument('-xp', '--xplan_path')
    parser.add_argument('-es', '--exp_space')
    parser.add_argument('-op', '--om_path')
    parser.add_argument('-va', '--validate', action='store_true')
    parser.add_argument('-ep', '--exp_path', nargs='?', default=None)
    parser.add_argument('-ds', '--design_space', nargs='?', default=None)
    parser.add_argument('-dp', '--design_path', nargs='?', default=None)
    parser.add_argument('-su', '--sbh_url', nargs='?', default=None)
    parser.add_argument('-se', '--sbh_email', nargs='?', default=None)
    parser.add_argument('-sp', '--sbh_password', nargs='?', default=None)
    
    args = parser.parse_args(args)

    with open(args.xplan_path) as plan_file:
        plan_data = json.load(plan_file)

        exp_doc = convert_xplan_to_sbol(plan_data, args.exp_space, args.om_path, args.validate)

        if args.exp_path is not None:
            exp_doc.write(args.exp_path)

        if args.sbh_url is not None and args.sbh_email is not None and args.sbh_password is not None:
            exp_doc.upload(args.sbh_url, args.sbh_email, args.sbh_password)

    print('done')

if __name__ == '__main__':
    main()