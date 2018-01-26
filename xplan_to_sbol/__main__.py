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

        path = parsed_uri.path[1:].replace('/', '_').replace('-', '_').replace('.', '_')

        fragment = parsed_uri.fragment.replace('/', '_').replace('-', '_').replace('.', '_')

        if len(path) > 0 and len(fragment) > 0:
            return ''.join([path, '_', fragment])
        elif len(path) > 0:
            return path
        else:
            return fragment

def load_build_activity(src_sample_key, doc, operator, replicate_id, entity_dict, act_dict, act_name=None, act_desc=None, sample_measures=[], dest_sample_key=None, custom=[]):
    try:
        src_sample = act_dict[src_sample_key]
    except:
        src_sample = entity_dict[src_sample_key]

    if dest_sample_key is None:
            act_dict[src_sample_key] = doc.create_activity(operator, replicate_id, [src_sample], act_name, act_desc, custom)
    else:
        dest_sample = entity_dict[dest_sample_key]

        doc.add_measures(dest_sample, sample_measures)

        doc.create_activity(operator, replicate_id, [src_sample], act_name, act_desc, custom, dest_sample)

def load_src_dest_build_activity(sample_data, doc, operator, replicate_id, entity_dict, act_dict, act_name=None, act_desc=None, sample_measures=[]):
    src_sample_data = load_src_sample_data(sample_data)

    dest_sample_data = load_dest_sample_data(sample_data)

    if isinstance(src_sample_data, str) and isinstance(dest_sample_data, str):
        load_build_activity(src_sample_data, doc, operator, replicate_id, entity_dict, act_dict, act_name, act_desc, sample_measures, dest_sample_data)
    elif isinstance(src_sample_data, str):
        for dest_sample_datum in dest_sample_data:
            load_build_activity(src_sample_data, doc, operator, replicate_id, entity_dict, act_dict, act_name, act_desc, sample_measures, load_dest_sample_key(dest_sample_datum))
    elif isinstance(dest_sample_data, str):
        for src_entity_datum in src_sample_data:
            if isinstance(src_entity_datum, str):
                load_build_activity(src_entity_datum, doc, operator, replicate_id, entity_dict, act_dict, act_name, act_desc, sample_measures, dest_sample_data)
    else:
        for src_entity_datum in src_sample_data:
            if isinstance(src_entity_datum, str):
                for dest_sample_datum in dest_sample_data:
                    load_build_activity(src_entity_datum, doc, operator, replicate_id, entity_dict, act_dict, act_name, act_desc, sample_measures, load_dest_sample_key(dest_sample_datum))

def load_operator_activities(operator_data, doc, replicate_id, entity_dict, act_dict, unit_dict, om):
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
        sample_measures = load_sample_measures(sample_datum, doc, ['od600', 'volume'], unit_dict, om)

        try:
            load_src_dest_build_activity(sample_datum, doc, operator, replicate_id, entity_dict, act_dict, act_name, act_desc, sample_measures)
        except:
            load_build_activity(load_src_sample_key(sample_datum), doc, operator, replicate_id, entity_dict, act_dict, act_name, act_desc, sample_measures)

def load_channels(operator_data):
    channel_data = operator_data['channels']

    channels = []

    for channel_datum in channel_data:
        channel = {}
        channel['display_id'] = load_alnum_id(channel_datum.calibration_file)
        channel['calibration_file'] = channel_datum.calibration_file
        channel['name'] = channel_datum.name

    return channels

def load_upload_activity(operator_data, doc, replicate_id, entity_dict, act_dict):
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
            src_sample = entity_dict[src_sample_key]

        file_paths = load_file_paths(entity_datum)

        dest_entity = entity_dict[file_paths[0]]

        if len(channels) > 0:
            act_dict[src_sample_key] = doc.create_flow_cytometry_activity(operator, channels, replicate_id, [src_sample], act_name, act_desc, custom, dest_entity)
        else:
            act_dict[src_sample_key] = doc.create_activity(operator, replicate_id, [src_sample], act_name, act_desc, custom, dest_entity)

def load_step_activities(step_data, doc, entity_dict, act_dict, unit_dict, om):
    operator_data = step_data['operator']
    
    replicate_id = repr(step_data['id'])

    try:
        load_upload_activity(operator_data, doc, replicate_id, entity_dict, act_dict)
    except:
        load_operator_activities(operator_data, doc, replicate_id, entity_dict, act_dict, unit_dict, om)

def load_src_sample_key(sample_data):
    try:
        sample_key = sample_data['source']
    except:
        try:
            sample_key = sample_data['sample']
        except:
            sample_key = sample_data

    return sample_key

def load_dest_sample_key(sample_data):
    try:
        sample_key = sample_data['dest']
    except:
        sample_key = sample_data

    return sample_key

def load_sample(sample_key, doc, entity_dict, condition=None, src_samples=[]):
    sample_id = load_alnum_id(sample_key)

    if sample_key not in entity_dict:
        entity_dict[sample_key] = doc.create_sample(sample_id, condition, src_samples)
    
    return entity_dict[sample_key]

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

def load_src_samples(sample_data, doc, entity_dict):
    src_samples = []

    src_sample_data = load_src_sample_data(sample_data)

    if isinstance(src_sample_data, str):
        src_samples.append(load_sample(src_sample_data, doc, entity_dict))
    else:
        for src_sample_datum in src_sample_data:
            if isinstance(src_sample_datum, str):
                src_samples.append(load_sample(src_sample_datum, doc, entity_dict))

    return src_samples

def load_dest_samples(sample_data, doc, entity_dict, src_samples, condition=None):
    dest_sample_data = load_dest_sample_data(sample_data)

    if isinstance(dest_sample_data, str):
        load_sample(dest_sample_data, doc, entity_dict, condition, src_samples)
    else:
        for dest_sample_datum in dest_sample_data:
            load_sample(load_dest_sample_key(dest_sample_datum), doc, entity_dict, condition, src_samples)
        
def load_src_dest_samples(sample_data, doc, entity_dict, condition=None):
    src_samples = load_src_samples(sample_data, doc, entity_dict)

    load_dest_samples(sample_data, doc, entity_dict, src_samples, condition)

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

def load_unit(entity_data, doc, unit_dict, om):
    try:
        symbol = entity_data['units']

        if symbol not in unit_dict:
            unit_dict[symbol] = doc.create_unit(om, symbol)

        return unit_dict[symbol]
    except:
        name = entity_data.split(':')[1]

        if name not in unit_dict:
            unit_dict[name] = doc.create_unit(om=om, name=name)

        return unit_dict[name]

def load_inducers(condition_data, doc, unit_dict, om, measures):
    inducer_data = condition_data['inducer']

    try:
        unit = load_unit(inducer_data, doc, unit_dict, om)
        measures.append({'mag': repr(inducer_data['amount']), 'unit': unit})
    except:
        measures.append({'mag': repr(inducer_data['amount'])})

    inducer_id = load_alnum_id(inducer_data['compound'])

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

    sub_systems = []
    try:
        src_samples = load_src_samples(condition_data, doc, entity_dict)

        for src_sample in src_samples:
            for sub_system in doc.get_systems(src_sample.built):
                sub_systems.append(sub_system)
    except:
        pass

    measures = []

    try:
        inputs = load_inducers(condition_data, doc, unit_dict, om, measures)
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

def load_experimental_data(operator_data, doc, exp, replicate_id, attachs, entity_dict):
    operator = operator_data['type'].replace('-', '_')

    if operator == 'uploadData':
        entity_data = operator_data['samples']
    else:
        entity_data = load_measurement_data(operator_data)

    for entity_datum in entity_data:
        sample = load_sample(load_src_sample_key(entity_datum), doc, entity_dict)

        file_paths = load_file_paths(entity_datum)

        temp_attachs = []

        for file_path in file_paths:
            attach_id = load_alnum_id(file_path)

            temp_attachs.append(doc.create_attachment(attach_id, attach_id, file_path, replicate_id))

        exp_data = doc.create_experimental_data(temp_attachs, sample, exp, operator, replicate_id)

        if exp_data.identity.get() not in entity_dict:
            entity_dict[file_paths[0]] = exp_data

            for attach in temp_attachs:
                attachs.append

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

def load_sample_measures(sample_data, doc, measure_ids, unit_dict, om):
    measures = []

    for measure_id in measure_ids:
        try:
            measure_data = sample_data[measure_id]

            if isinstance(measure_data, str):
                mag = measure_data.split(':')[0]
                try:
                    unit = load_unit(measure_data, doc, unit_dict, om)
                    measures.append({'id': measure_id, 'mag': mag, 'unit': unit})
                except:
                    measures.append({'id': measure_id, 'mag': mag})
            else:
                measures.append({'id': measure_id, 'mag': repr(measure_data)})
        except:
            pass

    return measures

def load_operator_samples(operator_data, doc, entity_dict, unit_dict, om):
    sample_data = load_sample_data(operator_data)

    try:
        plasmids = load_plasmids(operator_data, doc)
    except:
        plasmids = []

    for i in range(0, len(sample_data)):
        if i < len(plasmids):
            condition = load_condition(sample_data[i], doc, entity_dict, unit_dict, om, plasmids[i])
        else:
            condition = load_condition(sample_data[i], doc, entity_dict, unit_dict, om)

        try:
            load_src_dest_samples(sample_data[i], doc, entity_dict, condition)
        except:
            load_sample(load_src_sample_key(sample_data[i]), doc, entity_dict, condition)

def load_step_entities(step_data, doc, exp, attachs, entity_dict, unit_dict, om):
    operator_data = step_data['operator']

    try:
        load_experimental_data(operator_data, doc, exp, repr(step_data['id']), attachs, entity_dict)
    except:
        load_operator_samples(operator_data, doc, entity_dict, unit_dict, om)

def load_experiment(plan_data, doc):
    exp_id = load_alnum_id(plan_data['id'])

    return doc.create_experiment(exp_id, plan_data['name'])

def convert_xplan_to_sbol(homespace, om_path, xplan_path, sbol_path, validate):
    doc = XDocument()

    doc.configure_options(homespace, validate, False)

    om = doc.read_om(om_path)

    plan_data = json.loads(open(xplan_path).read())

    exp = load_experiment(plan_data, doc)

    attachs = []

    entity_dict = {}
    unit_dict = {}
    
    for step_data in plan_data['steps']:
        load_step_entities(step_data, doc, exp, attachs, entity_dict, unit_dict, om)

    doc.add_top_levels([exp])
    doc.add_top_levels(attachs)
    doc.add_top_levels(list(entity_dict.values()))
    doc.add_top_levels(list(unit_dict.values()))
    
    act_dict = {}

    for step_data in plan_data['steps']:
        load_step_activities(step_data, doc, entity_dict, act_dict, unit_dict, om)

    doc.add_top_levels(list(unit_dict.values()))

    doc.write(sbol_path)

    print('done')

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

    convert_xplan_to_sbol(args.homespace, args.om_path, args.xplan_path, args.sbol_path, args.validate)

if __name__ == '__main__':
    main()