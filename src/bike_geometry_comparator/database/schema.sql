CREATE TABLE bike_geometry
(
    brand TEXT NOT NULL,
    model TEXT NOT NULL,
    year  INTEGER CHECK ( year == -1 OR (year > 1900 AND year < 2100)
) DEFAULT -1,
    size                  TEXT NOT NULL,

    top_tube_horizontal   INTEGER DEFAULT NULL,
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

    PRIMARY KEY (brand, model, year, size)
);