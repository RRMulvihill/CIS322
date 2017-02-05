SQL files and scripts used to create a new database to store OSNAP's legacy data. Once a database has been initialized, run these commands in order. 1. $ psql -f create_tables.sql [DATABASE NAME] -p[PORT NAME (optional)] 2. $ psql -f import_data.sql [DATABASE NAME] -p[PORT NAME (optional)]

create_tables.sql : Adds the tables products, assets, vehicles, facilities, assets_at, convoys, used_by, assets_on, users, roles, user_is, user_supports, levels, compartments, and security_tags to the database. These tables have variables according to LOST documentation.

import_data.sql : Adds product and asset entires from the legacy data. I chose to use manual sql commands rather than python as the legacy data was not uniform, had missing information, and needed human judgment on a individual level.

The instructions on this assignment were vague in regard to what data is to be trnsferred, I made my best guess at what to include and what to ommit. Few assets and products mached descriptions to connect private and foreign keys, most have been given a null value.

I hope making import_data an sql instead of ssh wont count against me, it seemed unecessary to write a script that would just run the sql file, so I trimmed it out.
