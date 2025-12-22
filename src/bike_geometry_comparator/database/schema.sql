CREATE TABLE bike_geometry
(
    brand TEXT NOT NULL,
    model TEXT NOT NULL,
    year  INTEGER CHECK ( year == -1 OR (year > 1900 AND year < 2100)
) DEFAULT -1,
    size                  TEXT NOT NULL,

    -- always means horizontal length
    top_tube_length       INTEGER DEFAULT NULL,
    seat_tube_length      INTEGER DEFAULT NULL,
    seat_tube_angle       FLOAT DEFAULT NULL,
    head_tube_angle       FLOAT DEFAULT NULL,
    chainstay             INTEGER DEFAULT NULL,
    fork_rake             INTEGER DEFAULT NULL,
    wheelbase             INTEGER DEFAULT NULL,
    trail                 INTEGER DEFAULT NULL,
    bb_drop               INTEGER DEFAULT NULL,
    front_center_distance INTEGER DEFAULT NULL,
    head_tube_length      INTEGER DEFAULT NULL,
    stack                 INTEGER CHECK ( stack > 400 AND stack < 800) NOT NULL,
    reach                 INTEGER CHECK ( reach > 300 AND reach < 600) NOT NULL,
    standover_height      INTEGER DEFAULT NULL,
    fork_axle_to_crown    INTEGER DEFAULT NULL,

    -- here goes list of some custom bike manufacturers metrics

    -- components

    -- in mm
    stem_length          INTEGER CHECK ( stem_length == NULL OR (stem_length > 9 AND stem_length <= 200)) DEFAULT NULL,
    -- in mm
    handlebar_width      INTEGER CHECK ( handlebar_width == NULL OR (handlebar_width >= 200 AND handlebar_width <= 900)) DEFAULT NULL,
    -- some measurments for integrated handlebar including stem length
    cockpit_dimensions TEXT DEFAULT NULL,
    -- in mm
    crank_length         FLOAT CHECK ( crank_length == NULL OR (crank_length >= 120 AND crank_length <= 220)) DEFAULT NULL,
    chainring_size       TEXT DEFAULT NULL,
    seat_post_diameter   TEXT DEFAULT NULL,
    -- in mm
    seat_post_length     INTEGER CHECK ( seat_post_length == NULL OR (seat_post_length >= 20 AND seat_post_length <= 600)) DEFAULT NULL,
    wheel_size           TEXT DEFAULT NULL,
    saddle_width         INTEGER CHECK ( saddle_width == NULL OR (saddle_width >= 50 AND saddle_width <= 300)) DEFAULT NULL,

    -- recommended body height
    body_height_range   TEXT DEFAULT NULL,
    -- seat height adjustable range
    seat_height_range   TEXT DEFAULT NULL,

    PRIMARY KEY (brand, model, year, size)
);