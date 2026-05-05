oakcross_mira_assignment:
    type: assignment
    actions:
        on assignment:
        - trigger name:click state:true cooldown:2s
    interact scripts:
    - oakcross_mira_interact

oakcross_mira_interact:
    type: interact
    steps:
        1:
            click trigger:
                script:
                - if !<player.has_flag[oakcross.met_mira]>:
                    - flag player oakcross.met_mira
                    - chat "You're new to Oakcross, <player.name>. Read the board and keep to the patrolled roads."
                    - stop
                - if <server.has_flag[oakcross.profile.market_day]> && !<player.has_flag[oakcross.market_tip_heard]>:
                    - flag player oakcross.market_tip_heard
                    - chat "Market day's live, <player.name>. The square is crowded and the best contracts go first."
                    - stop
                - if <server.has_flag[oakcross.season.autumn]>:
                    - chat "Autumn caravans have started arriving. Expect fuller roads and thinner tempers."
                    - stop
                - chat "Board's current, gates are watched, and Oakcross is still holding."

oakcross_elira_assignment:
    type: assignment
    actions:
        on assignment:
        - trigger name:click state:true cooldown:2s
    interact scripts:
    - oakcross_elira_interact

oakcross_elira_interact:
    type: interact
    steps:
        1:
            click trigger:
                script:
                - if !<player.has_flag[oakcross.met_elira]>:
                    - flag player oakcross.met_elira
                    - chat "First stay in Oakcross, <player.name>? Keep a bed claimed and you'll always have a safe return."
                    - stop
                - if <server.has_flag[oakcross.profile.gathering_week]> && !<player.has_flag[oakcross.gathering_tip_heard]>:
                    - flag player oakcross.gathering_tip_heard
                    - chat "Gathering week's packed the tavern. Bread, herbs, and rabbit stew are moving fastest today."
                    - stop
                - if <server.has_flag[oakcross.profile.traveler_week]>:
                    - chat "More travelers than locals tonight. If you hear road rumors, bring them back to me."
                    - stop
                - chat "Beds are warm, stew is hot, and rumors travel faster than carts in this town."

oakcross_bram_assignment:
    type: assignment
    actions:
        on assignment:
        - trigger name:click state:true cooldown:2s
    interact scripts:
    - oakcross_bram_interact

oakcross_bram_interact:
    type: interact
    steps:
        1:
            click trigger:
                script:
                - if !<player.has_flag[oakcross.met_bram]>:
                    - flag player oakcross.met_bram
                    - chat "You bring ore, I turn it into work worth carrying. That's how this place functions."
                    - stop
                - if <server.has_flag[oakcross.profile.road_patrol]> && !<player.has_flag[oakcross.rowan_patrol_heard]>:
                    - flag player oakcross.rowan_patrol_heard
                    - chat "Rowan's pushing more patrols east. Means more repairs and fewer surprises at the gate."
                    - stop
                - if <server.has_flag[oakcross.season.winter]>:
                    - chat "Winter cracks tool handles. Check your gear before you trust it."
                    - stop
                - chat "Sharp tools, sound armor, no wasted motion. That's all I promise."

oakcross_rowan_assignment:
    type: assignment
    actions:
        on assignment:
        - trigger name:click state:true cooldown:2s
    interact scripts:
    - oakcross_rowan_interact

oakcross_rowan_interact:
    type: interact
    steps:
        1:
            click trigger:
                script:
                - if !<player.has_flag[oakcross.met_rowan]>:
                    - flag player oakcross.met_rowan
                    - chat "If you leave Oakcross by the east road, return before dark or travel armed."
                    - stop
                - if <server.has_flag[oakcross.profile.road_patrol]>:
                    - chat "Patrols doubled this week. Fewer bandits, but more reason to report what you see."
                    - stop
                - if <server.has_flag[oakcross.profile.market_day]>:
                    - chat "Crowds make cover for thieves. Keep your eyes up in the square today."
                    - stop
                - chat "Quiet roads are earned, not given. Help keep them that way."

oakcross_sella_assignment:
    type: assignment
    actions:
        on assignment:
        - trigger name:click state:true cooldown:2s
    interact scripts:
    - oakcross_sella_interact

oakcross_sella_interact:
    type: interact
    steps:
        1:
            click trigger:
                script:
                - if !<player.has_flag[oakcross.met_sella]>:
                    - flag player oakcross.met_sella
                    - chat "Trade's simple, <player.name>: move what people need before somebody else does."
                    - stop
                - if <server.has_flag[oakcross.profile.market_day]>:
                    - chat "Best prices are at first bell and worst tempers at last bell. Shop early."
                    - stop
                - if <server.has_flag[oakcross.season.spring]>:
                    - chat "Spring stock is fresher, lighter, and gone before noon if I guessed right."
                    - stop
                - chat "Come back when the caravans change and so will my stall."

oakcross_fen_assignment:
    type: assignment
    actions:
        on assignment:
        - trigger name:click state:true cooldown:2s
    interact scripts:
    - oakcross_fen_interact

oakcross_fen_interact:
    type: interact
    steps:
        1:
            click trigger:
                script:
                - if !<player.has_flag[oakcross.met_fen]>:
                    - flag player oakcross.met_fen
                    - chat "You learn the woods by surviving them. Start by listening before you walk."
                    - stop
                - if <server.has_flag[oakcross.profile.traveler_week]>:
                    - chat "Too many boots on the road this week. Tracks won't mean much until the crowds thin."
                    - stop
                - if <server.has_flag[oakcross.season.summer]>:
                    - chat "Summer makes the tree line loud. Trouble hides behind all that noise."
                    - stop
                - chat "The ruin stays quiet right before it doesn't. Be ready for that shift."