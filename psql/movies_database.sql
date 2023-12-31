CREATE SCHEMA IF NOT EXISTS content;

CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    rating FLOAT,
    type TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid PRIMARY KEY,
    genre_id uuid NOT NULL,
    film_work_id uuid NOT NULL,
    created timestamp with time zone,
    CONSTRAINT fk_genre_id
        FOREIGN KEY (genre_id)
        REFERENCES content.genre (id)
        ON DELETE CASCADE,
    CONSTRAINT fk_film_id
        FOREIGN KEY (film_work_id)
        REFERENCES content.film_work (id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
    person_id uuid NOT NULL,
    film_work_id uuid NOT NULL,
    role TEXT,
    created timestamp with time zone,
    CONSTRAINT fk_person_id
        FOREIGN KEY (person_id)
        REFERENCES content.person (id)
        ON DELETE CASCADE,
    CONSTRAINT fk_film_id
        FOREIGN KEY (film_work_id)
        REFERENCES content.film_work (id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS content.user_admin (
    id uuid PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    password TEXT,
    first_name TEXT,
    last_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE,
    last_login timestamp with time zone
);

CREATE UNIQUE INDEX film_work_person_idx ON content.person_film_work (film_work_id, person_id, role);
CREATE UNIQUE INDEX film_work_genre_idx ON content.genre_film_work (film_work_id, genre_id);
CREATE UNIQUE INDEX  title_creation_date_idx ON content.film_work (title, creation_date);
CREATE INDEX film_work_title_idx ON content.film_work (title);
CREATE INDEX person_full_name_idx ON content.person (full_name)