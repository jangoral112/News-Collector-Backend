CREATE TABLE users (
	user_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    user_authkey VARCHAR(24) NOT NULL,
    PRIMARY KEY (user_id)
) ENGINE=INNODB;

CREATE TABLE websites (
	website_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    website_name VARCHAR(64) NOT NULL,
    website_link VARCHAR(2083) NOT NULL,
    PRIMARY KEY (website_id)
) ENGINE=INNODB;


CREATE TABLE rss_feeds (
	feed_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    feed_name VARCHAR(64) NOT NULL,
    feed_link VARCHAR(2083) NOT NULL,
    website_id INT UNSIGNED NOT NULL,
    CONSTRAINT fk__rss_feeds__websites__website_id
		FOREIGN KEY (website_id) REFERENCES websites(website_id),
    PRIMARY KEY (feed_id)
) ENGINE=INNODB;

CREATE TABLE users_feeds (
	user_id INT UNSIGNED NOT NULL,
    feed_id INT UNSIGNED NOT NULL,
    PRIMARY KEY (user_id, feed_id),
    CONSTRAINT fk__users_feeds__users__user_id
		FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT fk__users_feeds__rss_feeds__feed_id
		FOREIGN KEY(feed_id) REFERENCES rss_feeds(feed_id)
		ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=INNODB;

CREATE TABLE news (
	news_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
	feed_id INT UNSIGNED NOT NULL,
    news_title VARCHAR(256) NOT NULL,
    news_link VARCHAR(2083) NOT NULL,
    news_description VARCHAR(512),
    news_img_link VARCHAR(2083),
    publish_date timestamp,
    CONSTRAINT fk__news__rss_feeds__feed_id
		FOREIGN KEY (feed_id) REFERENCES rss_feeds(feed_id),
	PRIMARY KEY (news_id)
) ENGINE=INNODB;

CREATE TABLE keywords (
	keyword_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    keyword_value VARCHAR(256),
    PRIMARY KEY(keyword_id)
) ENGINE=INNODB;

CREATE TABLE users_keywords (
	user_id INT UNSIGNED NOT NULL ,
    keyword_id INT UNSIGNED NOT NULL,
    PRIMARY KEY(user_id, keyword_id),
	CONSTRAINT fk__user_keywords__users__user_id
		FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT fk__user_keywords__keywords__keyword_id
		FOREIGN KEY (keyword_id) REFERENCES keywords(keyword_id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=INNODB;

CREATE TABLE news_keywords (
	news_id INT UNSIGNED NOT NULL ,
    keyword_id INT UNSIGNED NOT NULL,
    PRIMARY KEY(news_id, keyword_id),
	CONSTRAINT fk__news_keywords__news__news_id
		FOREIGN KEY (news_id) REFERENCES news(news_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT fk__news_keywords__keywords__keyword_id
		FOREIGN KEY (keyword_id) REFERENCES keywords(keyword_id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=INNODB;