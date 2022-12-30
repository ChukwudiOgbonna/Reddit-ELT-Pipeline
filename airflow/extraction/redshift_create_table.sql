CREATE TABLE IF NOT EXISTS redshift_table(
id varchar PRIMARY KEY,
title varchar(max),
num_comments int,
score int,
author varchar(max),
created_utc timestamp,
url varchar(max),
upvote_ratio float,
over_18 bool,
edited bool,
spoiler bool,
stickied bool
);
