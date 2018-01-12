import argparse
import json
import sys
from pySBOLx.pySBOLx import XDocument

def load_activity(src_entity_data, doc, operator, replicate_id, entity_dict, act_dict, dest_entity_data=None):
    try:
        src_entity_id = src_entity_data['sample']
    except:
        src_entity_id = src_entity_data

    try:
        src_entity = act_dict[src_entity_id]
    except:
        src_entity = entity_dict[src_entity_id]

    if dest_entity_data is None:
        act_dict[src_entity_id] = doc.create_activity(operator, replicate_id, [src_entity])
    else:
        try:
            dest_entity_id = dest_entity_data['dest']
        except:
            dest_entity_id = dest_entity_data
        
        dest_entity = entity_dict[dest_entity_id]

        doc.create_activity(operator, replicate_id, [src_entity], dest_entity)

def load_src_dest_activity(entity_data, doc, operator, replicate_id, entity_dict, act_dict):
    src_entity_data = entity_data['src']

    try:
        dest_entity_data = entity_data['dest']

        if isinstance(dest_entity_data, str):
            load_activity(src_entity_data, doc, operator, replicate_id, entity_dict, act_dict, dest_entity_data)
        else:
            for dest_entity_datum in dest_entity_data:
                load_activity(src_entity_data, doc, operator, replicate_id, entity_dict, act_dict, dest_entity_datum)
    except:
        dest_entity_data = entity_data['dests']

        for dest_entity_datum in dest_entity_data:
            load_activity(src_entity_data, doc, operator, replicate_id, entity_dict, act_dict, dest_entity_datum)

def load_step_activities(step_data, doc, entity_dict, act_dict):
    operator = step_data['operator']['type'].replace('-', '_')
    replicate_id = repr(step_data['id'])

    for entity_data in step_data['operator']['samples']:
        if operator == 'uploadData':
            load_activity(entity_data, doc, operator, replicate_id, entity_dict, act_dict, entity_data)
        else:
            try:
                load_src_dest_activity(entity_data, doc, operator, replicate_id, entity_dict, act_dict)
            except:
                load_activity(entity_data, doc, operator, replicate_id, entity_dict, act_dict)

def load_sample(sample_data, doc, entity_dict, src_samples=[], strain_condition=None, induction_condition=None):
    try:
        sample_id = sample_data['sample']
    except:
        sample_id = sample_data

    if sample_id not in entity_dict:
        if strain_condition is None:
            system_uris = []

            for src_sample in src_samples:
                if len(src_sample.built) == 1:
                    for built_uri in src_sample.built:
                        system_uris.append(built_uri)

            systems = doc.get_systems(system_uris)

            if induction_condition is None:
                if len(systems) > 1:
                    condition = doc.create_system(sub_systems=systems)
                elif len(systems) > 0:
                    condition = systems[0]
                else:
                    condition = None
            else:
                condition = doc.copy_inducible_system(system=induction_condition, sub_systems=systems)
        elif induction_condition is None:
            condition = strain_condition
        else:
            condition = induction_condition

        entity_dict[sample_id] = doc.create_sample(sample_id.replace('-', '_'), src_samples, condition)
    
    return entity_dict[sample_id]

def load_src_dest_samples(sample_data, doc, entity_dict, strain_condition=None, induction_condition=None):
    src_sample_data = sample_data['src']
    
    src_sample = load_sample(src_sample_data, doc, entity_dict)

    try:
        dest_sample_data = sample_data['dest']

        if isinstance(dest_sample_data, str):
            load_sample(dest_sample_data, doc, entity_dict, [src_sample], strain_condition, induction_condition)
        else:
            for dest_sample_datum in dest_sample_data:
                load_sample(dest_sample_datum, doc, entity_dict, [src_sample], strain_condition, induction_condition)
    except:
        dest_sample_data = sample_data['dests']

        for dest_sample_datum in dest_sample_data:
            load_sample(dest_sample_datum['dest'], doc, entity_dict, [src_sample], strain_condition, induction_condition)

def load_experimental_data(source, doc, sample, exp, operator, replicate_id, attachs, entity_dict):
    if source not in entity_dict:
        attachs.append(doc.create_attachment(source=source, replicate_id=replicate_id))

        entity_dict[source] = doc.create_experimental_data([attachs[-1]], sample, exp, operator, replicate_id)
    
    return entity_dict[source]

def load_entities(entity_data, doc, exp, operator, replicate_id, attachs, entity_dict, strain_condition=None, induction_condition=None):
    if operator == 'uploadData':
        sample = load_sample(sample_data=entity_data, doc=doc, entity_dict=entity_dict, strain_condition=strain_condition, induction_condition=induction_condition)

        load_experimental_data(entity_data['dest'], doc, sample, exp, operator, replicate_id, attachs, entity_dict)
    else:
        try:
            load_src_dest_samples(entity_data, doc, entity_dict, strain_condition, induction_condition)
        except:
            load_sample(sample_data=entity_data, doc=doc, entity_dict=entity_dict, strain_condition=strain_condition, induction_condition=induction_condition)

def load_inducer(inducer_data, doc, unit_dict, om, mags, units):
    mags.append(repr(inducer_data['amount']))

    symbol = inducer_data['units']

    if symbol not in unit_dict:
        unit_dict[symbol] = doc.create_unit(symbol, om)

    units.append(unit_dict[symbol])

    inducer_id = inducer_data['compound'].replace('-', '_')

    return doc.create_inducer(inducer_id, inducer_id)

def load_induction_condition(sample_data, doc, unit_dict, om, strain_condition=None):
    inducers = []
    mags = []
    units = []

    inducers.append(load_inducer(sample_data['inducer'], doc, unit_dict, om, mags, units))

    if strain_condition is None:
        return doc.create_system(inputs=inducers, mags=mags, units=units)
    else:
        return doc.create_system(sub_systems=[strain_condition], inputs=inducers, mags=mags, units=units)

def load_plasmids(plasmid_data, doc):
    plasmids = []

    if isinstance(plasmid_data, str):
        plasmid_id = plasmid_data.replace('-', '_')

        plasmids.append(doc.create_plasmid(plasmid_id, plasmid_id))
    else:
        for plasmid_datum in plasmid_data:
            plasmid_id = plasmid_datum.replace('-', '_')

            plasmids.append(doc.create_plasmid(plasmid_id, plasmid_id))

    return plasmids

def load_strain_condition(sample_data, doc):
    devices = []

    try:
        strain_id = sample_data['strain'].replace('-', '_')

        devices.append(doc.create_strain(strain_id, strain_id))
    except:
        devices.append(load_plasmids(sample_data['plasmids'], doc))

    return doc.create_system(devices)

def load_entities_and_conditions(entity_data, doc, exp, operator, replicate_id, attachs, entity_dict, unit_dict, om):
    try:
        strain_condition = load_strain_condition(entity_data, doc)

        try:
            induction_condition = load_induction_condition(entity_data, doc, unit_dict, om, strain_condition)

            load_entities(entity_data, doc, exp, operator, replicate_id, attachs, entity_dict, strain_condition, induction_condition)
        except:
            load_entities(entity_data, doc, exp, operator, replicate_id, attachs, entity_dict, strain_condition)
    except:
        try:
            induction_condition = load_induction_condition(entity_data, doc, unit_dict, om)

            load_entities(entity_data=entity_data, doc=doc, exp=exp, operator=operator, replicate_id=replicate_id, attachs=attachs, entity_dict=entity_dict, induction_condition=induction_condition)
        except:
            load_entities(entity_data, doc, exp, operator, replicate_id, attachs, entity_dict)
    
def load_step_entities(step_data, doc, exp, attachs, entity_dict, unit_dict, om):
    operator = step_data['operator']['type'].replace('-', '_')
    replicate_id = repr(step_data['id'])

    for entity_data in step_data['operator']['samples']:
        load_entities_and_conditions(entity_data, doc, exp, operator, replicate_id, attachs, entity_dict, unit_dict, om)

def load_experiment(plan_data, doc):
    exp_id = plan_data['id'].replace('-', '_')

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