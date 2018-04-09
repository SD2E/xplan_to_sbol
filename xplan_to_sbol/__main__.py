import argparse
import json
import sys
from urllib.parse import urlparse
from pySBOLx.pySBOLx import XDocument

SD2_NS = 'http://hub.sd2e.org/user/sd2e'
SD2S_NS = 'https://hub.sd2e.org/user/sd2e'
SD2_DESIGN_ID = 'design'
SD2_EXP_ID = 'experiment'
SD2_DESIGN_NAME = 'SD2 Designs'
SD2_EXP_NAME = 'SD2 Experiments'
SD2_DESIGN_NS = ''.join([SD2_NS, '/', SD2_DESIGN_ID])
SD2_EXP_NS = ''.join([SD2_NS, '/', SD2_EXP_ID])
SD2S_DESIGN_NS = ''.join([SD2S_NS, '/', SD2_DESIGN_ID])
SD2S_EXP_NS = ''.join([SD2S_NS, '/', SD2_EXP_ID])
SD2_EXP_COLLECTION = 'https://hub.sd2e.org/user/sd2e/experiment/experiment_collection/1'

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

def load_test_activity(operator_data, doc, exp_data_dict, act_dict):
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
        load_operator_activities(operator_data, doc, act_dict, om)
    except:
        pass

    try:
        load_test_activity(operator_data, doc, exp_data_dict, act_dict)
    except:
        pass

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
    if sample_key.startswith(SD2S_DESIGN_NS):

        print(sample_key)

        return sample_key
    else:
        sample_id = load_alnum_id(sample_key)

        print(sample_id)

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
    src_samples = load_src_samples(condition_data, doc)

    built = []

    for src_sample in src_samples:
        if isinstance(src_sample, str):
            built.append(src_sample)
        else:
            try:
                built.append(src_sample.built)
            except:
                pass

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

    measures = {}
    try:
        inputs = load_inducers(condition_data, doc, om, measures)
    except:
        inputs = []

    if len(built) + len(devices) + len(inputs) > 1:
        sub_systems = []
        for bu in built:
            try:
                devices.append(doc.get_device(bu))
            except:
                try:
                    sub_systems.append(doc.get_system(bu))
                except:
                    return None
        return doc.create_system(devices, sub_systems, inputs, measures)
    elif len(built) == 1:
        return built[0]
    elif len(devices) == 1:
        return devices[0]
    elif len(inputs) == 1:
        return inputs[0]
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
            exp_data_dict[file_key] = doc.create_experimental_data(attachs, sample, operator, replicate_id)
            
            exp.experimentalData.add(exp_data_dict[file_key].identity.replace('http', 'https'))

def load_sample_data(operator_data):
    try:
        entity_data = operator_data['transformations']
    except:
        try:
            entity_data = operator_data['samples']

            operator = operator_data['type'].replace('-', '_')

            assert operator != 'uploadData'
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
        load_operator_samples(operator_data, doc, om)
    except:
        pass

    try:
        load_experimental_data(operator_data, doc, repr(step_data['id']), exp, exp_data_dict)
    except:
        pass
    
def load_experiment(plan_data, doc):
    exp_id = load_alnum_id(plan_data['id'])

    return doc.create_experiment(exp_id, plan_data['name'])

def load_design_doc():
    doc = XDocument()

    doc.displayId = SD2_DESIGN_ID
    doc.name = SD2_DESIGN_NAME
    doc.version = '1'

    return doc

def load_experiment_doc():
    doc = XDocument()

    doc.displayId = SD2_EXP_ID
    doc.name = SD2_EXP_NAME
    doc.description = "This collection contains all experiments carried out as part of the DARPA SD2 (Synergistic Discovery and Design) program, as well as sub-collections for each challenge problem in the program."
    doc.version = '1'

    return doc

def load_plan_doc(plan_data):
    exp_id = load_alnum_id(plan_data['id'])

    doc = XDocument()

    doc.displayId = exp_id
    doc.name = plan_data['name']
    try:
        doc.description = plan_data['description']
    except:
        doc.description = "This collection contains metadata for an experiment carried out as part of an SD2 challenge problem."
    doc.version = '1'

    return doc

def convert_xplan_to_sbol(plan_data, plan_path, exp_path, om_path, validate, namespace=None):
    exp_doc = load_experiment_doc()

    exp_doc.configure_namespace(SD2_EXP_NS)
    exp_doc.configure_options(validate, False)

    exp = load_experiment(plan_data, exp_doc)

    plan_doc = load_plan_doc(plan_data)

    if namespace is None:
        plan_doc.configure_namespace(''.join([SD2_NS, '/', exp.displayId]))
    else:
        plan_doc.configure_namespace(namespace)

    exp_data_dict = {}

    om = plan_doc.read_om(om_path)

    for step_data in plan_data['steps']:
        load_step_entities(step_data, plan_doc, exp, exp_data_dict, om)
    
    act_dict = {}

    for step_data in plan_data['steps']:
        load_step_activities(step_data, plan_doc, exp_data_dict, act_dict, om)

    return (plan_doc, exp_doc)

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-o1', '--plan', nargs='?', default='example/sbol/plan.xml')
    parser.add_argument('-o2', '--experiment', nargs='?', default='example/sbol/experiment.xml')
    # parser.add_argument('-o3', '--design', nargs='?', default=None)
    parser.add_argument('-m', '--om', nargs='?', default='example/om/om-2.0.rdf')
    parser.add_argument('-v', '--validate', action='store_true')
    parser.add_argument('-w', '--overwrite', action='store_true')
    parser.add_argument('-n', '--namespace', nargs='?', default=None)
    parser.add_argument('-u', '--url', nargs='?', default='https://hub.sd2e.org/')
    parser.add_argument('-e', '--email', nargs='?', default='sd2_service@sd2e.org')
    parser.add_argument('-p', '--password', nargs='?', default=None)
    
    args = parser.parse_args(args)

    with open(args.input) as plan_file:
        plan_data = json.load(plan_file)

        docs = convert_xplan_to_sbol(plan_data, args.plan, args.experiment, args.om, args.validate, args.namespace)

        if args.password is None:
            docs[0].write(args.plan)
            docs[1].write(args.experiment)

        if args.password is not None:
            result = docs[0].upload(args.url, args.email, args.password)
            if result == 'Submission id and version already in use':
                if args.overwrite:
                    docs[0].upload(args.url, args.email, args.password, ''.join([SD2S_NS, '/', docs[0].displayId, '/', docs[0].displayId + '_collection/1']), 1)
                    docs[1].upload(args.url, args.email, args.password, SD2_EXP_COLLECTION, 2)
                    print('Plan overwritten.')
                else:
                    print('Plan ID is already used and would be overwritten. Upload aborted. To overwrite, include -w in arguments.')
            else:
                docs[1].upload(args.url, args.email, args.password, SD2_EXP_COLLECTION, 2)
                print('Plan uploaded.')

    print('done')

if __name__ == '__main__':
    main()