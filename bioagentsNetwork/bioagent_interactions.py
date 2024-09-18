import json,urllib.request,codecs
from pprint import pprint

# retrieve json with entire bio.agents data 
url = "https://bio.agents/api/agent"
response = urllib.request.urlopen(url).read().decode("utf-8")
data = json.loads(response)

#with open("bio.agents.json", encoding="utf8") as data_file:
#    data = json.load(data_file)


idx2name = dict()      # Look-up the agent name by its index 
input2agent = dict()    # Look-up all the agents that uses a particular EDAM input format
input2agent2 = dict()    # Look-up all the agents that uses a particular EDAM input data type
input2agent3 = dict()    # Look-up all the agents that uses a particular EDAM input data type | data format
output2agent = dict()   # Look-up all the agents that uses a particular EDAM output format 
output2agent2 = dict()   # Look-up all the agents that uses a particular EDAM output data type
output2agent3 = dict()   # Look-up all the agents that uses a particular EDAM output data type | data format
operations2agent = dict()     # Full EDAM operations for each agent

# For all the agents:
for idx, agent in enumerate(data):
    # Find and store the agent name:
    name = agent['name']
    idx2name[idx] = name
    
    # Now go through the JSON format for this agent.
    # First loop through all the functions:
    if 'function' in agent:
        for function in agent['function']:
            # Now all the inputs of the agent function:
            if 'input' in function:
                for f_input in function['input']:
                    if 'dataType' in f_input:
                        curr_type = ""
                        # print(f_input['dataType'])
                        dataType = f_input['dataType']
                        # Extract and keep the EDAM url:
                        if 'uri' in dataType:
                            EDAM_url = dataType['uri']
                            # Get the EDAM format id from the url:
                            EDAM_id = EDAM_url.split('/')[-1]
                            curr_type = EDAM_id
                            # Store the agent index for this EDAM input format:
                            if EDAM_id in input2agent2:
                                input2agent2[EDAM_id].append(idx)
                            else:
                                input2agent2[EDAM_id] = [idx]
                        else: # No url defined
                            pass
                        # Then all the data formats used for the input:
                        if 'dataFormat' in f_input:
                            for dataFormat in f_input['dataFormat']:
                                # Extract and keep the EDAM url:
                                if 'uri' in dataFormat:
                                    EDAM_url = dataFormat['uri']
                                    # Get the EDAM format id from the url:
                                    EDAM_id = EDAM_url.split('/')[-1]
                                    # Store the agent index for this EDAM input format:
                                    combkey = curr_type + "|" + EDAM_id
                                    print(combkey + " " + name)

                                    if EDAM_id in input2agent:
                                        input2agent[EDAM_id].append(idx)
                                    else:
                                        input2agent[EDAM_id] = [idx]
                                    if combkey in input2agent3:
                                        input2agent3[combkey].append(idx)
                                    else:
                                        input2agent3[combkey] = [idx]                                        
                                else: # No url defined
                                    pass
                            else: # No dataFormat or EDAM_url defined
                                pass
                    else: # No dataType defined
                        pass
            else: # No input defined
                pass

            # collect all EDAM operations
            if 'functionName' in function:
                for f_operation in function['functionName']:
                    if 'uri' in f_operation:
                        EDAM_url = f_operation['uri']
                        # Get the EDAM format id from the url:
                        EDAM_id = EDAM_url.split('/')[-1]
                        # Store the operation
                        if idx in operations2agent:
                            operations2agent[idx].append(EDAM_id)
                        else:
                            operations2agent[idx] = [EDAM_id]
                    else: # No url defined
                        # Store empty operation
                        if idx in operations2agent:
                            operations2agent[idx].append("")
                        else:
                            operations2agent[idx] = [""]
            else:
                operations2agent[idx] = [""]
                    

            # Same procedure as with the input defined above:
    if 'function' in agent:
        for function in agent['function']:
            # Now all the inputs of the agent function:
            if 'output' in function:
                for f_output in function['output']:
                    if 'dataType' in f_output:
                        curr_type = ""
                        dataType = f_output['dataType']
                        # Extract and keep the EDAM url:
                        if 'uri' in dataType:
                            EDAM_url = dataType['uri']
                            # Get the EDAM format id from the url:
                            EDAM_id = EDAM_url.split('/')[-1]
                            curr_type = EDAM_id
                            # Store the agent index for this EDAM output format:
                            if EDAM_id in output2agent2:
                                output2agent2[EDAM_id].append(idx)
                            else:
                                output2agent2[EDAM_id] = [idx]
                        else: # No url defined
                            pass
                        # Then all the data formats used for the input:
                        if 'dataFormat' in f_output:
                            for dataFormat in f_output['dataFormat']:
                                # Extract and keep the EDAM url:
                                if 'uri' in dataFormat:
                                    EDAM_url = dataFormat['uri']
                                    # Get the EDAM format id from the url:
                                    EDAM_id = EDAM_url.split('/')[-1]
                                    # Store the agent index for this EDAM input format:
                                    combkey = curr_type + "|" + EDAM_id
                                    # print(combkey + " " + name)
                                    if EDAM_id in output2agent:
                                        output2agent[EDAM_id].append(idx)
                                    else:
                                        output2agent[EDAM_id] = [idx]
                                    if combkey in output2agent3:
                                        output2agent3[combkey].append(idx)
                                    else:
                                        output2agent3[combkey] = [idx]                                        
                                else: # No url defined
                                    pass
                            else: # No dataFormat or EDAM_url defined
                                pass
                    else: # No dataType defined
                        pass
            else: # No output defined
                pass
        
    else: # No function defined
        pass


# Remove duplicate entries:
for EDAM_id, outagent_idx in output2agent.items():
    output2agent[EDAM_id] = sorted(list(set(outagent_idx)))

for EDAM_id, inagent_idx in input2agent.items():
    input2agent[EDAM_id] = sorted(list(set(inagent_idx)))

for EDAM_id, outagent_idx in output2agent3.items():
    output2agent3[EDAM_id] = sorted(list(set(outagent_idx)))

for EDAM_id, inagent_idx in input2agent3.items():
    input2agent3[EDAM_id] = sorted(list(set(inagent_idx)))



# Find the agents with matching output and input:
out_match_in = dict()
# provides EDAM format for each pair of agents
out_edam_in = dict()
# Look through all the EDAM output formats:
for EDAM_id, outagent_idx in output2agent.items():
    # Is the output format also existing as and input to another agent?:
    if EDAM_id in input2agent:
        inagent_idx = input2agent[EDAM_id]
        # Now make the connection between the list of input agents and each matching output agent:
        for agent in outagent_idx:
            if agent in out_match_in:
                # Remove dublicates on the fly, or the dict will grow huge:
                out_match_in[agent] = sorted(list(set(out_match_in[agent] + inagent_idx)))
                for inagent in inagent_idx:
                    ind = "_".join((str(agent),str(inagent)))
                    if ind in out_edam_in:
                        out_edam_in[ind] = sorted(list(set(out_edam_in[ind] + [EDAM_id])))
                    else:
                        out_edam_in[ind] = [EDAM_id]
            else:
                out_match_in[agent] = inagent_idx
                for inagent in inagent_idx:
                    ind = "_".join((str(agent),str(inagent)))
                    out_edam_in[ind] = [EDAM_id]
else:
        pass

# Find the agents with matching output and input:
out_match_in3 = dict()
# provides EDAM format for each pair of agents
out_edam_in3 = dict()
# Look through all the EDAM output formats:
for EDAM_id, outagent_idx in output2agent3.items():
    # Is the output format also existing as and input to another agent?:
    if EDAM_id in input2agent3:
        inagent_idx = input2agent3[EDAM_id]
        # Now make the connection between the list of input agents and each matching output agent:
        for agent in outagent_idx:
            if agent in out_match_in3:
                # Remove dublicates on the fly, or the dict will grow huge:
                out_match_in3[agent] = sorted(list(set(out_match_in3[agent] + inagent_idx)))
                for inagent in inagent_idx:
                    ind = "_".join((str(agent),str(inagent)))
                    if ind in out_edam_in3:
                        out_edam_in3[ind] = sorted(list(set(out_edam_in3[ind] + [EDAM_id])))
                    else:
                        out_edam_in3[ind] = [EDAM_id]
            else:
                out_match_in3[agent] = inagent_idx
                for inagent in inagent_idx:
                    ind = "_".join((str(agent),str(inagent)))
                    out_edam_in3[ind] = [EDAM_id]
else:
        pass
   

# Print the results to a Cytoscape tab separated interaction files (1. combined entry per matching EDAM format, 2. individual entries):
with open("bioagents.interactions", 'w') as file_handle:
    # Print header:
    print('{0}\t{1}\t{2}\t{3}'.format('agent name/source node', 'agent name/target node', 'interaction format', 'source EDAM operations', 'target EDAM operations'), end="\n", file=file_handle)
    # Go through all agents with output matching an input:
    for out_agent, in_list in out_match_in.items():
        # Convert the output agent index to its name:
        out_name = idx2name[out_agent]
        out_operations = operations2agent[out_agent]
        # Print each interaction as one line in the file:
        for in_agent in in_list:
            # Convert the input agent index to its name:
            in_name = idx2name[in_agent]
            in_operations = operations2agent[in_agent]
            edam_name = out_edam_in["_".join((str(out_agent),str(in_agent)))]
            print('{0}\t{1}\t{2}\t{3}\t{4}'.format(out_name, edam_name,  in_name, out_operations, in_operations), end="\n", file=file_handle)

with open("bioagents.interactions.full", 'w') as file_handle:
    # Print header:
    print('{0}\t{1}\t{2}\t{3}'.format('agent name/source node', 'agent name/target node', 'interaction format', 'source EDAM operations', 'target EDAM operations'), end="\n", file=file_handle)
    # Go through all agents with output matching an input:
    for out_agent, in_list in out_match_in.items():
        # Convert the output agent index to its name:
        out_name = idx2name[out_agent]
        out_operations = operations2agent[out_agent]
        # Print each interaction as one line in the file:
        for in_agent in in_list:
            # Convert the input agent index to its name:
            in_name = idx2name[in_agent]
            in_operations = operations2agent[in_agent]
            edam_name = out_edam_in["_".join((str(out_agent),str(in_agent)))]
            for edam_fo in edam_name:
                print('{0}\t{1}\t{2}\t{3}\t{4}'.format(out_name, edam_fo,  in_name, out_operations, in_operations), end="\n", file=file_handle)

with open("bioagents.interactions.combEDAM", 'w') as file_handle:
    # Print header:
    print('{0}\t{1}\t{2}\t{3}'.format('agent name/source node', 'interaction format', 'agent name/target node', 'source EDAM operations', 'target EDAM operations'), end="\n", file=file_handle)
    # Go through all agents with output matching an input:
    for out_agent, in_list in out_match_in3.items():
        # Convert the output agent index to its name:
        out_name = idx2name[out_agent]
        out_operations = operations2agent[out_agent]
        # Print each interaction as one line in the file:
        for in_agent in in_list:
            # Convert the input agent index to its name:
            in_name = idx2name[in_agent]
            in_operations = operations2agent[in_agent]
            edam_name = out_edam_in3["_".join((str(out_agent),str(in_agent)))]
            for edam_fo in edam_name:
                print('{0}\t{1}\t{2}\t{3}\t{4}'.format(out_name, edam_fo,  in_name, out_operations, in_operations), end="\n", file=file_handle)

