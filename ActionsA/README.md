 text comes with <text> and <id>

 <get_element>

->  process text, find <action_points> <action_of>
    We have defined <action_of.txt> and <action_params.txt>

 Based on Action_of, decide to <update_element> using <action_params>

 Use hash table to find current state_id

 Use hash table to <state_id; action_point, Action_params> --->> <new_state_id> //update state_id

 Use <state_id> to respond_text

<system defined>
 Text, Entities, Action_point

<user defined>
 Element
 Action_on, Action_params,
 State, State_transition_table, State_response_nlg

 <b> NLE:  Natural Language Extraction </b>

We have our NER: Named Entity Recognition which will tag entities such as
1. day
2. time
3. duration
4. distance
5. quantity
6. email
7. phone numbers
8. location (plus cities and countries)

If you define your own entity like 'music artists' or 'songs' -> then you should define your own bag of words in simple text file with each music artist or a song in new line.

When you define the Element in template.json, make sure you use either one of our given entities from NER, or from the one you defined yourself. It is very crucial that the names match exactly. 


 Named Entity Recog. extracting root words. knowledge graph.

<b> NLU: Natural Langauge Understanding </b>

State Transition Table

<b> NLG: Natural Langauge Generation </b>

NLG Response Function Associated to each State
