CREATE TABLE "user"
(
    id          VARCHAR(36) PRIMARY KEY  NOT NULL,
    name        VARCHAR(100)             NULL,
    email       VARCHAR(100) UNIQUE      NOT NULL,
    picture_url VARCHAR(255)             NULL,
    created_at  TIMESTAMP WITH TIME ZONE NOT NULL
);