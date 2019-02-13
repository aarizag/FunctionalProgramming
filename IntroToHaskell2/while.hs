while :: state ->
    (state -> Bool) ->
    (state -> state) ->
    (state -> result) ->
    result

while cur_state cont_cond action final_action =
    if cont_cond then while $ action cur_state cont_cond action final_action
    else final_action cur_state

