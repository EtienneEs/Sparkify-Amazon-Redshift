import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

staging_events_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_events
(
    artist          VARCHAR,
    auth            VARCHAR,
    firstName       VARCHAR,
    gender          VARCHAR(10),
    itemInSession   INT,
    lastName        VARCHAR,
    length          DECIMAL,
    level           VARCHAR,
    location        VARCHAR,
    method          VARCHAR,
    page            VARCHAR,
    registration    DECIMAL,
    sessionId       VARCHAR,
    song            VARCHAR,
    status          INT,
    ts              BIGINT,
    userAgent       VARCHAR,
    userId          VARCHAR
);
""")

staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_songs
(
    num_songs           INT,
    artist_id           VARCHAR,
    artist_latitude     DECIMAL,
    artist_longitude    DECIMAL,
    artist_location     VARCHAR,
    artist_name         VARCHAR,
    song_id             VARCHAR,
    title               VARCHAR,
    duration            DECIMAL,
    year                INT
);
""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays
(
    songplay_id     BIGINT IDENTITY(0,1) SORTKEY DISTKEY,
    start_time      VARCHAR,
    user_id         INT,
    level           VARCHAR,
    song_id         VARCHAR,
    artist_id       VARCHAR,
    session_id      INT,
    location        VARCHAR,
    user_agent      VARCHAR
);
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users
(
    user_id     INT SORTKEY,
    first_name  VARCHAR,
    last_name   VARCHAR,
    gender      VARCHAR(10),
    level       VARCHAR
);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs
(
    song_id     VARCHAR SORTKEY,
    title       VARCHAR NOT NULL,
    artist_id   VARCHAR,
    duration    DECIMAL,
    year        INT
);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists
(
    artist_id           VARCHAR SORTKEY,
    name                VARCHAR,
    location            VARCHAR,
    latitude     DECIMAL,
    longitude    DECIMAL
);
""")

time_table_create = ("""
CREATE TABLE time (
    start_time  TIMESTAMP SORTKEY,
    hour        INT,
    day         INT,
    week        INT,
    month       INT,
    year        INT,
    weekday     INT
);
""")

# STAGING TABLES

staging_events_copy = ("""
COPY staging_events FROM {}
iam_role {}
FORMAT AS JSON 'auto'
REGION 'us-west-2';
""").format(config.get("S3", "LOG_DATA"), config.get("IAM_ROLE", "ARN"))

staging_songs_copy = ("""
COPY staging_songs FROM {}
iam_role {}
FORMAT AS JSON 'auto'
REGION 'us-west-2' maxerror 10;
""").format(config.get("S3", "SONG_DATA"), config.get("IAM_ROLE", "ARN"))

# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO songplays(
    start_time,
    user_id,
    level,
    song_id,
    artist_id,
    session_id,
    location,
    user_agent
)
(
    SELECT
        TIMESTAMP 'epoch' + ev.ts/1000 * INTERVAL '1 second' as start_time,
        CAST(ev.userId AS INT),
        ev.level,
        so.song_id,
        so.artist_id,
        CAST(ev.sessionId AS INT),
        ev.location,
        ev.userAgent
    FROM
        staging_events ev
    LEFT OUTER JOIN staging_songs so
        ON (ev.song = so.title AND ev.artist = so.artist_name)
    WHERE ev.page = 'NextSong'
)
""")

user_table_insert = ("""
INSERT INTO users(
    user_id,
    first_name,
    last_name,
    gender,
    level
)
(
SELECT DISTINCT CAST(userid AS INT),
    firstname,
    lastname,
    gender,
    level
FROM staging_events WHERE userid IS NOT NULL
)
""")

song_table_insert = ("""
INSERT INTO songs(song_id, title, artist_id, year, duration)
(SELECT DISTINCT song_id, title, artist_id, year, duration FROM staging_songs)
""")

artist_table_insert = ("""
INSERT INTO artists(
    artist_id,
    name,
    location,
    latitude,
    longitude
)
(
SELECT
    DISTINCT artist_id,
    artist_name,
    artist_location,
    artist_latitude,
    artist_longitude
FROM staging_songs
)
""")

time_table_insert = ("""
INSERT INTO time(
    start_time,
    hour,
    day,
    week,
    month,
    year,
    weekday
)
SELECT DISTINCT ts.start_time as start_time,
    EXTRACT (HOUR FROM ts.start_time) as hour,
    EXTRACT (DAY FROM ts.start_time) as day,
    EXTRACT (WEEK FROM ts.start_time) as week,
    EXTRACT (MONTH FROM ts.start_time) as month,
    EXTRACT (YEAR FROM ts.start_time) as year,
    EXTRACT (WEEKDAY FROM ts.start_time) as weekday
FROM (
    SELECT TIMESTAMP 'epoch' + ev.ts/1000 * INTERVAL '1 second' as start_time
    FROM staging_events ev
    ) ts
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
