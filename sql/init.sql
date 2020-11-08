CREATE SCHEMA broker;

USE broker;

CREATE TABLE User
(
    id         INT             NOT NULL UNIQUE AUTO_INCREMENT,
    user_key   CHAR(36)        NOT NULL UNIQUE,
    name       VARCHAR(200)    NOT NULL,
    document   VARCHAR(14)     NOT NULL,
    email      VARCHAR(400)    NOT NULL,
    balance    BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at DATETIME                 DEFAULT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE Asset
(
    id         INT          NOT NULL UNIQUE AUTO_INCREMENT,
    code       VARCHAR(5)   NOT NULL UNIQUE,
    name       VARCHAR(500) NOT NULL,
    created_at TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE TABLE Wallet
(
    id         INT             NOT NULL UNIQUE AUTO_INCREMENT,
    user_id    INT             NOT NULL,
    asset_id   INT             NOT NULL,
    quantity   BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY fk_wallet_user (user_id) REFERENCES User (id),
    FOREIGN KEY fk_wallet_asset (asset_id) REFERENCES Asset (id),
    UNIQUE unique_user_asset (user_id, asset_id)
);


CREATE TABLE Transfer
(
    id                      INT             NOT NULL UNIQUE AUTO_INCREMENT,
    user_key                CHAR(36)        NOT NULL UNIQUE,
    origin_user_id          INT             NOT NULL,
    destination_user_id     INT             NOT NULL,
    quantity                BIGINT UNSIGNED NOT NULL,
    unit_price_usd          BIGINT UNSIGNED NOT NULL,
    usd_brl_conversion_rate DECIMAL(15, 15) NOT NULL,
    total_price_brl         DECIMAL(28, 2)  NOT NULL,
    created_at              TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY fk_transfer_origin_user (origin_user_id) REFERENCES User (id),
    FOREIGN KEY fk_transfer_destination_user (destination_user_id) REFERENCES User (id)
);

